-- Fitkit employee workspace — initial schema.
-- Money is stored in kopiyky (1 ₴ = 100) as BIGINT.

CREATE TABLE employees (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL,
  email         TEXT NOT NULL UNIQUE,
  role          TEXT NOT NULL CHECK (role IN ('buyer', 'lead', 'warehouse', 'support')),
  password_hash TEXT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  token_hash  BYTEA PRIMARY KEY,
  employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  expires_at  TIMESTAMPTZ NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX sessions_employee_idx ON sessions(employee_id);

CREATE TABLE clients (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id TEXT UNIQUE,              -- id in the Fitkit client app
  name        TEXT NOT NULL,
  phone       TEXT NOT NULL,
  telegram    TEXT,
  city        TEXT NOT NULL DEFAULT '',
  branch      TEXT NOT NULL DEFAULT '',  -- Nova Poshta branch or postomat
  sizes       TEXT NOT NULL DEFAULT '',
  stores      TEXT NOT NULL DEFAULT '',
  dislikes    TEXT,
  note        TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE SEQUENCE order_number_seq START 1000;

CREATE TABLE orders (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  number      TEXT NOT NULL UNIQUE,
  external_id TEXT UNIQUE,              -- id in the Fitkit client app
  client_id   UUID NOT NULL REFERENCES clients(id),
  owner_id    UUID REFERENCES employees(id),
  status      TEXT NOT NULL CHECK (status IN ('new', 'in_progress', 'awaiting', 'purchased', 'shipped', 'delivered', 'cancelled')),
  paid        BIGINT,                   -- what the client paid, kopiyky
  fee         BIGINT NOT NULL DEFAULT 0,
  problem     TEXT,
  location    TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  due_at      TIMESTAMPTZ NOT NULL,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX orders_status_idx ON orders(status, due_at);
CREATE INDEX orders_owner_idx ON orders(owner_id, status);
CREATE INDEX orders_client_idx ON orders(client_id, created_at DESC);

CREATE TABLE items (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  position        INT NOT NULL,
  photo           TEXT NOT NULL DEFAULT '',
  name            TEXT NOT NULL,
  store           TEXT NOT NULL,
  url             TEXT NOT NULL,
  size            TEXT NOT NULL,
  qty             INT NOT NULL DEFAULT 1 CHECK (qty > 0),
  price           BIGINT,               -- price the client paid per unit, kopiyky
  store_price     BIGINT,               -- actual store price per unit, kopiyky
  comment         TEXT,
  status          TEXT NOT NULL CHECK (status IN ('pending', 'checked', 'sold_out', 'price_up', 'awaiting', 'bought', 'cancelled')),
  confirm_sent_at TIMESTAMPTZ,          -- price confirmation sent to the client
  UNIQUE (order_id, position)
);

CREATE TABLE notes (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id   UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  author_id  UUID REFERENCES employees(id),
  author     TEXT NOT NULL,
  text       TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX notes_order_idx ON notes(order_id, created_at);

CREATE TABLE history (
  id       BIGSERIAL PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  who      TEXT NOT NULL,
  what     TEXT NOT NULL,
  at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX history_order_idx ON history(order_id, at);

CREATE TABLE shipments (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id     UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  leg          TEXT NOT NULL CHECK (leg IN ('in', 'out')),
  store        TEXT,
  carrier      TEXT,
  tracking     TEXT,
  source       TEXT CHECK (source IN ('email', 'manual', 'api')),
  problem      TEXT,
  at_warehouse BOOLEAN NOT NULL DEFAULT false,
  delivered    BOOLEAN NOT NULL DEFAULT false,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX shipments_order_idx ON shipments(order_id);
CREATE UNIQUE INDEX shipments_tracking_idx ON shipments(tracking) WHERE tracking IS NOT NULL;

CREATE TABLE tracking_events (
  id          BIGSERIAL PRIMARY KEY,
  shipment_id UUID NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
  at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  title       TEXT NOT NULL,
  detail      TEXT
);
CREATE INDEX tracking_events_shipment_idx ON tracking_events(shipment_id, at);

CREATE TABLE tickets (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id  UUID NOT NULL REFERENCES clients(id),
  order_id   UUID REFERENCES orders(id),
  status     TEXT NOT NULL CHECK (status IN ('open', 'resolved')),
  summary    TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX tickets_status_idx ON tickets(status, updated_at DESC);

CREATE TABLE messages (
  id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
  sender    TEXT NOT NULL CHECK (sender IN ('client', 'support', 'system')),
  author_id UUID REFERENCES employees(id),
  text      TEXT NOT NULL,
  at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX messages_ticket_idx ON messages(ticket_id, at);
