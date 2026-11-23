import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Icon } from '../components/Icon';
import { Empty, Modal, Photo, Pill, StatusPill } from '../components/ui';
import { clock, dayLabel, shortDate, timeLeft, uah } from '../domain/format';
import { canMarkPurchased, clientStatus, money, nextStep, ruleFor } from '../domain/rules';
import type { Item, ItemStatus, Order } from '../domain/types';
import { useLookups, useStore } from '../store/AppStore';

const ITEM_PILL: Record<ItemStatus, [string, '' | 'new' | 'wait' | 'bad' | 'ok']> = {
  pending: ['Перевірити', ''],
  checked: ['Перевірено', 'ok'],
  sold_out: ['Немає', 'bad'],
  price_up: ['Ціна зросла', 'wait'],
  awaiting: ['Чекаємо клієнта', 'wait'],
  bought: ['Викуплено', 'ok'],
  cancelled: ['Скасовано', ''],
};

export function OrderPage() {
  const { id = '' } = useParams();
  const { state, now, moveOrder, dispatch, toast } = useStore();
  const { client, employee, order: getOrder } = useLookups();
  const navigate = useNavigate();
  const [modal, setModal] = useState<null | 'problem' | 'handover' | 'cancel' | 'history' | { price: Item }>(null);

  const o = getOrder(id);
  if (!o) return <Empty>Замовлення не знайдено. <Link to="/requests">До заявок</Link></Empty>;

  const c = client(o.clientId);
  const owner = employee(o.ownerId);
  const mine = o.ownerId === state.me;
  const m = money(o);
  const t = timeLeft(o.dueAt, now);
  const step = nextStep(o.status);
  const blocked = (o.status === 'in_progress' || o.status === 'awaiting') && !canMarkPurchased(o);
  const editable = o.status === 'new' || o.status === 'in_progress' || o.status === 'awaiting';

  function main() {
    if (!step) return;
    if (o!.status === 'new') {
      dispatch({ type: 'take', orderId: o!.id });
      return toast(`${o!.number} тепер ваша`);
    }
    moveOrder(o!.id, step.to);
  }

  return (
    <>
      <div className="row">
        <button className="btn iconbtn" onClick={() => navigate(-1)} aria-label="Назад">
          <Icon name="back" />
        </button>
        <div className="grow">
          <div className="row" style={{ gap: 10 }}>
            <h1 className="num" style={{ fontSize: 28 }}>
              {o.number}
            </h1>
            <StatusPill status={o.status} />
            {o.problem && <Pill tone="bad">{o.problem}</Pill>}
          </div>
          <div className="sub">
            {c.name} · отримано {shortDate(o.createdAt)}, {clock(o.createdAt)} ·{' '}
            <button className="btn link" onClick={() => setModal('history')}>
              Історія
            </button>
          </div>
        </div>
      </div>

      <div className="cols">
        <div className="left">
          <div className="card">
            {o.items.map((it) => (
              <ItemRow key={it.id} order={o} item={it} editable={editable && (mine || o.status === 'new')} onPrice={() => setModal({ price: it })} />
            ))}
          </div>
          <div className="card">
            <div className="bd row" style={{ gap: 30, alignItems: 'flex-start' }}>
              <div>
                <div className="lbl">Доставка</div>
                {c.address}
                <div className="sub">
                  {c.name} · {c.phoneMasked} · {c.delivery}
                </div>
              </div>
              <span className="grow" />
              <button
                className="btn link"
                onClick={() => {
                  navigator.clipboard?.writeText(`${c.name}, ${c.address}`);
                  toast('Адресу скопійовано');
                }}
              >
                <Icon name="copy" size={14} /> Копіювати
              </button>
            </div>
          </div>
        </div>

        <div className="right">
          <div className="card">
            <div className="bd">
              <div className="kv">
                <span>Відповідальний</span>
                {owner?.name ?? '—'}
              </div>
              <div className="kv">
                <span>Термін</span>
                <span className={`timer ${t.tone || 'org'}`}>{t.text}</span>
              </div>
              <div className="kv">
                <span>Клієнт бачить</span>
                {clientStatus(o.status, o)}
              </div>
              <div className="kv" style={{ marginTop: 8 }}>
                <span>Клієнт сплатив</span>
                {m.priceKnown ? uah(m.paid) : '—'}
              </div>
              {m.refunds > 0 && (
                <div className="kv">
                  <span>Повернення</span>−{uah(m.refunds)}
                </div>
              )}
              <div className="kv">
                <span>Комісія Fitkit</span>
                {uah(m.fee)}
              </div>
              {m.covered > 0 && (
                <div className="kv">
                  <span>Fitkit доплачує</span>
                  {uah(m.covered)}
                </div>
              )}
              <div className="kv total">
                <span style={{ color: 'var(--text)' }}>До викупу</span>
                <span className="num">{m.toBuy ? uah(m.toBuy) : '—'}</span>
              </div>

              {step && (o.status === 'new' || mine) && (
                <button className="btn pri big" style={{ width: '100%', marginTop: 16 }} onClick={main} disabled={blocked} title={blocked ? 'Спершу розберіть кожен товар' : undefined}>
                  {step.label}
                </button>
              )}
              {blocked && <div className="hint">Щоб продовжити, розберіть кожен товар.</div>}
              {o.status !== 'new' && o.status !== 'cancelled' && o.status !== 'delivered' && (
                <div className="row" style={{ gap: 8, marginTop: 8 }}>
                  <button className={`btn ${o.problem ? 'danger' : ''}`} style={{ flex: 1 }} onClick={() => setModal('problem')}>
                    {o.problem ? 'Проблема ✓' : 'Проблема'}
                  </button>
                  <button className="btn" style={{ flex: 1 }} onClick={() => setModal('handover')}>
                    Передати
                  </button>
                </div>
              )}
              {editable && (
                <div style={{ textAlign: 'center', marginTop: 12 }}>
                  <button className="btn link quiet" onClick={() => setModal('cancel')}>
                    Скасувати замовлення
                  </button>
                </div>
              )}
            </div>
          </div>
          <Notes order={o} />
        </div>
      </div>

      {modal === 'problem' && <ProblemModal order={o} onClose={() => setModal(null)} />}
      {modal === 'handover' && (
        <Modal title="Передати колезі" onClose={() => setModal(null)}>
          <div className="stack">
            {state.employees
              .filter((e) => e.id !== o.ownerId)
              .map((e) => (
                <button
                  key={e.id}
                  className="btn"
                  onClick={() => {
                    dispatch({ type: 'handOver', orderId: o.id, to: e.id });
                    toast(`${o.number} передано: ${e.name}`);
                    setModal(null);
                  }}
                >
                  {e.name} · {ROLE[e.role]}
                </button>
              ))}
          </div>
        </Modal>
      )}
      {modal === 'cancel' && (
        <Modal title={`Скасувати ${o.number}?`} onClose={() => setModal(null)}>
          <p className="sub">Клієнт отримає повне повернення {m.priceKnown ? uah(m.paid) : 'сплаченої суми'} і сповіщення «Скасовано, кошти повернуто».</p>
          <div className="row" style={{ marginTop: 16, justifyContent: 'flex-end' }}>
            <button className="btn" onClick={() => setModal(null)}>
              Залишити
            </button>
            <button
              className="btn danger"
              onClick={() => {
                dispatch({ type: 'cancelOrder', orderId: o.id });
                toast(`${o.number} скасовано`);
                setModal(null);
              }}
            >
              Скасувати й повернути кошти
            </button>
          </div>
        </Modal>
      )}
      {modal === 'history' && (
        <Modal title={`${o.number} · історія`} onClose={() => setModal(null)}>
          <div className="stack" style={{ gap: 10 }}>
            {[...o.history].reverse().map((h, i) => (
              <div key={i} className="com">
                <b>{h.who}</b>
                <small>{dayLabel(h.at, now)}</small>
                <div>{h.what}</div>
              </div>
            ))}
          </div>
        </Modal>
      )}
      {modal && typeof modal === 'object' && <PriceModal order={o} item={modal.price} onClose={() => setModal(null)} />}
    </>
  );
}

function ItemRow({ order, item, editable, onPrice }: { order: Order; item: Item; editable: boolean; onPrice: () => void }) {
  const { dispatch, toast } = useStore();
  const rule = ruleFor(item);
  const [label, tone] = ITEM_PILL[item.status];
  const d = (type: 'itemCheck' | 'itemSoldOut' | 'itemCancel' | 'itemSendConfirm' | 'itemClientConfirmed', msg: string) => {
    dispatch({ type, orderId: order.id, itemId: item.id });
    toast(msg);
  };
  const cancelled = item.status === 'cancelled';
  const priceText =
    item.price == null ? (
      <span className="faint">{item.storePrice ? uah(item.storePrice) + ' (магазин)' : 'ціна невідома'}</span>
    ) : item.storePrice != null && item.storePrice !== item.price ? (
      <>
        {uah(item.price)} → {uah(item.storePrice)}
      </>
    ) : (
      uah(item.price)
    );

  return (
    <div className={`it ${cancelled ? 'off' : ''}`}>
      <Photo src={item.photo} w={80} h={100} />
      <div className="grow">
        <div className="row" style={{ gap: 8 }}>
          <div className="name">{item.name}</div>
          <span className="tag">{item.store}</span>
        </div>
        <div className="spec">
          <span>Розмір</span> {item.size} &nbsp;·&nbsp; <span>К-сть</span> {item.qty} &nbsp;·&nbsp; {priceText}
        </div>
        {item.comment && <div className="q">{item.comment}</div>}
        {cancelled && <div className="sub" style={{ marginTop: 6 }}>Скасовано · {uah((item.price ?? 0) * item.qty)} повернуто</div>}

        {rule && !cancelled && (
          <div className={`rule ${rule.kind === 'covered' ? 'ok' : rule.kind === 'confirm' ? 'wt' : ''}`}>
            <div className="h">
              <Icon name="alert" size={14} />
              {rule.title}
            </div>
            <div className="d">{rule.detail}</div>
            {editable && rule.kind === 'sold_out' && (
              <div className="b">
                <button className="btn sm pri" onClick={() => d('itemCancel', `${item.name}: скасовано, кошти повернуто`)}>
                  Скасувати й повернути
                </button>
                <a className="btn sm" href={`https://www.google.com/search?q=${encodeURIComponent(item.name + ' ' + item.size + ' купити')}`} target="_blank" rel="noreferrer">
                  Шукати в інших магазинах
                </a>
              </div>
            )}
            {editable && rule.kind === 'confirm' && item.status !== 'awaiting' && (
              <div className="b">
                <button className="btn sm pri" onClick={() => d('itemSendConfirm', 'Запит на підтвердження ціни надіслано клієнту')}>
                  Надіслати запит
                </button>
                <button className="btn sm" onClick={() => d('itemCancel', `${item.name} cancelled, refund sent`)}>
                  Cancel & refund
                </button>
              </div>
            )}
            {editable && item.status === 'awaiting' && (
              <div className="b">
                <button className="btn sm" onClick={() => d('itemClientConfirmed', 'Клієнт підтвердив — купуйте за новою ціною')}>
                  Клієнт підтвердив
                </button>
                <button className="btn sm" onClick={() => d('itemCancel', `${item.name} cancelled, refund sent`)}>
                  Cancel & refund
                </button>
              </div>
            )}
          </div>
        )}
      </div>
      <div className="acts">
        <Pill tone={tone}>{label}</Pill>
        <a className="btn" href={item.url} target="_blank" rel="noreferrer">
          Відкрити в магазині <Icon name="ext" size={14} />
        </a>
        {editable && item.status === 'pending' && (
          <div className="row" style={{ gap: 6 }}>
            <button className="btn sm" onClick={() => d('itemCheck', `${item.name}: перевірено`)}>
              <Icon name="check" size={13} /> Збігається
            </button>
            <button className="btn sm" onClick={() => d('itemSoldOut', `${item.name}: немає в наявності`)}>
              Немає
            </button>
          </div>
        )}
        {editable && !cancelled && item.status !== 'sold_out' && (
          <button className="btn link" onClick={onPrice}>
            {item.storePrice ? 'Змінити ціну магазину' : 'Вказати ціну магазину'}
          </button>
        )}
      </div>
    </div>
  );
}

function PriceModal({ order, item, onClose }: { order: Order; item: Item; onClose: () => void }) {
  const { dispatch } = useStore();
  const [v, setV] = useState(String(item.storePrice ?? item.price ?? ''));
  const n = Number(v.replace(/[^\d.]/g, ''));
  const preview = n > 0 ? ruleFor({ ...item, storePrice: n }) : null;
  return (
    <Modal title={`Ціна в магазині · ${item.name}`} onClose={onClose}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (n > 0) {
            dispatch({ type: 'itemStorePrice', orderId: order.id, itemId: item.id, price: n });
            onClose();
          }
        }}
      >
        <div className="sub" style={{ marginBottom: 8 }}>
          Клієнт сплатив {item.price != null ? uah(item.price) : '—'} за одиницю.
        </div>
        <input className="input" autoFocus inputMode="numeric" value={v} onChange={(e) => setV(e.target.value)} placeholder="₴" />
        {preview && <div className={`rule ${preview.kind === 'covered' ? 'ok' : 'wt'}`} style={{ marginTop: 12 }}><div className="h">{preview.title}</div><div className="d">{preview.detail}</div></div>}
        <div className="row" style={{ marginTop: 16, justifyContent: 'flex-end' }}>
          <button type="button" className="btn" onClick={onClose}>
            Скасувати
          </button>
          <button className="btn pri" disabled={!(n > 0)}>
            Зберегти
          </button>
        </div>
      </form>
    </Modal>
  );
}

const PROBLEMS = ['Магазин скасував замовлення', 'Оплату відхилено', 'Прийшов не той товар', 'Посилку втрачено або пошкоджено', 'Клієнт не на зв’язку'];

const ROLE = { buyer: 'закупник', lead: 'старший зміни', warehouse: 'склад', support: 'підтримка' } as const;

function ProblemModal({ order, onClose }: { order: Order; onClose: () => void }) {
  const { dispatch, toast } = useStore();
  const [text, setText] = useState(order.problem ?? '');
  const save = (p?: string) => {
    dispatch({ type: 'setProblem', orderId: order.id, problem: p });
    toast(p ? 'Проблему позначено — старшого зміни сповіщено' : 'Проблему знято');
    onClose();
  };
  return (
    <Modal title="Позначити проблему" onClose={onClose}>
      <div className="chips">
        {PROBLEMS.map((p) => (
          <button key={p} className={`chip ${text === p ? 'on' : ''}`} onClick={() => setText(p)}>
            {p}
          </button>
        ))}
      </div>
      <input className="input" style={{ marginTop: 12 }} value={text} onChange={(e) => setText(e.target.value)} placeholder="Або опишіть…" />
      <div className="row" style={{ marginTop: 16, justifyContent: 'flex-end' }}>
        {order.problem && (
          <button className="btn" onClick={() => save(undefined)}>
            Зняти проблему
          </button>
        )}
        <button className="btn pri" disabled={!text.trim()} onClick={() => save(text.trim())}>
          Позначити
        </button>
      </div>
    </Modal>
  );
}

function Notes({ order }: { order: Order }) {
  const { dispatch, now } = useStore();
  const [text, setText] = useState('');
  return (
    <div className="card">
      <div className="bd">
        <div className="lbl">Нотатки команди</div>
        {order.notes.length === 0 && <div className="sub" style={{ marginBottom: 12 }}>Нотаток поки немає.</div>}
        {order.notes.map((n) => (
          <div key={n.id} className="com">
            <b>{n.author}</b>
            <small>{dayLabel(n.at, now)}</small>
            <div>{n.text}</div>
          </div>
        ))}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (!text.trim()) return;
            dispatch({ type: 'addNote', orderId: order.id, text: text.trim() });
            setText('');
          }}
        >
          <input className="input" value={text} onChange={(e) => setText(e.target.value)} placeholder="Додати нотатку…" />
        </form>
      </div>
    </div>
  );
}
