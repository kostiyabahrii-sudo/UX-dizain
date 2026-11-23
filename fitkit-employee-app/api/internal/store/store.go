// Package store is the PostgreSQL persistence layer (pgx, plain SQL).
package store

import (
	"context"
	"embed"
	"errors"
	"fmt"
	"io/fs"
	"sort"
	"strings"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

//go:embed migrations/*.sql
var migrations embed.FS

var ErrNotFound = errors.New("not found")

// DBTX is satisfied by *pgxpool.Pool and pgx.Tx.
type DBTX interface {
	Exec(ctx context.Context, sql string, args ...any) (pgconn.CommandTag, error)
	Query(ctx context.Context, sql string, args ...any) (pgx.Rows, error)
	QueryRow(ctx context.Context, sql string, args ...any) pgx.Row
}

type Store struct {
	Pool *pgxpool.Pool
}

// Q is a set of queries bound to a pool or a transaction.
type Q struct{ db DBTX }

func Open(ctx context.Context, url string) (*Store, error) {
	pool, err := pgxpool.New(ctx, url)
	if err != nil {
		return nil, err
	}
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("connect to database: %w", err)
	}
	return &Store{Pool: pool}, nil
}

func (s *Store) Close() { s.Pool.Close() }

// Q returns queries outside a transaction.
func (s *Store) Q() *Q { return &Q{db: s.Pool} }

// Tx runs fn in a transaction; it commits when fn returns nil.
func (s *Store) Tx(ctx context.Context, fn func(q *Q) error) error {
	return pgx.BeginFunc(ctx, s.Pool, func(tx pgx.Tx) error { return fn(&Q{db: tx}) })
}

// Migrate applies the embedded migrations in order, once each.
func (s *Store) Migrate(ctx context.Context) error {
	if _, err := s.Pool.Exec(ctx, `CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())`); err != nil {
		return err
	}
	names, err := fs.Glob(migrations, "migrations/*.sql")
	if err != nil {
		return err
	}
	sort.Strings(names)
	for _, n := range names {
		name := strings.TrimPrefix(n, "migrations/")
		var done bool
		if err := s.Pool.QueryRow(ctx, `SELECT EXISTS (SELECT 1 FROM schema_migrations WHERE name = $1)`, name).Scan(&done); err != nil {
			return err
		}
		if done {
			continue
		}
		body, err := migrations.ReadFile(n)
		if err != nil {
			return err
		}
		if err := s.Tx(ctx, func(q *Q) error {
			if _, err := q.db.Exec(ctx, string(body)); err != nil {
				return fmt.Errorf("migration %s: %w", name, err)
			}
			_, err := q.db.Exec(ctx, `INSERT INTO schema_migrations (name) VALUES ($1)`, name)
			return err
		}); err != nil {
			return err
		}
	}
	return nil
}

// Reset drops all data (tests and demo seeding only).
func (s *Store) Reset(ctx context.Context) error {
	_, err := s.Pool.Exec(ctx, `TRUNCATE messages, tickets, tracking_events, shipments, history, notes, items, orders, clients, sessions, employees RESTART IDENTITY CASCADE; ALTER SEQUENCE order_number_seq RESTART WITH 1000`)
	return err
}

func notFound(err error) error {
	if errors.Is(err, pgx.ErrNoRows) {
		return ErrNotFound
	}
	return err
}
