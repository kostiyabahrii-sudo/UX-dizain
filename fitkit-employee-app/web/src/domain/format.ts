export const uah = (n: number) => '₴' + Math.round(n).toLocaleString('en-US');

export const initials = (name: string) =>
  name
    .split(/\s+/)
    .map((w) => w[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

const MIN = 60_000;

/** “1h 20m left”, “8 min left”, “−42 min” (overdue). */
export function timeLeft(dueAt: string, now: number): { text: string; tone: '' | 'org' | 'red' } {
  const diff = Math.round((new Date(dueAt).getTime() - now) / MIN);
  const fmt = (m: number) => {
    const a = Math.abs(m);
    if (a < 60) return `${a} min`;
    const h = Math.floor(a / 60);
    const r = a % 60;
    if (h >= 24) return `${Math.floor(h / 24)}d ${h % 24}h`;
    return r ? `${h}h ${r}m` : `${h}h`;
  };
  if (diff < 0) return { text: `−${fmt(diff)}`, tone: 'red' };
  return { text: `${fmt(diff)} left`, tone: diff <= 15 ? 'org' : '' };
}

export function clock(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}

export function dayLabel(iso: string, now: number): string {
  const d = new Date(iso);
  const n = new Date(now);
  const sameDay = (a: Date, b: Date) => a.toDateString() === b.toDateString();
  if (sameDay(d, n)) return `today, ${clock(iso)}`;
  const y = new Date(now - 86_400_000);
  if (sameDay(d, y)) return `yesterday, ${clock(iso)}`;
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + ', ' + clock(iso);
}

export function shortDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
