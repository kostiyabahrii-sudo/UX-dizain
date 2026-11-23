// Command api runs the Fitkit employee workspace back-end.
//
//	api serve                                   start the HTTP server (default)
//	api migrate                                 apply database migrations
//	api seed                                    wipe the database and load demo data
//	api create-employee -name … -email … -role buyer|lead|warehouse|support -password …
package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"golang.org/x/crypto/bcrypt"

	"fitkit/api/internal/domain"
	"fitkit/api/internal/httpapi"
	"fitkit/api/internal/integrations"
	"fitkit/api/internal/jobs"
	"fitkit/api/internal/seed"
	"fitkit/api/internal/service"
	"fitkit/api/internal/store"
)

func env(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func main() {
	log := slog.New(slog.NewTextHandler(os.Stdout, nil))
	cmd := "serve"
	args := os.Args[1:]
	if len(args) > 0 && !strings.HasPrefix(args[0], "-") {
		cmd, args = args[0], args[1:]
	}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	if err := run(ctx, cmd, args, log); err != nil {
		log.Error("fatal", "err", err)
		os.Exit(1)
	}
}

func run(ctx context.Context, cmd string, args []string, log *slog.Logger) error {
	dbURL := env("DATABASE_URL", "postgres://postgres@localhost:5432/fitkit?sslmode=disable")
	st, err := store.Open(ctx, dbURL)
	if err != nil {
		return err
	}
	defer st.Close()
	if err := st.Migrate(ctx); err != nil {
		return err
	}

	switch cmd {
	case "migrate":
		log.Info("migrations applied")
		return nil
	case "seed":
		if err := seed.Load(ctx, st); err != nil {
			return err
		}
		log.Info("demo data loaded", "login", "anna@fitkit.space", "password", seed.DemoPassword)
		return nil
	case "create-employee":
		fs := flag.NewFlagSet(cmd, flag.ExitOnError)
		name := fs.String("name", "", "full name")
		email := fs.String("email", "", "login e-mail")
		role := fs.String("role", "buyer", "buyer | lead | warehouse | support")
		pass := fs.String("password", "", "password (min 10 characters)")
		_ = fs.Parse(args)
		if *name == "" || *email == "" || len(*pass) < 10 {
			return errors.New("create-employee: -name, -email and -password (10+ characters) are required")
		}
		switch domain.Role(*role) {
		case domain.RoleBuyer, domain.RoleLead, domain.RoleWarehouse, domain.RoleSupport:
		default:
			return fmt.Errorf("unknown role %q", *role)
		}
		hash, err := bcrypt.GenerateFromPassword([]byte(*pass), bcrypt.DefaultCost)
		if err != nil {
			return err
		}
		e, err := st.Q().CreateEmployee(ctx, *name, *email, domain.Role(*role), string(hash))
		if err != nil {
			return err
		}
		log.Info("employee created", "id", e.ID, "email", e.Email, "role", e.Role)
		return nil
	case "serve":
		return serve(ctx, st, log)
	default:
		return fmt.Errorf("unknown command %q (serve | migrate | seed | create-employee)", cmd)
	}
}

func serve(ctx context.Context, st *store.Store, log *slog.Logger) error {
	_, ints := integrations.NewFakes(log)
	if key := os.Getenv("NOVA_POSHTA_API_KEY"); key != "" {
		log.Warn("NOVA_POSHTA_API_KEY is set, but the recipient lookup (city/branch → refs) is not wired yet — using the fake shipping integration")
	}
	hub := httpapi.NewHub()
	svc := &service.Service{Store: st, Int: ints, Events: hub, Log: log}

	every, err := time.ParseDuration(env("JOBS_INTERVAL", "1m"))
	if err != nil {
		return fmt.Errorf("JOBS_INTERVAL: %w", err)
	}
	go jobs.Run(ctx, svc, every, log)

	handler := httpapi.New(httpapi.Config{
		Service: svc, Hub: hub, Log: log,
		ClientAppSecret: os.Getenv("CLIENT_APP_WEBHOOK_SECRET"),
		TrackerSecret:   os.Getenv("TRACKER_WEBHOOK_SECRET"),
		AllowOrigin:     os.Getenv("ALLOW_ORIGIN"),
		SecureCookie:    env("SECURE_COOKIE", "false") == "true",
	})
	srv := &http.Server{Addr: env("ADDR", ":8080"), Handler: handler, ReadHeaderTimeout: 10 * time.Second}
	go func() {
		<-ctx.Done()
		sctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		_ = srv.Shutdown(sctx)
	}()
	log.Info("listening", "addr", srv.Addr)
	if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		return err
	}
	return nil
}
