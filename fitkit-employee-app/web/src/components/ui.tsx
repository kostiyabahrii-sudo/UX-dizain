import { useEffect, type ReactNode } from 'react';
import { initials } from '../domain/format';
import type { AvatarColor, Item, OrderStatus } from '../domain/types';
import { STATUS_LABEL } from '../domain/rules';

export function Photo({ src, w, h, className = '', style }: { src: string; w: number; h: number; className?: string; style?: React.CSSProperties }) {
  return <img className={`ph ${className}`} src={`/assets/photos/${src}.jpg`} width={w} height={h} style={{ width: w, height: h, ...style }} alt="" loading="lazy" />;
}

export function Thumbs({ items, w = 30, h = 38, max = 3 }: { items: Pick<Item, 'photo' | 'id'>[]; w?: number; h?: number; max?: number }) {
  return (
    <div className="thumbs">
      {items.slice(0, max).map((i, n) => (
        <Photo key={i.id + n} src={i.photo} w={w} h={h} style={n ? { marginLeft: -8 } : undefined} />
      ))}
    </div>
  );
}

export function Avatar({ name, color, size = 32 }: { name: string; color: AvatarColor; size?: number }) {
  return (
    <div className={`ava ${color}`} style={size !== 32 ? { width: size, height: size, fontSize: size * 0.37 } : undefined}>
      {initials(name)}
    </div>
  );
}

const TONE: Record<OrderStatus, string> = {
  new: 'new',
  in_progress: 'wait',
  awaiting: 'wait',
  purchased: 'new',
  shipped: 'ok',
  delivered: 'ok',
  cancelled: '',
};

export function StatusPill({ status, overdue }: { status: OrderStatus; overdue?: boolean }) {
  if (overdue) return <span className="st bad">Прострочено</span>;
  return <span className={`st ${TONE[status]}`}>{STATUS_LABEL[status]}</span>;
}

export function Pill({ tone = '', children }: { tone?: '' | 'new' | 'wait' | 'bad' | 'ok'; children: ReactNode }) {
  return <span className={`st ${tone}`}>{children}</span>;
}

export interface TabDef<K extends string> {
  key: K;
  label: string;
  count?: number;
  red?: boolean;
}

export function Tabs<K extends string>({ tabs, value, onChange }: { tabs: TabDef<K>[]; value: K; onChange: (k: K) => void }) {
  return (
    <div className="tabs" role="tablist">
      {tabs.map((t) => (
        <button key={t.key} role="tab" aria-selected={t.key === value} className={`${t.key === value ? 'on' : ''} ${t.red ? 'red' : ''}`} onClick={() => onChange(t.key)}>
          {t.label}
          {t.count != null && <b>{t.count.toLocaleString('uk-UA')}</b>}
        </button>
      ))}
    </div>
  );
}

export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  useEffect(() => {
    const k = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onClose]);
  return (
    <div className="modal-bg" onMouseDown={onClose}>
      <div className="modal card" onMouseDown={(e) => e.stopPropagation()} role="dialog" aria-label={title}>
        <div className="hd">
          <h2 className="grow">{title}</h2>
        </div>
        <div className="bd">{children}</div>
      </div>
    </div>
  );
}

export function Empty({ children }: { children: ReactNode }) {
  return <div className="empty">{children}</div>;
}
