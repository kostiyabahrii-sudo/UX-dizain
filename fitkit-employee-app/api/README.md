# Fitkit — Employee Workspace API (Go)

Back-end for the buyer workspace in [`../web`](../web). Go 1.24, standard library HTTP router, PostgreSQL via pgx, Server-Sent Events for live updates. The business rules are the same as in the front-end (`web/src/domain/rules.ts` ↔ `internal/domain/rules.go`) and are re-checked on every request.

## Run locally

Needs Go 1.24+ and PostgreSQL 14+ (or Docker).

```bash
# with Docker: database + API on :8080
docker compose up --build
docker compose run --rm api seed          # demo data (same as the front-end mock)

# or with your own PostgreSQL
export DATABASE_URL="postgres://user:pass@localhost:5432/fitkit?sslmode=disable"
go run ./cmd/api seed                     # migrate + load demo data
CLIENT_APP_WEBHOOK_SECRET=dev TRACKER_WEBHOOK_SECRET=dev go run ./cmd/api serve
```

Demo logins (password `fitkit-demo`): `anna@fitkit.space` (buyer), `taras@fitkit.space` (buyer), `iryna@fitkit.space` (shift lead), `sklad@fitkit.space` (warehouse).

Real employees: `go run ./cmd/api create-employee -name "…" -email … -role buyer -password …`

Configuration is read from the environment — see [`.env.example`](.env.example).

## Tests

```bash
go test ./internal/domain/                                     # rules, no database
TEST_DATABASE_URL="postgres://…/fitkit_test?sslmode=disable" go test -p 1 ./...   # + API scenarios (wipes that DB)
```

The API tests run the full flows over HTTP against PostgreSQL: login/logout, a request card from sold-out item to purchase (refund sent, store parcels created), price confirmation answered by the client app webhook, auto-refund after 24 h, shipping only after every parcel is at the warehouse, Nova Poshta shipment and delivery via the tracking webhook, manual tracking numbers, stalled parcels, 20 concurrent “take” calls (exactly one wins), full cancellation refund, idempotent order ingestion, support tickets, the live event stream.

## Structure

```
cmd/api/              main: serve | migrate | seed | create-employee
internal/domain/      entities, rules (price tolerance, confirmation, purchase guard, money), tests
internal/store/       PostgreSQL queries; migrations/*.sql embedded and applied on start
internal/service/     operations: one transaction each, history entries, side effects after commit
internal/httpapi/     JSON API, auth, HMAC-signed webhooks, SSE hub; api_test.go
internal/integrations/ interfaces + fakes: Nova Poshta, tracking aggregator, payments, client app
internal/jobs/        every minute: auto-refund unanswered confirmations, flag stalled parcels
internal/seed/        demo data
```

## Auth

`POST /api/auth/login {email, password}` → sets an HttpOnly cookie `fitkit_session` and returns `{token, me}`. Send the cookie (browser) or `Authorization: Bearer <token>`. Sessions last 30 days; only a SHA-256 of the token is stored. `POST /api/auth/logout` ends the session.

Permissions: an order is changed by its owner or a shift lead (`lead`); the warehouse (`warehouse`) can receive parcels and ship; anyone signed in can take a new request and answer support tickets.

## API

Amounts are in **kopiyky** (1 ₴ = 100). Errors: `{"error": "<message in Ukrainian>"}` with 400 / 401 / 403 / 404 / 409 / 502.

| Method & path | Body | Does |
| --- | --- | --- |
| `GET /api/me` | | Current employee |
| `GET /api/bootstrap` | | Everything the UI shows: me, employees, clients, orders, shipments, tickets |
| `GET /api/events` | | SSE stream: `event: order\|shipment\|ticket`, `data: {"type","id"}` — refetch that object |
| `GET /api/orders?status=new,in_progress&owner=me&client=…` | | Orders with items, notes, history, `money`, `clientSees`, `canPurchase` |
| `GET /api/orders/{id}` | | One order (same shape) |
| `POST /api/orders/take-next` | | Assign the oldest new request to me |
| `POST /api/orders/{id}/take` | | Take a request (409 if someone was faster) |
| `POST /api/orders/{id}/status` | `{status}` | `purchased` (all items resolved; creates store parcels), `shipped`, `delivered`, `in_progress` |
| `PATCH /api/orders/{id}/items/{itemId}` | `{action, price?}` | `check`, `sold_out`, `store_price` (+`price`), `send_confirmation`, `client_confirmed`, `cancel` (refund) |
| `PUT /api/orders/{id}/problem` | `{problem: string\|null}` | Flag or clear a problem |
| `POST /api/orders/{id}/notes` | `{text}` | Team note |
| `POST /api/orders/{id}/cancel` | | Cancel before purchase, refund what is left |
| `POST /api/orders/{id}/ship` | | Create the Nova Poshta ТТН (all store parcels at the warehouse) |
| `GET /api/clients`, `GET /api/clients/{id}` | | Clients |
| `GET /api/shipments?order=…` | | Parcels of both legs with tracking events |
| `POST /api/shipments/{id}/tracking` | `{tracking, carrier?}` | Add a store tracking number; registered with the aggregator |
| `POST /api/shipments/{id}/arrived` | | Warehouse received the parcel |
| `GET /api/tickets?status=open` | | Support tickets with messages |
| `POST /api/tickets/{id}/messages` | `{text}` | Reply as Fitkit Support (sent to the client app) |
| `POST /api/tickets/{id}/resolve` | | Close the ticket |

### Webhooks (signed)

Header `X-Fitkit-Signature: sha256=<hex HMAC-SHA256 of the raw body>`; secrets `CLIENT_APP_WEBHOOK_SECRET` and `TRACKER_WEBHOOK_SECRET`.

| Path | From | Body |
| --- | --- | --- |
| `POST /webhooks/client-app/orders` | Fitkit app | `{externalId, paid, fee, client: {externalId, name, phone, telegram?, city, branch, sizes?, stores?}, items: [{name, store, url, size, qty, price?, photo?, comment?}]}` — idempotent by `externalId` |
| `POST /webhooks/client-app/confirmations` | Fitkit app | `{orderExternalId, itemId, accept}` — answer to a price confirmation |
| `POST /webhooks/client-app/messages` | Fitkit app | `{clientExternalId, orderExternalId?, text}` — opens or continues a support ticket |
| `POST /webhooks/tracking` | Tracking aggregator adapter | `{tracking, status: in_transit\|arrived_warehouse\|delivered\|exception, title, detail?, at?}` |

Each aggregator (17TRACK, AfterShip, …) has its own payload, so a small adapter maps it to `/webhooks/tracking`.

## Integrations

Defined in `internal/integrations` with fakes that log and record calls (used now and in tests):

- **Shipping** — Nova Poshta `InternetDocument.save` client is in `novaposhta.go`; it still needs the Fitkit sender refs and a city/branch → ref lookup (`Address.getCities`, `Address.getWarehouses`) before it replaces the fake.
- **Tracker** — register store tracking numbers with the chosen aggregator.
- **Payments** — refunds; a failed refund flags the order with a problem.
- **ClientApp** — notices to the Fitkit app: price confirmation, refund, shipped, delivered, support reply.

## Not done yet

- Front-end still runs on mock data; next step is an API client in `web/` (`/api` is already proxied to `:8080` in `vite.config.ts`) and a login screen.
- Real Nova Poshta, aggregator, payment and client-app clients (need accounts and keys).
- Warehouse photos, admin back office (analytics, rules and thresholds), login rate limiting, multi-instance events (Postgres LISTEN/NOTIFY).
