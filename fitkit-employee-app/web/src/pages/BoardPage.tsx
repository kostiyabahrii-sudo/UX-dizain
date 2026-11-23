import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tabs, Thumbs } from '../components/ui';
import { timeLeft, uah } from '../domain/format';
import type { Order, OrderStatus } from '../domain/types';
import { useLookups, useStore } from '../store/AppStore';

const COLS: { status: OrderStatus; label: string; color: string }[] = [
  { status: 'in_progress', label: 'In progress', color: 'var(--muted)' },
  { status: 'awaiting', label: 'Awaiting confirmation', color: 'var(--wait)' },
  { status: 'purchased', label: 'Purchased', color: 'var(--info)' },
  { status: 'shipped', label: 'Shipped', color: 'var(--ok)' },
];

function note(o: Order): { tone: 'red' | 'org'; text: string } | null {
  if (o.problem) return { tone: 'red', text: o.problem };
  const a = o.items.find((i) => i.status === 'awaiting');
  if (a && a.price && a.storePrice) {
    const pct = Math.round(((a.storePrice - a.price) / a.price) * 100);
    return { tone: 'org', text: `Price +${pct}% — confirmation sent` };
  }
  return null;
}

export function BoardPage() {
  const { state, now, moveOrder } = useStore();
  const { client } = useLookups();
  const navigate = useNavigate();
  const [scope, setScope] = useState<'mine' | 'all'>('mine');
  const [drag, setDrag] = useState<string | null>(null);
  const [over, setOver] = useState<OrderStatus | null>(null);

  const list = state.orders.filter((o) => COLS.some((c) => c.status === o.status) && (scope === 'all' || o.ownerId === state.me));

  return (
    <>
      <div className="row">
        <h1 className="grow">
          Current orders <span className="cnt">{list.length}</span>
        </h1>
        <Tabs value={scope} onChange={setScope} tabs={[{ key: 'mine', label: 'Mine' }, { key: 'all', label: 'All' }]} />
      </div>
      <div className="board">
        {COLS.map((col) => {
          const cards = list.filter((o) => o.status === col.status).sort((a, b) => Number(!!b.problem) - Number(!!a.problem) || a.dueAt.localeCompare(b.dueAt));
          return (
            <div
              key={col.status}
              className={`col ${over === col.status ? 'over' : ''}`}
              onDragOver={(e) => {
                e.preventDefault();
                setOver(col.status);
              }}
              onDragLeave={() => setOver(null)}
              onDrop={(e) => {
                e.preventDefault();
                setOver(null);
                if (drag) moveOrder(drag, col.status);
                setDrag(null);
              }}
            >
              <div className="colh">
                <span className="dot" style={{ background: col.color }} />
                {col.label} <b>{cards.length}</b>
              </div>
              {cards.map((o) => {
                const c = client(o.clientId);
                const n = note(o);
                const t = timeLeft(o.dueAt, now);
                const info = o.status === 'purchased' || o.status === 'shipped' ? o.location ?? '' : `${o.items.length} item${o.items.length > 1 ? 's' : ''} · ${o.paid != null ? uah(o.paid) : 'price not set'}`;
                return (
                  <div
                    key={o.id}
                    className={`oc ${n?.tone === 'red' ? 'prob' : n ? 'wt' : ''} ${drag === o.id ? 'dragging' : ''}`}
                    draggable
                    onDragStart={() => setDrag(o.id)}
                    onDragEnd={() => setDrag(null)}
                    onClick={() => navigate(`/orders/${o.id}`)}
                  >
                    <div className="row" style={{ gap: 10 }}>
                      <Thumbs items={o.items} />
                      <span className="num" style={{ fontSize: 16 }}>
                        {o.number}
                      </span>
                      <span className={`t ${t.tone === 'red' ? 'red' : n?.tone === 'org' ? 'org' : ''}`}>{t.text.replace(' left', '')}</span>
                    </div>
                    <div>
                      <div style={{ fontSize: 13.5 }}>{c.name}</div>
                      <div className="sub" style={{ fontSize: 12.5 }}>
                        {info}
                      </div>
                    </div>
                    {n && <div className={`note ${n.tone}`}>{n.text}</div>}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    </>
  );
}
