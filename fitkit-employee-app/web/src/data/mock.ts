import type { Client, Employee, Item, Order, Shipment, Ticket } from '../domain/types';

/** Mock data for the front-end until the API is ready. Times are relative to page load. */
const T0 = Date.now();
const at = (min: number) => new Date(T0 + min * 60_000).toISOString();
const ago = (min: number) => at(-min);

export const ME = 'e1';

export const employees: Employee[] = [
  { id: 'e1', name: 'Анна Коваль', role: 'buyer', color: 'c2' },
  { id: 'e2', name: 'Ірина Руденко', role: 'lead', color: 'c3' },
  { id: 'e3', name: 'Тарас Мельник', role: 'buyer', color: 'c4' },
];

export const clients: Client[] = [
  { id: 'cl1', name: 'Марія Лебеденко', color: 'c2', telegram: '@maria_l', phoneMasked: '+380 67 ••• 45 12', address: 'Київ, вул. Велика Васильківська, 12, кв. 48', delivery: 'Кур’єр Нової Пошти', sizes: 'S–M · W28 L32 · 38', stores: 'Zara, COS, Massimo Dutti', dislikes: 'синтетика, яскраві принти', note: 'Zara на неї маломірить — беріть на розмір більше.' },
  { id: 'cl2', name: 'Ігор Соколенко', color: 'c4', telegram: '@ihor_s', phoneMasked: '+380 50 ••• 11 07', address: 'Львів, відділення Нової Пошти №14', delivery: 'Відділення Нової Пошти', sizes: 'L · 44', stores: 'Answear, Nike' },
  { id: 'cl3', name: 'Ольга Петренко', color: 'c3', phoneMasked: '+380 93 ••• 80 21', address: 'Одеса, вул. Дерибасівська, 5, кв. 3', delivery: 'Кур’єр Нової Пошти', sizes: 'XS–S · W26 · 37', stores: 'Reserved, Zara' },
  { id: 'cl4', name: 'Дарія Вовк', color: 'c5', telegram: '@dariavovk', phoneMasked: '+380 63 ••• 52 90', address: 'Київ, відділення Нової Пошти №101', delivery: 'Відділення Нової Пошти', sizes: 'M · W29', stores: 'ASOS, H&M' },
  { id: 'cl5', name: 'Павло Тихоненко', color: 'c2', phoneMasked: '+380 97 ••• 33 18', address: 'Дніпро, просп. Яворницького, 40, кв. 12', delivery: 'Кур’єр Нової Пошти', sizes: 'L · 43', stores: 'Nike, Zara' },
  { id: 'cl6', name: 'Ксенія Орлик', color: 'c4', telegram: '@ks_orlyk', phoneMasked: '+380 66 ••• 74 05', address: 'Харків, відділення Нової Пошти №7', delivery: 'Відділення Нової Пошти', sizes: 'S · 38', stores: 'Mango, COS' },
  { id: 'cl7', name: 'Артем Білик', color: 'c3', phoneMasked: '+380 68 ••• 19 44', address: 'Київ, вул. Хрещатик, 3, кв. 9', delivery: 'Кур’єр Нової Пошти', sizes: 'M · 42', stores: 'Zara, AliExpress' },
  { id: 'cl8', name: 'Олена Смирнова', color: 'c5', phoneMasked: '+380 99 ••• 62 31', address: 'Вінниця, відділення Нової Пошти №2', delivery: 'Відділення Нової Пошти', sizes: 'S · W27 · 38', stores: 'Massimo Dutti, H&M' },
];

let seq = 0;
const it = (photo: string, name: string, store: string, size: string, price: number | undefined, extra: Partial<Item> = {}): Item => ({
  id: `i${++seq}`,
  photo,
  name,
  store,
  url: storeUrl(store),
  size,
  qty: 1,
  price,
  status: 'pending',
  ...extra,
});

function storeUrl(store: string): string {
  const map: Record<string, string> = {
    Zara: 'https://www.zara.com/ua/',
    'H&M': 'https://www2.hm.com/',
    Answear: 'https://answear.ua/',
    Reserved: 'https://www.reserved.com/ua/',
    ASOS: 'https://www.asos.com/',
    Nike: 'https://www.nike.com/',
    Mango: 'https://shop.mango.com/ua/',
    COS: 'https://www.cos.com/',
    'Massimo Dutti': 'https://www.massimodutti.com/ua/',
    AliExpress: 'https://www.aliexpress.com/',
  };
  return map[store] ?? 'https://www.google.com/search?q=' + encodeURIComponent(store);
}

type OrderSeed = Omit<Order, 'id' | 'notes' | 'history' | 'fee'> & Partial<Pick<Order, 'notes' | 'history' | 'fee'>>;
const order = (o: OrderSeed): Order => ({
  id: o.number.replace('#', 'o'),
  notes: [],
  history: [{ at: o.createdAt, who: 'Система', what: 'Заявка надійшла' }],
  fee: Math.round(((o.paid ?? 0) * 0.075) / 10) * 10,
  ...o,
});

export const orders: Order[] = [
  // ---- New requests (not taken yet)
  order({ number: '#009', clientId: 'cl8', status: 'new', createdAt: ago(102), dueAt: ago(42), paid: 3999, items: [it('jacket-black', 'Чорна куртка', 'Zara', 'S', 3999, { comment: '«Як на фото, чорна»' })] }),
  order({ number: '#002', clientId: 'cl2', status: 'new', createdAt: ago(75), dueAt: ago(15), paid: 2499, items: [it('hoodie', 'Худі вільного крою', 'Answear', 'L', 2499)] }),
  order({ number: '#003', clientId: 'cl3', status: 'new', createdAt: ago(22), dueAt: at(8), paid: 3170, items: [it('sweater-grey', 'Сірий в’язаний светр', 'Reserved', 'S', 1771), it('jeans', 'Прямі джинси', 'Reserved', 'W26 L32', 1399)] }),
  order({ number: '#004', clientId: 'cl4', status: 'new', createdAt: ago(1), dueAt: at(29), items: [it('hoodie', 'Базове худі', 'ASOS', 'M', undefined), it('sweatpants', 'Джогери', 'ASOS', 'M', undefined), it('scarf', 'Вовняний шарф', 'ASOS', 'Один розмір', undefined)] }),
  order({ number: '#005', clientId: 'cl5', status: 'new', createdAt: ago(-5), dueAt: at(35), paid: 5899, items: [it('sneakers', 'Кросівки Air', 'Nike', '43', 5899)] }),
  order({ number: '#006', clientId: 'cl6', status: 'new', createdAt: ago(-10), dueAt: at(40), paid: 4270, items: [it('scarf', 'Картатий шарф', 'Mango', 'Один розмір', 1299), it('loafers', 'Шкіряні лофери', 'COS', '38', 2971)] }),
  order({ number: '#007', clientId: 'cl7', status: 'new', createdAt: ago(-18), dueAt: at(48), items: [it('stripe', 'Смугастий светр', 'Zara', 'M', undefined), it('sweatpants2', 'Спортивні штани', 'Zara', 'M', undefined), it('loafers', 'Лофери', 'Zara', '42', undefined)] }),

  // ---- In progress
  order({
    number: '#001', clientId: 'cl1', ownerId: 'e1', status: 'in_progress', createdAt: ago(170), dueAt: at(80), paid: 7777, fee: 580,
    items: [
      it('stripe', 'Смугастий светр', 'Zara', 'L', 1799, { comment: '«На розмір більше, люблю вільну посадку»', status: 'checked' }),
      it('jacket-black', 'Чорна куртка', 'Zara', 'M', 3999, { comment: '«Потрібно до 25 листопада»', status: 'sold_out' }),
      it('jeans-black', 'Широкі джинси', 'H&M', 'W28 L32', 1399, { comment: '«Темні, як на фото»', status: 'checked', storePrice: 1449 }),
    ],
    problem: 'Чорна куртка: немає в наявності — застосуйте правило',
    notes: [{ id: 'n1', author: 'Ірина Р.', at: ago(30), text: 'У Massimo Dutti є схожа куртка в M — перевір перед поверненням.' }],
    history: [
      { at: ago(170), who: 'Система', what: 'Заявка надійшла' },
      { at: ago(150), who: 'Анна Коваль', what: 'Заявку взято в роботу' },
      { at: ago(60), who: 'Анна Коваль', what: 'Чорна куртка: позначено «немає в наявності»' },
    ],
  }),
  order({ number: '#008', clientId: 'cl8', ownerId: 'e1', status: 'in_progress', createdAt: ago(60), dueAt: at(120), paid: 3999, items: [it('jacket-black', 'Чорна куртка', 'Massimo Dutti', 'S', 3999)] }),
  order({ number: '#0993', clientId: 'cl7', ownerId: 'e1', status: 'in_progress', createdAt: ago(80), dueAt: at(160), paid: 5380, items: [it('hoodie', 'Худі на блискавці', 'Zara', 'M', 2690, { status: 'checked' }), it('sweatpants', 'Джогери', 'Zara', 'M', 2690)] }),
  order({ number: '#0990', clientId: 'cl6', ownerId: 'e3', status: 'in_progress', createdAt: ago(90), dueAt: at(180), paid: 1599, items: [it('scarf', 'Вовняний шарф', 'COS', 'Один розмір', 1599)] }),
  order({ number: '#0987', clientId: 'cl3', ownerId: 'e3', status: 'in_progress', createdAt: ago(100), dueAt: at(210), paid: 12480, items: [it('sweater-grey', 'Кашеміровий светр', 'COS', 'S', 6490), it('jeans', 'Прямі джинси', 'COS', 'W26', 3490), it('loafers', 'Лофери', 'COS', '37', 2500)] }),

  // ---- Awaiting confirmation
  order({ number: '#0995', clientId: 'cl2', ownerId: 'e1', status: 'awaiting', createdAt: ago(600), dueAt: at(360), paid: 5899, items: [it('sneakers', 'Кросівки Air', 'Nike', '44', 5899, { storePrice: 6599, status: 'awaiting' })], problem: undefined }),
  order({ number: '#0981', clientId: 'cl5', ownerId: 'e3', status: 'awaiting', createdAt: ago(1800), dueAt: ago(120), paid: 4480, items: [it('stripe', 'Смугастий светр', 'Zara', 'L', 2240, { status: 'checked' }), it('sweatpants2', 'Спортивні штани', 'Zara', 'L', 2240, { storePrice: 2590, status: 'awaiting' })], problem: 'Немає відповіді 26 год — потрібне автоповернення' }),
  order({ number: '#0976', clientId: 'cl4', ownerId: 'e1', status: 'awaiting', createdAt: ago(300), dueAt: at(120), paid: 1899, items: [it('jeans-black', 'Широкі джинси', 'H&M', 'W29', 1899, { storePrice: 2069, status: 'awaiting' })] }),

  // ---- Purchased (on the way to the warehouse)
  order({ number: '#0968', clientId: 'cl8', ownerId: 'e1', status: 'purchased', createdAt: ago(9000), dueAt: at(600), paid: 4590, location: 'На складі · Нова Пошта', items: [it('loafers', 'Шкіряні лофери', 'Massimo Dutti', '38', 4590, { status: 'bought' })] }),
  order({ number: '#0972', clientId: 'cl7', ownerId: 'e1', status: 'purchased', createdAt: ago(7000), dueAt: at(5000), paid: 2140, location: 'В дорозі · Cainiao', items: [it('hoodie', 'Худі оверсайз', 'AliExpress', 'L', 1290, { status: 'bought' }), it('sweatpants', 'Джогери карго', 'AliExpress', 'L', 850, { status: 'bought' })] }),
  order({ number: '#0951', clientId: 'cl5', ownerId: 'e3', status: 'purchased', createdAt: ago(8000), dueAt: at(300), paid: 5899, location: 'Чекаємо ТТН · Nike', problem: 'Немає ТТН 3 дні', items: [it('sneakers', 'Кросівки Air', 'Nike', '43', 5899, { status: 'bought' })] }),
  order({ number: '#0947', clientId: 'cl6', ownerId: 'e1', status: 'purchased', createdAt: ago(11000), dueAt: at(200), paid: 5080, location: 'В дорозі · DHL', problem: 'Немає руху 5 днів', items: [it('sweater-grey', 'В’язаний светр', 'COS', 'S', 3490, { status: 'bought' }), it('scarf', 'Шарф', 'COS', 'Один розмір', 1590, { status: 'bought' })] }),

  // ---- Shipped
  order({ number: '#0932', clientId: 'cl3', ownerId: 'e1', status: 'shipped', createdAt: ago(12000), dueAt: at(1440), paid: 3198, location: 'Нова Пошта · прибуде завтра', items: [it('jeans', 'Прямі джинси', 'Reserved', 'W26', 1399, { status: 'bought' }), it('stripe', 'Смугастий топ', 'Reserved', 'S', 1799, { status: 'bought' })] }),
  order({ number: '#0918', clientId: 'cl1', ownerId: 'e1', status: 'shipped', createdAt: ago(14000), dueAt: at(300), paid: 3999, location: 'Кур’єр доставить сьогодні', items: [it('jacket-black', 'Вовняне пальто', 'Massimo Dutti', 'S', 3999, { status: 'bought' })] }),
];

export const shipments: Shipment[] = [
  { id: 's1', orderId: 'o0968', leg: 'in', store: 'Massimo Dutti', carrier: 'Нова Пошта', tracking: '2045 0088 1244 71', source: 'email', atWarehouse: true, events: [
    { at: ago(8600), title: 'Викуплено в Massimo Dutti' },
    { at: ago(7200), title: 'Передано Новій Пошті', detail: 'ТТН з листа магазину' },
    { at: ago(48), title: 'Прибуло на склад', detail: 'перевірено, 3 фото' },
  ] },
  { id: 's2', orderId: 'o0972', leg: 'in', store: 'AliExpress', carrier: 'Cainiao', tracking: 'LP00 4821 7730 15UA', source: 'email', events: [
    { at: ago(6900), title: 'Викуплено на AliExpress' },
    { at: ago(5000), title: 'Прийнято Cainiao', detail: 'ТТН з листа магазину' },
    { at: ago(210), title: 'Виїхало із сортувального центру, Шеньчжень' },
  ] },
  { id: 's3', orderId: 'o0951', leg: 'in', store: 'Nike', problem: 'Немає ТТН 3 дні', events: [{ at: ago(7900), title: 'Викуплено в Nike' }] },
  { id: 's4', orderId: 'o0947', leg: 'in', store: 'COS', carrier: 'DHL', tracking: '4821 0093 77', source: 'manual', problem: 'Немає руху 5 днів', events: [
    { at: ago(10800), title: 'Викуплено в COS' },
    { at: ago(7300), title: 'Забрано DHL', detail: 'ТТН введено закупником' },
  ] },
  { id: 's5', orderId: 'o0932', leg: 'out', carrier: 'Нова Пошта', tracking: '2045 0099 8211 67', source: 'api', events: [
    { at: ago(1500), title: 'ТТН створено', detail: 'API Нової Пошти' },
    { at: ago(1300), title: 'Прямує до клієнта' },
  ] },
  { id: 's6', orderId: 'o0918', leg: 'out', carrier: 'Нова Пошта', tracking: '2045 0055 3000 81', source: 'api', events: [
    { at: ago(2900), title: 'ТТН створено', detail: 'API Нової Пошти' },
    { at: ago(25), title: 'Кур’єр доставить сьогодні' },
  ] },
];

export const tickets: Ticket[] = [
  { id: 't1', clientId: 'cl1', orderId: 'o001', status: 'open', summary: 'Коли прийде моє замовлення?', updatedAt: ago(19), messages: [
    { id: 'm1', from: 'system', text: 'Товар скасовано автоматично: Чорна куртка · 3 999 ₴ повернуто · клієнта сповіщено', at: ago(40) },
    { id: 'm2', from: 'client', text: 'Привіт! Гроші за куртку повернули, а коли прийде решта замовлення?', at: ago(19) },
  ] },
  { id: 't2', clientId: 'cl2', orderId: 'o0995', status: 'open', summary: 'Можна змінити адресу доставки?', updatedAt: ago(40), messages: [
    { id: 'm3', from: 'client', text: 'Можна змінити адресу доставки? Мені зручніше інше відділення.', at: ago(40) },
  ] },
  { id: 't3', clientId: 'cl3', orderId: 'o0932', status: 'open', summary: 'Трекінг показує завтра, а кур’єр…', updatedAt: ago(48), messages: [
    { id: 'm4', from: 'client', text: 'Трекінг показує доставку завтра, а кур’єр подзвонив сьогодні — так і має бути?', at: ago(48) },
  ] },
  { id: 't4', clientId: 'cl4', orderId: 'o0976', status: 'resolved', summary: 'Повернення отримано', updatedAt: ago(1500), messages: [
    { id: 'm5', from: 'client', text: 'Ви повернули гроші за старе замовлення?', at: ago(1600) },
    { id: 'm6', from: 'support', text: 'Так, повернення надіслали 20 листопада — це займає до 3 банківських днів.', at: ago(1500) },
  ] },
  { id: 't5', clientId: 'cl5', orderId: 'o0981', status: 'resolved', summary: 'Питання про розмір', updatedAt: ago(3000), messages: [
    { id: 'm7', from: 'client', text: 'Спортивні штани в L мені підійдуть?', at: ago(3100) },
    { id: 'm8', from: 'support', text: 'Так, L відповідає вашому звичному розміру в Zara.', at: ago(3000) },
  ] },
];

export const QUICK_REPLIES: Record<string, string> = {
  'Статус замовлення': 'Ваше замовлення готується. Щойно воно виїде з нашого складу, ви отримаєте номер ТТН Нової Пошти.',
  'Повернення коштів': 'Кошти повернуто на вашу картку. Зазвичай банк зараховує їх протягом 3 робочих днів.',
  'Дата доставки': 'Плануємо відправити замовлення протягом 2–3 днів; доставка Новою Поштою займає ще 1–2 дні.',
  'Змінити адресу': 'Звісно! Надішліть нову адресу або відділення Нової Пошти — оновимо до відправки.',
};
