# Fitkit — Employee Workspace (front-end)

React 19 + TypeScript + Vite + React Router, UI on **shadcn/ui** (Radix + Tailwind CSS v4, components in `src/components/ui`), icons from lucide-react, toasts from sonner. Black / white / grey theme; colour only as small status dots (red = overdue/problem, amber = waiting, green = done). Interface in Ukrainian. Works on mock data in memory — no back-end yet.

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # typecheck + production build into dist/
```

## Screens

| Route | Screen | What works |
| --- | --- | --- |
| `/requests` | Requests | Queue of new requests, *All / New / Overdue*, live timers, **Take next request** (oldest first) |
| `/orders/:id` | Request card | Left (narrow): items with checks, store price and rules (≤5% covered, >5% confirmation, sold out → refund); delivery block with city, Nova Poshta branch, recipient, phone and items in large bold text, each with a copy button, plus *Copy all*. Right (wide): owner, due, what the client sees, money, next-step button (blocked until every item is resolved), **Problem**, **Team notes**, cancel, history |
| `/orders` | Current orders | Board *In progress · Awaiting confirmation · Purchased · Shipped*, drag-and-drop with the same guards, *Mine / All* |
| `/clients` | Clients & support | Ticket list, thread, quick replies, reply as Fitkit Support, close ticket, client details with copy buttons |
| `/tracking` | Tracking | Both legs, tabs, problems first, timeline, add tracking number, **Create shipment & ship** (once every parcel is at the warehouse — the board enforces the same rule) |

The top search finds an order number, a tracking number, a client name or phone. The bell lists what needs attention (overdue requests, problems, open tickets, stuck parcels) and links to each.

New shadcn/ui components can be added with `npx shadcn@latest add <name>` (config in `components.json`).

## Structure

```
src/
  domain/      types.ts (entities), rules.ts (price/sold-out rules, client-facing status, money), format.ts
  data/        mock.ts — mock clients, orders, shipments, tickets (times relative to page load)
  store/       AppStore.tsx — state + reducer; every action = one future API call
  components/  ui/ (shadcn/ui: button, badge, card, input, textarea, tabs, table, dialog, alert-dialog, dropdown-menu, tooltip, …),
               shared.tsx (Photo, Thumbs, Avatar, StatusDot, FilterTabs, CopyButton), Layout.tsx (sidebar, search, notifications)
  pages/       RequestsPage, OrderPage, BoardPage, ClientsPage, TrackingPage
  index.css    Tailwind + shadcn theme tokens (neutral, dark)
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
| `setProblem`, `addNote` | `PATCH /orders/:id`, `POST /orders/:id/notes` |
| `createOutbound` | `POST /orders/:id/shipments` — creates the Nova Poshta shipment via its API |
| `setTracking` | `POST /shipments/:id/tracking` — registers the number with the tracking aggregator |
| `sendMessage`, `resolveTicket` | `POST /tickets/:id/messages`, `POST /tickets/:id/resolve` |

Real-time updates (new requests, client confirmations, tracking webhooks, ticket messages) should arrive over WebSocket/SSE and be applied as the same actions.
Rule thresholds (`PRICE_TOLERANCE`, `CONFIRM_HOURS` in `rules.ts`) will come from the admin back office.
