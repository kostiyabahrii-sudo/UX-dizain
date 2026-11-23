import type { Item, Order, OrderStatus } from './types';

/** Price increase Fitkit covers silently. Set in the admin back office. */
export const PRICE_TOLERANCE = 0.05;
/** Hours the client has to confirm a higher price before auto-refund. */
export const CONFIRM_HOURS = 24;

export type RuleKind = 'covered' | 'confirm' | 'sold_out';

export interface RuleResult {
  kind: RuleKind;
  title: string;
  detail: string;
  /** Extra amount Fitkit pays, ₴. */
  covered?: number;
}

const uah = (n: number) => '₴' + n.toLocaleString('en-US');

/** Which rule applies to an item, if any. */
export function ruleFor(item: Item): RuleResult | null {
  if (item.status === 'sold_out') {
    const refund = (item.price ?? 0) * item.qty;
    return {
      kind: 'sold_out',
      title: `Out of stock in ${item.size}`,
      detail: `Rule: cancel the item and refund ${uah(refund)}. The client gets “Item no longer available, money refunded”.`,
    };
  }
  if (item.price != null && item.storePrice != null && item.storePrice > item.price) {
    const diff = (item.storePrice - item.price) * item.qty;
    const pct = (item.storePrice - item.price) / item.price;
    const pctText = `${(pct * 100).toFixed(1).replace(/\.0$/, '')}%`;
    if (pct <= PRICE_TOLERANCE) {
      return {
        kind: 'covered',
        title: `Price up ${uah(diff)} (+${pctText})`,
        detail: `Within the ${PRICE_TOLERANCE * 100}% tolerance — Fitkit covers the difference, the client sees nothing.`,
        covered: diff,
      };
    }
    return {
      kind: 'confirm',
      title: `Price up ${uah(diff)} (+${pctText})`,
      detail:
        item.status === 'awaiting'
          ? `Confirmation sent. No answer in ${CONFIRM_HOURS} h → the item is cancelled and refunded.`
          : `Over ${PRICE_TOLERANCE * 100}% — the client confirms in one tap. No answer in ${CONFIRM_HOURS} h → refund.`,
    };
  }
  return null;
}

/** An item still blocks “Purchased” until it is resolved. */
export function isBlocking(item: Item): boolean {
  if (item.status === 'cancelled' || item.status === 'bought') return false;
  if (item.status === 'pending' || item.status === 'sold_out' || item.status === 'awaiting') return true;
  const r = ruleFor(item);
  return r?.kind === 'confirm';
}

export function canMarkPurchased(order: Order): boolean {
  return order.items.some((i) => i.status !== 'cancelled') && !order.items.some(isBlocking);
}

/** The only status text the client ever sees. */
export function clientStatus(status: OrderStatus, order?: Order): string {
  switch (status) {
    case 'new':
      return 'Order confirmed';
    case 'in_progress':
    case 'purchased':
      return 'Preparing your order';
    case 'awaiting':
      return order?.items.some((i) => i.status === 'awaiting') ? 'Price changed (action)' : 'Preparing your order';
    case 'shipped':
      return 'Shipped';
    case 'delivered':
      return 'Delivered';
    case 'cancelled':
      return 'Cancelled, refunded';
  }
}

export interface Money {
  paid: number;
  refunds: number;
  fee: number;
  covered: number;
  toBuy: number;
  priceKnown: boolean;
}

export function money(order: Order): Money {
  let refunds = 0;
  let covered = 0;
  let toBuy = 0;
  let priceKnown = order.paid != null;
  for (const it of order.items) {
    const line = (it.price ?? 0) * it.qty;
    if (it.price == null) priceKnown = false;
    if (it.status === 'cancelled') {
      refunds += line;
      continue;
    }
    if (it.status === 'sold_out') continue; // can't be bought; refunded once the rule is applied
    const r = ruleFor(it);
    if (r?.kind === 'covered') covered += r.covered ?? 0;
    toBuy += (it.storePrice ?? it.price ?? 0) * it.qty;
  }
  return { paid: order.paid ?? 0, refunds, fee: order.fee, covered, toBuy, priceKnown };
}

export const STATUS_LABEL: Record<OrderStatus, string> = {
  new: 'New',
  in_progress: 'In progress',
  awaiting: 'Awaiting confirmation',
  purchased: 'Purchased',
  shipped: 'Shipped',
  delivered: 'Delivered',
  cancelled: 'Cancelled',
};

/** Next main action for the order card button. */
export function nextStep(status: OrderStatus): { label: string; to: OrderStatus } | null {
  switch (status) {
    case 'new':
      return { label: 'Take request', to: 'in_progress' };
    case 'in_progress':
    case 'awaiting':
      return { label: 'Move to “Purchased” →', to: 'purchased' };
    case 'purchased':
      return { label: 'Create shipment & ship →', to: 'shipped' };
    case 'shipped':
      return { label: 'Mark as delivered', to: 'delivered' };
    default:
      return null;
  }
}
