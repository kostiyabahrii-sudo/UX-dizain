import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Icon } from '../components/Icon';
import { Avatar, Empty, StatusPill, Tabs, Thumbs } from '../components/ui';
import { QUICK_REPLIES } from '../data/mock';
import { clock, dayLabel } from '../domain/format';
import { clientStatus } from '../domain/rules';
import { useLookups, useStore } from '../store/AppStore';

export function ClientsPage() {
  const { state, dispatch, now, toast } = useStore();
  const { client, order } = useLookups();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const [tab, setTab] = useState<'all' | 'open'>('open');
  const [q, setQ] = useState('');
  const [text, setText] = useState('');
  const [revealed, setRevealed] = useState(false);
  const msgsRef = useRef<HTMLDivElement>(null);

  const openCount = state.tickets.filter((t) => t.status === 'open').length;

  /** One row per client: latest ticket if any, else the latest order. */
  const rows = useMemo(() => {
    return state.clients
      .map((c) => {
        const ts = state.tickets.filter((t) => t.clientId === c.id).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
        return { c, ticket: ts.find((t) => t.status === 'open') ?? ts[0] };
      })
      .filter((r) => (tab === 'all' ? true : r.ticket?.status === 'open'))
      .filter((r) => r.c.name.toLowerCase().includes(q.toLowerCase()))
      .sort((a, b) => (b.ticket?.updatedAt ?? '').localeCompare(a.ticket?.updatedAt ?? ''));
  }, [state.clients, state.tickets, tab, q]);

  const selectedId = params.get('client') ?? rows[0]?.c.id;
  const sel = selectedId ? client(selectedId) : undefined;
  const selTickets = state.tickets.filter((t) => t.clientId === selectedId).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
  const ticket = selTickets.find((t) => t.status === 'open') ?? selTickets[0];
  const tOrder = ticket ? order(ticket.orderId) : undefined;
  const clientOrders = state.orders.filter((o) => o.clientId === selectedId).sort((a, b) => b.createdAt.localeCompare(a.createdAt));

  useEffect(() => {
    msgsRef.current?.scrollTo({ top: msgsRef.current.scrollHeight });
  }, [ticket?.messages.length, selectedId]);
  useEffect(() => setRevealed(false), [selectedId]);

  function send() {
    if (!ticket || !text.trim()) return;
    dispatch({ type: 'sendMessage', ticketId: ticket.id, text: text.trim() });
    setText('');
  }

  return (
    <div className="wrap">
      <div className="list">
        <div className="hd2">
          <h1>Clients</h1>
        </div>
        <input className="s2" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Find a client…" />
        <div style={{ padding: '0 14px 10px' }}>
          <Tabs value={tab} onChange={setTab} tabs={[{ key: 'all', label: 'All' }, { key: 'open', label: 'Open tickets', count: openCount }]} />
        </div>
        <div className="scroll">
          {rows.length === 0 && <Empty>No open tickets 🎉</Empty>}
          {rows.map(({ c, ticket: t }) => {
            const o = t ? order(t.orderId) : undefined;
            return (
              <button key={c.id} className={`c ${c.id === selectedId ? 'on' : ''}`} onClick={() => setParams({ client: c.id })}>
                <Avatar name={c.name} color={c.color} />
                <div className="t">
                  <b>
                    {c.name}
                    <small>{t ? (t.status === 'open' ? clock(t.updatedAt) : dayLabel(t.updatedAt, now).split(',')[0]) : ''}</small>
                  </b>
                  <p>
                    {o && <span style={{ color: 'var(--clay)' }}>{o.number}</span>}
                    {t ? ` · ${t.summary}` : ' · no tickets'}
                  </p>
                </div>
                {t?.status === 'open' && t.messages.at(-1)?.from === 'client' && (
                  <span className="badge" style={{ alignSelf: 'center' }}>
                    1
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <div className="chat">
        {!sel || !ticket ? (
          <Empty>{sel ? `${sel.name} has no support tickets.` : 'Select a client.'}</Empty>
        ) : (
          <>
            <div className="head">
              <div className="grow">
                <b>
                  Support ticket · {sel.name} {ticket.status === 'resolved' && <span className="st ok">Resolved</span>}
                </b>
                {tOrder && (
                  <div className="sub">
                    Order {tOrder.number} · client sees “{clientStatus(tOrder.status, tOrder)}”
                  </div>
                )}
              </div>
              {tOrder && (
                <button className="btn" onClick={() => navigate(`/orders/${tOrder.id}`)}>
                  Open order
                </button>
              )}
              {ticket.status === 'open' && (
                <button
                  className="btn pri"
                  onClick={() => {
                    dispatch({ type: 'resolveTicket', ticketId: ticket.id });
                    toast('Ticket resolved');
                  }}
                >
                  Resolve
                </button>
              )}
            </div>
            <div className="msgs" ref={msgsRef}>
              {ticket.messages.map((m) =>
                m.from === 'system' ? (
                  <div key={m.id} className="sys">
                    {m.text}
                  </div>
                ) : (
                  <div key={m.id} className={`m ${m.from === 'client' ? 'cl' : 'me'}`}>
                    {m.text}
                    <small>
                      {m.from === 'client' ? sel.name.split(' ')[0] : 'Fitkit Support'} · {dayLabel(m.at, now)}
                    </small>
                  </div>
                ),
              )}
            </div>
            {ticket.status === 'open' && (
              <>
                <div className="quick">
                  {Object.entries(QUICK_REPLIES).map(([k, v]) => (
                    <button key={k} onClick={() => setText(v)}>
                      {k}
                    </button>
                  ))}
                </div>
                <form
                  className="composer"
                  onSubmit={(e) => {
                    e.preventDefault();
                    send();
                  }}
                >
                  <textarea
                    className="in"
                    value={text}
                    rows={1}
                    onChange={(e) => setText(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        send();
                      }
                    }}
                    placeholder="Reply as Fitkit Support…"
                  />
                  <button className="btn pri" style={{ height: 42 }} disabled={!text.trim()}>
                    <Icon name="send" />
                    Send
                  </button>
                </form>
              </>
            )}
          </>
        )}
      </div>

      {sel && (
        <div className="info">
          <div>
            <div className="lbl">Contacts</div>
            {sel.telegram && (
              <div className="kv2">
                <span>Telegram</span>
                {sel.telegram}
              </div>
            )}
            <div className="kv2">
              <span>Phone</span>
              {revealed ? sel.phoneMasked.replace('•••', '555') : sel.phoneMasked}{' '}
              {!revealed && (
                <button className="btn link" onClick={() => setRevealed(true)} title="Every reveal is logged">
                  Show
                </button>
              )}
            </div>
          </div>
          <div>
            <div className="lbl">Address</div>
            <div style={{ fontSize: 13.5 }}>{sel.address}</div>
            <div className="sub">{sel.delivery}</div>
          </div>
          <div>
            <div className="lbl">Preferences</div>
            <div className="kv2">
              <span>Sizes</span>
              {sel.sizes}
            </div>
            <div className="kv2">
              <span>Stores</span>
              {sel.stores}
            </div>
            {sel.dislikes && (
              <div className="kv2">
                <span>Dislikes</span>
                <em style={{ color: 'var(--bad)', fontStyle: 'normal' }}>{sel.dislikes}</em>
              </div>
            )}
            {sel.note && (
              <div className="sub" style={{ marginTop: 6, fontSize: 12.5 }}>
                {sel.note}
              </div>
            )}
          </div>
          <div>
            <div className="lbl">Orders · {clientOrders.length}</div>
            {clientOrders.slice(0, 5).map((o) => (
              <button key={o.id} className="ord" onClick={() => navigate(`/orders/${o.id}`)}>
                <Thumbs items={o.items} w={24} h={30} max={2} />
                <span className="num">{o.number}</span>
                <span className="grow" />
                <StatusPill status={o.status} />
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
