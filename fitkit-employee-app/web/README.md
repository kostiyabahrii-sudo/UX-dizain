# Fitkit — Employee Workspace (front-end)

React 19 + TypeScript + Vite + React Router. The five buyer screens from `../mockups`, working on mock data in memory. No back-end yet.

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # typecheck + production build into dist/
```

## Screens

| Route | Screen | What works |
| --- | --- | --- |
| `/requests` | Requests | Queue of new requests, *All / New / Overdue*, live timers, **Take next request** (oldest first) |
| `/orders/:id` | Request card | Item checks, store price, rules (≤5% covered, >5% confirmation, sold out → refund), money panel, next-step button (blocked until every item is resolved), Problem, Hand over, Cancel, team notes, history |
| `/orders` | Current orders | Board *In progress · Awaiting confirmation · Purchased · Shipped*, drag-and-drop with the same guards, *Mine / All* |
| `/clients` | Clients & support | Ticket list, thread, quick replies, reply as Fitkit Support, Resolve, client details, masked phone with *Show* |
| `/tracking` | Tracking | Both legs, tabs, problems first, timeline, add tracking number, **Create shipment & ship** (once every parcel is at the warehouse) |

The top search finds an order number, a tracking number or a client.

## Structure

```
src/
  domain/      types.ts (entities), rules.ts (price/sold-out rules, client-facing status, money), format.ts
  data/        mock.ts — mock clients, orders, shipments, tickets (times relative to page load)
  store/       AppStore.tsx — state + reducer; every action = one future API call
  components/  Layout (sidebar, search), Icon, ui (Photo, Thumbs, Avatar, StatusPill, Tabs, Modal)
  pages/       RequestsPage, OrderPage, BoardPage, ClientsPage, TrackingPage
  styles/      global.css (fitkit.space dark theme tokens), pages.css
public/assets/ logo, fonts, garment photos
```

## API to implement (replaces the reducer)

| Action in `AppStore` | Endpoint (suggested) |
| --- | --- |
| `take` | `POST /orders/:id/take` — atomic, 409 if someone took it first |
| `setStatus` | `POST /orders/:id/status` — server re-checks the guards |
| `itemCheck`, `itemSoldOut`, `itemStorePrice` | `PATCH /orders/:id/items/:itemId` |
| `itemSendConfirm`, `itemClientConfirmed` | `POST /orders/:id/items/:itemId/confirmation` (client answers in the Fitkit app) |
| `itemCancel`, `cancelOrder` | `POST …/refund` — refund via the payment provider |
| `setProblem`, `handOver`, `addNote` | `PATCH /orders/:id`, `POST /orders/:id/notes` |
| `createOutbound` | `POST /orders/:id/shipments` — creates the Nova Poshta shipment via its API |
| `setTracking` | `POST /shipments/:id/tracking` — registers the number with the tracking aggregator |
| `sendMessage`, `resolveTicket` | `POST /tickets/:id/messages`, `POST /tickets/:id/resolve` |

Real-time updates (new requests, client confirmations, tracking webhooks, ticket messages) should arrive over WebSocket/SSE and be applied as the same actions.
Rule thresholds (`PRICE_TOLERANCE`, `CONFIRM_HOURS` in `rules.ts`) will come from the admin back office.
