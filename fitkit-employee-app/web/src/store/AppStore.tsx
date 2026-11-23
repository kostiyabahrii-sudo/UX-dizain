import { createContext, useCallback, useContext, useEffect, useMemo, useReducer, useState, type ReactNode } from 'react';
import * as mock from '../data/mock';
import { canMarkPurchased, STATUS_LABEL } from '../domain/rules';
import type { Client, Employee, Id, Item, Message, Order, OrderStatus, Shipment, Ticket } from '../domain/types';

/**
 * Client-side store for the mock phase. Each action maps 1:1 to a future API call
 * (see README → “API to implement”), so swapping the reducer for fetch calls is local.
 */
export interface State {
  me: Id;
  employees: Employee[];
  clients: Client[];
  orders: Order[];
  shipments: Shipment[];
  tickets: Ticket[];
}

export type Action =
  | { type: 'take'; orderId: Id }
  | { type: 'setStatus'; orderId: Id; status: OrderStatus }
  | { type: 'itemCheck'; orderId: Id; itemId: Id }
  | { type: 'itemSoldOut'; orderId: Id; itemId: Id }
  | { type: 'itemCancel'; orderId: Id; itemId: Id }
  | { type: 'itemStorePrice'; orderId: Id; itemId: Id; price: number }
  | { type: 'itemSendConfirm'; orderId: Id; itemId: Id }
  | { type: 'itemClientConfirmed'; orderId: Id; itemId: Id }
  | { type: 'setProblem'; orderId: Id; problem?: string }
  | { type: 'handOver'; orderId: Id; to: Id }
  | { type: 'cancelOrder'; orderId: Id }
  | { type: 'addNote'; orderId: Id; text: string }
  | { type: 'createOutbound'; orderId: Id }
  | { type: 'setTracking'; shipmentId: Id; carrier: string; tracking: string }
  | { type: 'sendMessage'; ticketId: Id; text: string }
  | { type: 'resolveTicket'; ticketId: Id };

const nowIso = () => new Date().toISOString();
let uid = 1000;
const nextId = (p: string) => `${p}${++uid}`;

function meName(s: State) {
  return s.employees.find((e) => e.id === s.me)?.name ?? 'Me';
}

function patchOrder(s: State, id: Id, fn: (o: Order) => Order, what?: string): State {
  return {
    ...s,
    orders: s.orders.map((o) => {
      if (o.id !== id) return o;
      const next = fn(o);
      return what ? { ...next, history: [...next.history, { at: nowIso(), who: meName(s), what }] } : next;
    }),
  };
}

function patchItem(s: State, orderId: Id, itemId: Id, fn: (i: Item) => Item, what: (i: Item) => string): State {
  const item = s.orders.find((o) => o.id === orderId)?.items.find((i) => i.id === itemId);
  if (!item) return s;
  return patchOrder(s, orderId, (o) => syncOrder({ ...o, items: o.items.map((i) => (i.id === itemId ? fn(i) : i)) }), what(item));
}

/** Keep the order status and red flag in line with its items. */
function syncOrder(o: Order): Order {
  const awaiting = o.items.some((i) => i.status === 'awaiting');
  let status = o.status;
  if (awaiting && (status === 'in_progress' || status === 'new')) status = 'awaiting';
  if (!awaiting && status === 'awaiting') status = 'in_progress';
  const soldOut = o.items.find((i) => i.status === 'sold_out');
  const problem = soldOut ? `${soldOut.name} sold out — apply rule` : o.problem?.includes('sold out') ? undefined : o.problem;
  return { ...o, status, problem };
}

export function reducer(s: State, a: Action): State {
  switch (a.type) {
    case 'take':
      return patchOrder(s, a.orderId, (o) => ({ ...o, ownerId: s.me, status: o.status === 'new' ? 'in_progress' : o.status }), 'Took the request');
    case 'setStatus': {
      let next = patchOrder(
        s,
        a.orderId,
        (o) => ({
          ...o,
          status: a.status,
          items: a.status === 'purchased' ? o.items.map((i) => (i.status === 'cancelled' ? i : { ...i, status: 'bought' as const })) : o.items,
          location: a.status === 'purchased' ? 'Waiting for store tracking' : o.location,
        }),
        `Status → ${STATUS_LABEL[a.status]}`,
      );
      if (a.status === 'purchased') {
        const o = next.orders.find((x) => x.id === a.orderId)!;
        const stores = [...new Set(o.items.filter((i) => i.status === 'bought').map((i) => i.store))];
        const fresh: Shipment[] = stores
          .filter((store) => !s.shipments.some((sh) => sh.orderId === o.id && sh.leg === 'in' && sh.store === store))
          .map((store) => ({ id: nextId('s'), orderId: o.id, leg: 'in', store, events: [{ at: nowIso(), title: `Purchased at ${store}` }] }));
        next = { ...next, shipments: [...next.shipments, ...fresh] };
      }
      return next;
    }
    case 'itemCheck':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, status: 'checked' }), (i) => `${i.name}: checked`);
    case 'itemSoldOut':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, status: 'sold_out' }), (i) => `${i.name}: marked sold out`);
    case 'itemCancel':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, status: 'cancelled' }), (i) => `${i.name}: cancelled, ₴${((i.price ?? 0) * i.qty).toLocaleString('en-US')} refunded`);
    case 'itemStorePrice':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, storePrice: a.price, status: i.status === 'pending' ? 'checked' : i.status }), (i) => `${i.name}: store price ₴${a.price.toLocaleString('en-US')}`);
    case 'itemSendConfirm':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, status: 'awaiting' }), (i) => `${i.name}: price confirmation sent to client`);
    case 'itemClientConfirmed':
      return patchItem(s, a.orderId, a.itemId, (i) => ({ ...i, status: 'checked', price: i.storePrice ?? i.price }), (i) => `${i.name}: client confirmed the new price`);
    case 'setProblem':
      return patchOrder(s, a.orderId, (o) => ({ ...o, problem: a.problem }), a.problem ? `Problem: ${a.problem}` : 'Problem cleared');
    case 'handOver': {
      const to = s.employees.find((e) => e.id === a.to)?.name ?? a.to;
      return patchOrder(s, a.orderId, (o) => ({ ...o, ownerId: a.to }), `Handed over to ${to}`);
    }
    case 'cancelOrder':
      return patchOrder(s, a.orderId, (o) => ({ ...o, status: 'cancelled', items: o.items.map((i) => ({ ...i, status: 'cancelled' as const })) }), 'Order cancelled, full refund');
    case 'addNote':
      return patchOrder(s, a.orderId, (o) => ({ ...o, notes: [...o.notes, { id: nextId('n'), author: meName(s), at: nowIso(), text: a.text }] }));
    case 'createOutbound': {
      const tracking = `2045 ${String(Math.floor(Math.random() * 1e4)).padStart(4, '0')} ${String(Math.floor(Math.random() * 1e4)).padStart(4, '0')} ${String(Math.floor(Math.random() * 100)).padStart(2, '0')}`;
      const sh: Shipment = { id: nextId('s'), orderId: a.orderId, leg: 'out', carrier: 'Nova Poshta', tracking, source: 'api', events: [{ at: nowIso(), title: 'Shipment created', detail: 'Nova Poshta API' }] };
      const next = patchOrder(s, a.orderId, (o) => ({ ...o, status: 'shipped', location: `Nova Poshta · ${tracking}` }), `Shipped · Nova Poshta ${tracking}`);
      return { ...next, shipments: [...next.shipments, sh] };
    }
    case 'setTracking':
      return {
        ...s,
        shipments: s.shipments.map((sh) =>
          sh.id === a.shipmentId
            ? { ...sh, carrier: a.carrier, tracking: a.tracking, source: 'manual', problem: undefined, events: [...sh.events, { at: nowIso(), title: `Tracking added · ${a.carrier}`, detail: 'entered by buyer' }] }
            : sh,
        ),
      };
    case 'sendMessage': {
      const m: Message = { id: nextId('m'), from: 'support', text: a.text, at: nowIso() };
      return { ...s, tickets: s.tickets.map((t) => (t.id === a.ticketId ? { ...t, messages: [...t.messages, m], updatedAt: m.at } : t)) };
    }
    case 'resolveTicket':
      return { ...s, tickets: s.tickets.map((t) => (t.id === a.ticketId ? { ...t, status: 'resolved', summary: 'Resolved · ' + t.summary, updatedAt: nowIso() } : t)) };
  }
}

interface Ctx {
  state: State;
  dispatch: (a: Action) => void;
  now: number;
  toast: (text: string, tone?: 'ok' | 'bad') => void;
  /** Guarded status change used by the card and the board. Returns false if refused. */
  moveOrder: (orderId: Id, status: OrderStatus) => boolean;
}

const StoreCtx = createContext<Ctx | null>(null);

export function AppStoreProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    me: mock.ME,
    employees: mock.employees,
    clients: mock.clients,
    orders: mock.orders,
    shipments: mock.shipments,
    tickets: mock.tickets,
  });
  const [now, setNow] = useState(Date.now());
  const [toasts, setToasts] = useState<{ id: number; text: string; tone: 'ok' | 'bad' }[]>([]);

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 30_000);
    return () => clearInterval(t);
  }, []);

  const toast = useCallback((text: string, tone: 'ok' | 'bad' = 'ok') => {
    const id = Date.now() + Math.random();
    setToasts((ts) => [...ts, { id, text, tone }]);
    setTimeout(() => setToasts((ts) => ts.filter((x) => x.id !== id)), 3200);
  }, []);

  const moveOrder = useCallback(
    (orderId: Id, status: OrderStatus) => {
      const o = state.orders.find((x) => x.id === orderId);
      if (!o || o.status === status) return false;
      if (status === 'purchased' && !canMarkPurchased(o)) {
        toast('Resolve every item first: check it, apply a rule or cancel it.', 'bad');
        return false;
      }
      if (status === 'awaiting' && !o.items.some((i) => i.status === 'awaiting')) {
        toast('Send a price confirmation from the request card first.', 'bad');
        return false;
      }
      if (status === 'shipped') {
        if (o.status !== 'purchased') {
          toast('Only purchased orders can be shipped.', 'bad');
          return false;
        }
        dispatch({ type: 'createOutbound', orderId });
        toast(`${o.number} shipped · Nova Poshta shipment created`);
        return true;
      }
      dispatch({ type: 'setStatus', orderId, status });
      toast(`${o.number} → ${STATUS_LABEL[status]}`);
      return true;
    },
    [state.orders, toast],
  );

  const value = useMemo(() => ({ state, dispatch, now, toast, moveOrder }), [state, now, toast, moveOrder]);
  return (
    <StoreCtx.Provider value={value}>
      {children}
      <div className="toasts">
        {toasts.map((t) => (
          <div key={t.id} className={`toast ${t.tone}`}>
            {t.text}
          </div>
        ))}
      </div>
    </StoreCtx.Provider>
  );
}

export function useStore() {
  const c = useContext(StoreCtx);
  if (!c) throw new Error('useStore outside AppStoreProvider');
  return c;
}

/** Lookup helpers */
export function useLookups() {
  const { state } = useStore();
  return useMemo(
    () => ({
      client: (id: Id) => state.clients.find((c) => c.id === id)!,
      employee: (id?: Id) => state.employees.find((e) => e.id === id),
      order: (id: Id) => state.orders.find((o) => o.id === id),
      orderByNumber: (num: string) => state.orders.find((o) => o.number === num),
    }),
    [state],
  );
}
