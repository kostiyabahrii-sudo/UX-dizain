import { useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Empty, Modal, Photo, Tabs, Thumbs } from '../components/ui';
import { dayLabel, shortDate } from '../domain/format';
import { clientStatus } from '../domain/rules';
import type { Shipment } from '../domain/types';
import { useLookups, useStore } from '../store/AppStore';

type Tab = 'all' | 'in' | 'warehouse' | 'out' | 'problems';
const SOURCE = { email: 'from store email', manual: 'entered by buyer', api: 'created via Nova Poshta API' } as const;

export function TrackingPage() {
  const { state, now, moveOrder } = useStore();
  const { client, order } = useLookups();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const [tab, setTab] = useState<Tab>('all');
  const [edit, setEdit] = useState<Shipment | null>(null);

  const all = useMemo(() => [...state.shipments].sort((a, b) => Number(!!b.problem) - Number(!!a.problem) || (b.events.at(-1)?.at ?? '').localeCompare(a.events.at(-1)?.at ?? '')), [state.shipments]);
  const filt: Record<Tab, (s: Shipment) => boolean> = {
    all: () => true,
    in: (s) => s.leg === 'in' && !s.atWarehouse,
    warehouse: (s) => s.leg === 'in' && !!s.atWarehouse && order(s.orderId)?.status === 'purchased',
    out: (s) => s.leg === 'out',
    problems: (s) => !!s.problem,
  };
  const rows = all.filter(filt[tab]);
  const count = (t: Tab) => all.filter(filt[t]).length;

  const selOrderId = params.get('order') ?? rows[0]?.orderId;
  const selOrder = selOrderId ? order(selOrderId) : undefined;
  const legIn = state.shipments.filter((s) => s.orderId === selOrderId && s.leg === 'in');
  const legOut = state.shipments.find((s) => s.orderId === selOrderId && s.leg === 'out');
  const ready = selOrder?.status === 'purchased' && legIn.length > 0 && legIn.every((s) => s.atWarehouse);

  return (
    <>
      <h1>
        Tracking <span className="cnt">{all.length}</span>
      </h1>
      <Tabs
        value={tab}
        onChange={setTab}
        tabs={[
          { key: 'all', label: 'All', count: count('all') },
          { key: 'in', label: 'Store → warehouse', count: count('in') },
          { key: 'warehouse', label: 'At warehouse', count: count('warehouse') },
          { key: 'out', label: 'Warehouse → client', count: count('out') },
          { key: 'problems', label: 'Problems', count: count('problems'), red: count('problems') > 0 },
        ]}
      />
      <div className="cols">
        <div className="card grow" style={{ overflow: 'hidden' }}>
          {rows.length === 0 ? (
            <Empty>No parcels here.</Empty>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Leg</th>
                  <th>Carrier · tracking</th>
                  <th>Last event</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((s) => {
                  const o = order(s.orderId)!;
                  const ev = s.events.at(-1);
                  return (
                    <tr key={s.id} className={`click ${s.problem ? 'late' : ''} ${s.orderId === selOrderId ? 'on' : ''}`} onClick={() => setParams({ order: s.orderId })}>
                      <td>
                        <div className="row" style={{ gap: 12 }}>
                          <div style={{ width: 58 }}>
                            <Thumbs items={o.items} w={30} h={38} />
                          </div>
                          <span className="num" style={{ fontSize: 15 }}>
                            {o.number}
                          </span>
                        </div>
                      </td>
                      <td>
                        {s.leg === 'in' ? <span className="leg in">Store → warehouse</span> : <span className="leg out">Warehouse → client</span>}
                        {s.store && <div style={{ marginTop: 4 }}>{s.store}</div>}
                      </td>
                      <td>
                        <div className="track">{s.tracking ? `${s.carrier} · ${s.tracking}` : '— no tracking yet'}</div>
                        <div className="src">{s.source ? SOURCE[s.source] : ''}</div>
                      </td>
                      <td>
                        {s.problem ? <span className="red">{s.problem}</span> : ev?.title}
                        <div className="sub" style={{ fontSize: 12 }}>
                          {ev ? dayLabel(ev.at, now) : ''}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>

        {selOrder && (
          <div className="card panel">
            <div className="bd">
              <div className="row" style={{ gap: 12, marginBottom: 14 }}>
                <Photo src={selOrder.items[0].photo} w={52} h={66} />
                <div className="grow">
                  <button className="btn link num" style={{ fontSize: 17, color: 'var(--text)' }} onClick={() => navigate(`/orders/${selOrder.id}`)}>
                    {selOrder.number}
                  </button>
                  <div style={{ fontSize: 13.5 }}>
                    {selOrder.items[0].name} · {selOrder.items[0].size}
                    {selOrder.items.length > 1 ? ` +${selOrder.items.length - 1}` : ''}
                  </div>
                  <div className="sub">{client(selOrder.clientId).name}</div>
                </div>
              </div>

              <div className="lbl">1 · Store → warehouse</div>
              {legIn.length === 0 && <div className="sub" style={{ marginBottom: 12 }}>Nothing bought yet.</div>}
              {legIn.map((s) => (
                <div key={s.id} className="tl">
                  {s.events.map((e, i) => (
                    <div key={i} className="ev d">
                      <b>{e.title}</b>
                      <small>
                        {e.detail ? `${e.detail} · ` : ''}
                        {dayLabel(e.at, now)}
                      </small>
                    </div>
                  ))}
                  {!s.atWarehouse && (
                    <div className="ev f">
                      <b>{s.problem ?? 'Arrives at warehouse'}</b>
                      <small>
                        {s.tracking ? 'updates from the tracking aggregator' : (
                          <button className="btn link" onClick={() => setEdit(s)}>
                            Add tracking number
                          </button>
                        )}
                      </small>
                    </div>
                  )}
                </div>
              ))}

              <div className="lbl">2 · Warehouse → client</div>
              <div className="tl">
                {legOut ? (
                  legOut.events.map((e, i) => (
                    <div key={i} className="ev d">
                      <b>{e.title}</b>
                      <small>
                        {e.detail ? `${e.detail} · ` : ''}
                        {dayLabel(e.at, now)}
                      </small>
                    </div>
                  ))
                ) : (
                  <div className="ev f">
                    <b>Not shipped yet</b>
                    <small>Nova Poshta shipment is created by the app</small>
                  </div>
                )}
              </div>

              <div className="lbl">Client sees</div>
              <div className="seen">
                “{clientStatus(selOrder.status, selOrder)}”
                {legOut ? ` · Nova Poshta ${legOut.tracking}` : ` · arrives by ${shortDate(new Date(now + 2 * 86_400_000).toISOString())}`}
              </div>
              {selOrder.status === 'purchased' && (
                <button className="btn pri big" style={{ width: '100%' }} disabled={!ready} onClick={() => moveOrder(selOrder.id, 'shipped')} title={ready ? undefined : 'All parcels must arrive at the warehouse first'}>
                  Create shipment & ship →
                </button>
              )}
            </div>
          </div>
        )}
      </div>
      {edit && <TrackingModal shipment={edit} onClose={() => setEdit(null)} />}
    </>
  );
}

function TrackingModal({ shipment, onClose }: { shipment: Shipment; onClose: () => void }) {
  const { dispatch, toast } = useStore();
  const [carrier, setCarrier] = useState('');
  const [tracking, setTracking] = useState('');
  return (
    <Modal title={`Tracking · ${shipment.store ?? ''}`} onClose={onClose}>
      <form
        className="stack"
        onSubmit={(e) => {
          e.preventDefault();
          dispatch({ type: 'setTracking', shipmentId: shipment.id, carrier: carrier.trim() || 'Auto-detect', tracking: tracking.trim() });
          toast('Tracking added — the aggregator will follow it');
          onClose();
        }}
      >
        <input className="input" autoFocus value={tracking} onChange={(e) => setTracking(e.target.value)} placeholder="Tracking number" />
        <input className="input" value={carrier} onChange={(e) => setCarrier(e.target.value)} placeholder="Carrier (optional — detected automatically)" />
        <div className="row" style={{ justifyContent: 'flex-end' }}>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button className="btn pri" disabled={!tracking.trim()}>
            Save
          </button>
        </div>
      </form>
    </Modal>
  );
}
