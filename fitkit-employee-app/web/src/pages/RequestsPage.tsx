import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Avatar, Empty, StatusPill, Tabs, Thumbs } from '../components/ui';
import { timeLeft, uah } from '../domain/format';
import { useLookups, useStore } from '../store/AppStore';

type Tab = 'all' | 'new' | 'overdue';

export function RequestsPage() {
  const { state, dispatch, now, toast } = useStore();
  const { client } = useLookups();
  const navigate = useNavigate();
  const [tab, setTab] = useState<Tab>('all');

  const requests = useMemo(
    () => state.orders.filter((o) => o.status === 'new').sort((a, b) => a.dueAt.localeCompare(b.dueAt)),
    [state.orders],
  );
  const isLate = (dueAt: string) => new Date(dueAt).getTime() < now;
  const overdue = requests.filter((o) => isLate(o.dueAt));
  const fresh = requests.filter((o) => !isLate(o.dueAt));
  const rows = tab === 'overdue' ? overdue : tab === 'new' ? fresh : requests;

  function takeNext() {
    const next = [...requests].sort((a, b) => a.createdAt.localeCompare(b.createdAt))[0];
    if (!next) return toast('No requests in the queue', 'bad');
    dispatch({ type: 'take', orderId: next.id });
    toast(`${next.number} is yours`);
    navigate(`/orders/${next.id}`);
  }

  return (
    <>
      <div className="row">
        <h1 className="grow">
          Requests <span className="cnt">{requests.length}</span>
        </h1>
        <button className="btn pri big" onClick={takeNext} disabled={!requests.length}>
          Take next request
        </button>
      </div>
      <Tabs
        value={tab}
        onChange={setTab}
        tabs={[
          { key: 'all', label: 'All', count: requests.length },
          { key: 'new', label: 'New', count: fresh.length },
          { key: 'overdue', label: 'Overdue', count: overdue.length, red: overdue.length > 0 },
        ]}
      />
      <div className="card" style={{ overflow: 'hidden' }}>
        {rows.length === 0 ? (
          <Empty>Nothing here — the queue is clear.</Empty>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Request</th>
                <th>Client</th>
                <th>Stores</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Due</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((o) => {
                const c = client(o.clientId);
                const late = isLate(o.dueAt);
                const t = timeLeft(o.dueAt, now);
                const stores = [...new Set(o.items.map((i) => i.store))].join(', ');
                return (
                  <tr key={o.id} className={`click ${late ? 'late' : ''}`} onClick={() => navigate(`/orders/${o.id}`)}>
                    <td>
                      <div className="row" style={{ gap: 14 }}>
                        <div style={{ width: 82 }}>
                          <Thumbs items={o.items} w={32} h={40} />
                        </div>
                        <div>
                          <div className="num" style={{ fontSize: 16 }}>
                            {o.number}
                          </div>
                          <div className="sub" style={{ fontSize: 12 }}>
                            {o.items.length} item{o.items.length > 1 ? 's' : ''}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="who">
                        <Avatar name={c.name} color={c.color} size={30} />
                        {c.name}
                      </div>
                    </td>
                    <td className="sub">{stores}</td>
                    <td>{o.paid != null ? uah(o.paid) : <span className="sub">price not set</span>}</td>
                    <td>
                      <StatusPill status={o.status} overdue={late} />
                    </td>
                    <td>
                      <span className={`timer ${t.tone}`}>{t.text}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
