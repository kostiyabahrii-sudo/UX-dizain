import { useState, type FormEvent } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { Icon, type IconName } from './Icon';
import { Avatar } from './ui';
import { useStore } from '../store/AppStore';

export function Layout() {
  const { state, now, toast } = useStore();
  const navigate = useNavigate();
  const [q, setQ] = useState('');
  const me = state.employees.find((e) => e.id === state.me)!;

  const newReq = state.orders.filter((o) => o.status === 'new');
  const overdue = newReq.some((o) => new Date(o.dueAt).getTime() < now);
  const mine = state.orders.filter((o) => o.ownerId === state.me && ['in_progress', 'awaiting', 'purchased', 'shipped'].includes(o.status));
  const openTickets = state.tickets.filter((t) => t.status === 'open').length;
  const trackProblems = state.shipments.filter((s) => s.problem).length;

  const nav: { to: string; icon: IconName; label: string; n: number; red: boolean }[] = [
    { to: '/requests', icon: 'inbox', label: 'Requests', n: newReq.length, red: overdue },
    { to: '/orders', icon: 'bag', label: 'Current orders', n: mine.length, red: false },
    { to: '/clients', icon: 'users', label: 'Clients', n: openTickets, red: openTickets > 0 },
    { to: '/tracking', icon: 'truck', label: 'Tracking', n: trackProblems, red: trackProblems > 0 },
  ];

  function search(e: FormEvent) {
    e.preventDefault();
    const s = q.trim().toLowerCase().replace(/\s+/g, ' ');
    if (!s) return;
    const num = s.startsWith('#') ? s : '#' + s;
    const byNum = state.orders.find((o) => o.number.toLowerCase() === num);
    const byClient = state.clients.find((c) => c.name.toLowerCase().includes(s) || c.phoneMasked.replace(/\D/g, '').endsWith(s.replace(/\D/g, '') || 'x'));
    const byTrack = state.shipments.find((sh) => sh.tracking?.toLowerCase().replace(/\s/g, '').includes(s.replace(/\s/g, '')));
    if (byNum) navigate(`/orders/${byNum.id}`);
    else if (byTrack) navigate(`/tracking?order=${byTrack.orderId}`);
    else if (byClient) navigate(`/clients?client=${byClient.id}`);
    else return toast(`Nothing found for “${q}”`, 'bad');
    setQ('');
  }

  return (
    <div className="app">
      <aside className="side">
        <div className="logo">
          <img src="/assets/logo-mark.png" alt="" />
          <b>Fitkit</b>
        </div>
        <nav className="nav">
          {nav.map((n) => (
            <NavLink key={n.to} to={n.to} className={({ isActive }) => (isActive ? 'on' : '')}>
              <Icon name={n.icon} size={17} />
              {n.label}
              {n.n > 0 && <span className={`n ${n.red ? 'red' : ''}`}>{n.n}</span>}
            </NavLink>
          ))}
        </nav>
        <div className="me">
          <Avatar name={me.name} color={me.color} />
          <div>
            {me.name}
            <small>Buyer</small>
          </div>
        </div>
      </aside>
      <div className="body">
        <header className="top">
          <form className="search" onSubmit={search}>
            <Icon name="search" size={14} />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search request #, client, phone or tracking…" aria-label="Search" />
          </form>
          <button className="bell" aria-label="Notifications" onClick={() => navigate('/clients')}>
            <Icon name="bell" size={18} />
            {openTickets > 0 && <i />}
          </button>
        </header>
        <main className="main">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
