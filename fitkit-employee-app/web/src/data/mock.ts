import type { Client, Employee, Item, Order, Shipment, Ticket } from '../domain/types';

/** Mock data for the front-end until the API is ready. Times are relative to page load. */
const T0 = Date.now();
const at = (min: number) => new Date(T0 + min * 60_000).toISOString();
const ago = (min: number) => at(-min);

export const ME = 'e1';

export const employees: Employee[] = [
  { id: 'e1', name: 'Anna Koval', role: 'buyer', color: 'c2' },
  { id: 'e2', name: 'Iryna Rudenko', role: 'lead', color: 'c3' },
  { id: 'e3', name: 'Taras Melnyk', role: 'buyer', color: 'c4' },
];

export const clients: Client[] = [
  { id: 'cl1', name: 'Maria Lebedenko', color: 'c2', telegram: '@maria_l', phoneMasked: '+380 67 ••• 45 12', address: 'Kyiv, 12 Velyka Vasylkivska St, apt 48', delivery: 'Nova Poshta courier', sizes: 'S–M · W28 L32 · 38', stores: 'Zara, COS, Massimo Dutti', dislikes: 'synthetics, loud prints', note: 'Zara runs small for her — take one size up.' },
  { id: 'cl2', name: 'Ihor Sokolenko', color: 'c4', telegram: '@ihor_s', phoneMasked: '+380 50 ••• 11 07', address: 'Lviv, Nova Poshta branch 14', delivery: 'Nova Poshta branch', sizes: 'L · 44', stores: 'Answear, Nike' },
  { id: 'cl3', name: 'Olha Petrenko', color: 'c3', phoneMasked: '+380 93 ••• 80 21', address: 'Odesa, 5 Deribasivska St, apt 3', delivery: 'Nova Poshta courier', sizes: 'XS–S · W26 · 37', stores: 'Reserved, Zara' },
  { id: 'cl4', name: 'Daria Vovk', color: 'c5', telegram: '@dariavovk', phoneMasked: '+380 63 ••• 52 90', address: 'Kyiv, Nova Poshta branch 101', delivery: 'Nova Poshta branch', sizes: 'M · W29', stores: 'ASOS, H&M' },
  { id: 'cl5', name: 'Pavlo Tykhonenko', color: 'c2', phoneMasked: '+380 97 ••• 33 18', address: 'Dnipro, 40 Yavornytskoho Ave, apt 12', delivery: 'Nova Poshta courier', sizes: 'L · 43', stores: 'Nike, Zara' },
  { id: 'cl6', name: 'Kseniia Orlyk', color: 'c4', telegram: '@ks_orlyk', phoneMasked: '+380 66 ••• 74 05', address: 'Kharkiv, Nova Poshta branch 7', delivery: 'Nova Poshta branch', sizes: 'S · 38', stores: 'Mango, COS' },
  { id: 'cl7', name: 'Artem Bilyk', color: 'c3', phoneMasked: '+380 68 ••• 19 44', address: 'Kyiv, 3 Khreshchatyk St, apt 9', delivery: 'Nova Poshta courier', sizes: 'M · 42', stores: 'Zara, AliExpress' },
  { id: 'cl8', name: 'Olena Smyrnova', color: 'c5', phoneMasked: '+380 99 ••• 62 31', address: 'Vinnytsia, Nova Poshta branch 2', delivery: 'Nova Poshta branch', sizes: 'S · W27 · 38', stores: 'Massimo Dutti, H&M' },
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
  history: [{ at: o.createdAt, who: 'System', what: 'Request received' }],
  fee: Math.round(((o.paid ?? 0) * 0.075) / 10) * 10,
  ...o,
});

export const orders: Order[] = [
  // ---- New requests (not taken yet)
  order({ number: '#009', clientId: 'cl8', status: 'new', createdAt: ago(102), dueAt: ago(42), paid: 3999, items: [it('jacket-black', 'Black jacket', 'Zara', 'S', 3999, { comment: '“Like in the photo, black”' })] }),
  order({ number: '#002', clientId: 'cl2', status: 'new', createdAt: ago(75), dueAt: ago(15), paid: 2499, items: [it('hoodie', 'Relaxed hoodie', 'Answear', 'L', 2499)] }),
  order({ number: '#003', clientId: 'cl3', status: 'new', createdAt: ago(22), dueAt: at(8), paid: 3170, items: [it('sweater-grey', 'Grey knit sweater', 'Reserved', 'S', 1771), it('jeans', 'Straight jeans', 'Reserved', 'W26 L32', 1399)] }),
  order({ number: '#004', clientId: 'cl4', status: 'new', createdAt: ago(1), dueAt: at(29), items: [it('hoodie', 'Basic hoodie', 'ASOS', 'M', undefined), it('sweatpants', 'Joggers', 'ASOS', 'M', undefined), it('scarf', 'Wool scarf', 'ASOS', 'One size', undefined)] }),
  order({ number: '#005', clientId: 'cl5', status: 'new', createdAt: ago(-5), dueAt: at(35), paid: 5899, items: [it('sneakers', 'Air sneakers', 'Nike', '43', 5899)] }),
  order({ number: '#006', clientId: 'cl6', status: 'new', createdAt: ago(-10), dueAt: at(40), paid: 4270, items: [it('scarf', 'Check scarf', 'Mango', 'One size', 1299), it('loafers', 'Leather loafers', 'COS', '38', 2971)] }),
  order({ number: '#007', clientId: 'cl7', status: 'new', createdAt: ago(-18), dueAt: at(48), items: [it('stripe', 'Striped sweater', 'Zara', 'M', undefined), it('sweatpants2', 'Track pants', 'Zara', 'M', undefined), it('loafers', 'Loafers', 'Zara', '42', undefined)] }),

  // ---- In progress
  order({
    number: '#001', clientId: 'cl1', ownerId: 'e1', status: 'in_progress', createdAt: ago(170), dueAt: at(80), paid: 7777, fee: 580,
    items: [
      it('stripe', 'Striped sweater', 'Zara', 'L', 1799, { comment: '“One size up, I like a loose fit”', status: 'checked' }),
      it('jacket-black', 'Black jacket', 'Zara', 'M', 3999, { comment: '“Need it by Nov 25”', status: 'sold_out' }),
      it('jeans-black', 'Wide-leg jeans', 'H&M', 'W28 L32', 1399, { comment: '“Dark, like in the photo”', status: 'checked', storePrice: 1449 }),
    ],
    problem: 'Jacket sold out — apply rule',
    notes: [{ id: 'n1', author: 'Iryna R.', at: ago(30), text: 'Massimo Dutti has a similar jacket in M — check before refunding.' }],
    history: [
      { at: ago(170), who: 'System', what: 'Request received' },
      { at: ago(150), who: 'Anna Koval', what: 'Took the request' },
      { at: ago(60), who: 'Anna Koval', what: 'Black jacket: marked sold out' },
    ],
  }),
  order({ number: '#008', clientId: 'cl8', ownerId: 'e1', status: 'in_progress', createdAt: ago(60), dueAt: at(120), paid: 3999, items: [it('jacket-black', 'Black jacket', 'Massimo Dutti', 'S', 3999)] }),
  order({ number: '#0993', clientId: 'cl7', ownerId: 'e1', status: 'in_progress', createdAt: ago(80), dueAt: at(160), paid: 5380, items: [it('hoodie', 'Zip hoodie', 'Zara', 'M', 2690, { status: 'checked' }), it('sweatpants', 'Joggers', 'Zara', 'M', 2690)] }),
  order({ number: '#0990', clientId: 'cl6', ownerId: 'e3', status: 'in_progress', createdAt: ago(90), dueAt: at(180), paid: 1599, items: [it('scarf', 'Wool scarf', 'COS', 'One size', 1599)] }),
  order({ number: '#0987', clientId: 'cl3', ownerId: 'e3', status: 'in_progress', createdAt: ago(100), dueAt: at(210), paid: 12480, items: [it('sweater-grey', 'Cashmere sweater', 'COS', 'S', 6490), it('jeans', 'Straight jeans', 'COS', 'W26', 3490), it('loafers', 'Loafers', 'COS', '37', 2500)] }),

  // ---- Awaiting confirmation
  order({ number: '#0995', clientId: 'cl2', ownerId: 'e1', status: 'awaiting', createdAt: ago(600), dueAt: at(360), paid: 5899, items: [it('sneakers', 'Air sneakers', 'Nike', '44', 5899, { storePrice: 6599, status: 'awaiting' })], problem: undefined }),
  order({ number: '#0981', clientId: 'cl5', ownerId: 'e3', status: 'awaiting', createdAt: ago(1800), dueAt: ago(120), paid: 4480, items: [it('stripe', 'Striped sweater', 'Zara', 'L', 2240, { status: 'checked' }), it('sweatpants2', 'Track pants', 'Zara', 'L', 2240, { storePrice: 2590, status: 'awaiting' })], problem: 'No answer 26h — auto-refund due' }),
  order({ number: '#0976', clientId: 'cl4', ownerId: 'e1', status: 'awaiting', createdAt: ago(300), dueAt: at(120), paid: 1899, items: [it('jeans-black', 'Wide-leg jeans', 'H&M', 'W29', 1899, { storePrice: 2069, status: 'awaiting' })] }),

  // ---- Purchased (on the way to the warehouse)
  order({ number: '#0968', clientId: 'cl8', ownerId: 'e1', status: 'purchased', createdAt: ago(9000), dueAt: at(600), paid: 4590, location: 'At warehouse · Nova Poshta', items: [it('loafers', 'Leather loafers', 'Massimo Dutti', '38', 4590, { status: 'bought' })] }),
  order({ number: '#0972', clientId: 'cl7', ownerId: 'e1', status: 'purchased', createdAt: ago(7000), dueAt: at(5000), paid: 2140, location: 'In transit · Cainiao', items: [it('hoodie', 'Oversized hoodie', 'AliExpress', 'L', 1290, { status: 'bought' }), it('sweatpants', 'Cargo joggers', 'AliExpress', 'L', 850, { status: 'bought' })] }),
  order({ number: '#0951', clientId: 'cl5', ownerId: 'e3', status: 'purchased', createdAt: ago(8000), dueAt: at(300), paid: 5899, location: 'Waiting for tracking · Nike', problem: 'No tracking for 3 days', items: [it('sneakers', 'Air sneakers', 'Nike', '43', 5899, { status: 'bought' })] }),
  order({ number: '#0947', clientId: 'cl6', ownerId: 'e1', status: 'purchased', createdAt: ago(11000), dueAt: at(200), paid: 5080, location: 'In transit · DHL', problem: 'No movement for 5 days', items: [it('sweater-grey', 'Knit sweater', 'COS', 'S', 3490, { status: 'bought' }), it('scarf', 'Scarf', 'COS', 'One size', 1590, { status: 'bought' })] }),

  // ---- Shipped
  order({ number: '#0932', clientId: 'cl3', ownerId: 'e1', status: 'shipped', createdAt: ago(12000), dueAt: at(1440), paid: 3198, location: 'Nova Poshta · arrives tomorrow', items: [it('jeans', 'Straight jeans', 'Reserved', 'W26', 1399, { status: 'bought' }), it('stripe', 'Striped top', 'Reserved', 'S', 1799, { status: 'bought' })] }),
  order({ number: '#0918', clientId: 'cl1', ownerId: 'e1', status: 'shipped', createdAt: ago(14000), dueAt: at(300), paid: 3999, location: 'Courier delivers today', items: [it('jacket-black', 'Wool coat', 'Massimo Dutti', 'S', 3999, { status: 'bought' })] }),
];

export const shipments: Shipment[] = [
  { id: 's1', orderId: 'o0968', leg: 'in', store: 'Massimo Dutti', carrier: 'Nova Poshta', tracking: '2045 0088 1244 71', source: 'email', atWarehouse: true, events: [
    { at: ago(8600), title: 'Purchased at Massimo Dutti' },
    { at: ago(7200), title: 'Handed to Nova Poshta', detail: 'tracking from store email' },
    { at: ago(48), title: 'Arrived at warehouse', detail: 'checked, 3 photos' },
  ] },
  { id: 's2', orderId: 'o0972', leg: 'in', store: 'AliExpress', carrier: 'Cainiao', tracking: 'LP00 4821 7730 15UA', source: 'email', events: [
    { at: ago(6900), title: 'Purchased at AliExpress' },
    { at: ago(5000), title: 'Accepted by Cainiao', detail: 'tracking from store email' },
    { at: ago(210), title: 'Left sorting center, Shenzhen' },
  ] },
  { id: 's3', orderId: 'o0951', leg: 'in', store: 'Nike', problem: 'No tracking for 3 days', events: [{ at: ago(7900), title: 'Purchased at Nike' }] },
  { id: 's4', orderId: 'o0947', leg: 'in', store: 'COS', carrier: 'DHL', tracking: '4821 0093 77', source: 'manual', problem: 'No movement for 5 days', events: [
    { at: ago(10800), title: 'Purchased at COS' },
    { at: ago(7300), title: 'Picked up by DHL', detail: 'tracking entered by buyer' },
  ] },
  { id: 's5', orderId: 'o0932', leg: 'out', carrier: 'Nova Poshta', tracking: '2045 0099 8211 67', source: 'api', events: [
    { at: ago(1500), title: 'Shipment created', detail: 'Nova Poshta API' },
    { at: ago(1300), title: 'On the way to client' },
  ] },
  { id: 's6', orderId: 'o0918', leg: 'out', carrier: 'Nova Poshta', tracking: '2045 0055 3000 81', source: 'api', events: [
    { at: ago(2900), title: 'Shipment created', detail: 'Nova Poshta API' },
    { at: ago(25), title: 'Courier delivers today' },
  ] },
];

export const tickets: Ticket[] = [
  { id: 't1', clientId: 'cl1', orderId: 'o001', status: 'open', summary: 'When will my order arrive?', updatedAt: ago(19), messages: [
    { id: 'm1', from: 'system', text: 'Item cancelled automatically: Black jacket · ₴3,999 refunded · client notified', at: ago(40) },
    { id: 'm2', from: 'client', text: 'Hi! I got a refund for the jacket, but when will the rest of my order arrive?', at: ago(19) },
  ] },
  { id: 't2', clientId: 'cl2', orderId: 'o0995', status: 'open', summary: 'Can I change the delivery address?', updatedAt: ago(40), messages: [
    { id: 'm3', from: 'client', text: 'Can I change the delivery address? I moved to another branch.', at: ago(40) },
  ] },
  { id: 't3', clientId: 'cl3', orderId: 'o0932', status: 'open', summary: 'Parcel says delivered but…', updatedAt: ago(48), messages: [
    { id: 'm4', from: 'client', text: 'The tracking says delivered tomorrow but the courier called today — is that right?', at: ago(48) },
  ] },
  { id: 't4', clientId: 'cl4', orderId: 'o0976', status: 'resolved', summary: 'Refund received', updatedAt: ago(1500), messages: [
    { id: 'm5', from: 'client', text: 'Did you refund the old order?', at: ago(1600) },
    { id: 'm6', from: 'support', text: 'Yes, the refund was sent on Nov 20 — it takes up to 3 banking days.', at: ago(1500) },
  ] },
  { id: 't5', clientId: 'cl5', orderId: 'o0981', status: 'resolved', summary: 'Size question', updatedAt: ago(3000), messages: [
    { id: 'm7', from: 'client', text: 'Is L the right size for the track pants?', at: ago(3100) },
    { id: 'm8', from: 'support', text: 'Yes, L matches your usual size in Zara.', at: ago(3000) },
  ] },
];

export const QUICK_REPLIES: Record<string, string> = {
  'Order status': 'Your order is being prepared. You’ll get a Nova Poshta tracking number as soon as it leaves our warehouse.',
  'Refund info': 'The refund has been sent to your card. Banks usually take up to 3 working days.',
  'Delivery date': 'We expect to ship your order within 2–3 days; delivery by Nova Poshta takes 1–2 more days.',
  'Change address': 'Sure! Send the new address or Nova Poshta branch and we’ll update it before shipping.',
};
