// Command api runs the Fitkit employee workspace back-end.
//
//	api serve                                   start the HTTP server (default)
//	api migrate                                 apply database migrations
//	api seed                                    wipe the database and load demo data (needs ALLOW_SEED=true)
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
		if os.Getenv("ALLOW_SEED") != "true" {
			return errors.New("seed WIPES the whole database and loads demo data; set ALLOW_SEED=true to confirm (never on production)")
		}
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

// bootstrapAdmin creates the first sign-in (a shift lead) from BOOTSTRAP_ADMIN_EMAIL / BOOTSTRAP_ADMIN_PASSWORD
// when the database has no employees yet — so a fresh deployment needs no shell access.
func bootstrapAdmin(ctx context.Context, st *store.Store, log *slog.Logger) error {
	email, pass := os.Getenv("BOOTSTRAP_ADMIN_EMAIL"), os.Getenv("BOOTSTRAP_ADMIN_PASSWORD")
	if email == "" || pass == "" {
		return nil
	}
	n, err := st.Q().CountEmployees(ctx)
	if err != nil || n > 0 {
		return err
	}
	if len(pass) < 10 {
		return errors.New("BOOTSTRAP_ADMIN_PASSWORD must be at least 10 characters")
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(pass), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	name := env("BOOTSTRAP_ADMIN_NAME", "Адміністратор")
	e, err := st.Q().CreateEmployee(ctx, name, email, domain.RoleLead, string(hash))
	if err == nil {
		log.Info("first employee created from BOOTSTRAP_ADMIN_*", "email", e.Email, "role", e.Role)
	}
	return err
}

func serve(ctx context.Context, st *store.Store, log *slog.Logger) error {
	if err := bootstrapAdmin(ctx, st, log); err != nil {
		return err
	}
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
		WebDir:          os.Getenv("WEB_DIR"),
	})
	if os.Getenv("CLIENT_APP_WEBHOOK_SECRET") == "" || os.Getenv("TRACKER_WEBHOOK_SECRET") == "" {
		log.Warn("a webhook secret is not set: the matching /webhooks/* endpoints answer 503 until it is")
	}
	addr := env("ADDR", ":8080")
	if p := os.Getenv("PORT"); p != "" && os.Getenv("ADDR") == "" { // hosting platforms pass the port in PORT
		addr = ":" + p
	}
	srv := &http.Server{Addr: addr, Handler: handler, ReadHeaderTimeout: 10 * time.Second}
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
