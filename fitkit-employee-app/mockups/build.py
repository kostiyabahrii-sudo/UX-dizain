# Mockup generator (minimal v4): python3 mockups/build.py mockups
import sys, os
OUT = sys.argv[1]
I = {
 'inbox': '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
 'bag': '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'truck': '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
 'back': '<path d="m15 18-6-6 6-6"/>',
 'ext': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'send': '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
 'clip': '<path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>',
 'msg': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'more': '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
 'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
}
def ic(n, w=16): return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I[n]}</svg>'
def photo(p, w, h, extra=''): return f'<img class="ph" src="assets/photos/{p}.jpg" style="width:{w}px;height:{h}px{extra}">'
def thumbs(ps, w=30, h=38):
    return '<div class="thumbs">' + ''.join(photo(p, w, h, ';margin-left:-8px' if i else '') for i, p in enumerate(ps)) + '</div>'
def ini(n): return ''.join(w[0] for w in n.split())

BASE = '''
.side { width: 208px; padding: 20px 12px; }
.side .cap { display: none; }
.nav a { padding: 9px 10px; }
.main { padding: 28px 36px; gap: 20px; }
.card { border-radius: 16px; }
h1 { font-size: 24px; }
h1 .cnt { color: var(--faint); font-weight: 500; }
.num { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-weight: 600; letter-spacing: -.01em; }
.who { display: flex; gap: 10px; align-items: center; }
.thumbs { display: flex; } .thumbs img { border: 2px solid var(--panel); }
.tabs { display: flex; gap: 2px; }
.tabs a { padding: 7px 14px; border-radius: 999px; color: var(--muted); font-weight: 500; display: flex; gap: 7px; align-items: center; }
.tabs a.on { background: var(--clay-veil); color: var(--text); font-weight: 600; }
.tabs a b { font-weight: 600; font-size: 12px; color: var(--faint); }
.tabs a.red b { color: var(--bad); }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; font-size: 12px; font-weight: 500; color: var(--faint); padding: 12px 16px; border-bottom: 1px solid var(--line); }
td { padding: 12px 16px; border-bottom: 1px solid var(--line); white-space: nowrap; vertical-align: middle; }
tr:last-child td { border-bottom: 0; }
tr.late td:first-child { box-shadow: inset 3px 0 0 var(--bad); }
tr.on td { background: var(--clay-veil); }
.timer { font-weight: 600; font-size: 13px; color: var(--muted); }
.timer.red { color: var(--bad); } .timer.org { color: var(--wait); }
.badge { background: var(--clay); color: #1c1013; font-size: 11px; font-weight: 700; border-radius: 9px; padding: 0 6px; }
.lbl { font-size: 11.5px; color: var(--faint); font-weight: 500; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 8px; }
.ghost { color: var(--muted); font-size: 13px; display: inline-flex; gap: 6px; align-items: center; }
.ghost svg { color: var(--faint); }
.iconbtn { width: 34px; padding: 0; }
'''
def shell(active, title, main, css=''):
    items = [('inbox','Requests','<span class="n red">12</span>'),('bag','Current orders','<span class="n">14</span>'),('users','Clients','<span class="n red">3</span>'),('truck','Tracking','<span class="n red">2</span>')]
    nav = ''.join(f'<a class="{"on" if t == active else ""}">{ic(i, 17)}{t}{n}</a>' for i, t, n in items)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fitkit — {title}</title>
<link rel="stylesheet" href="styles.css"><style>{BASE}{css}</style></head>
<body><div class="app">
  <aside class="side">
    <div class="logo"><img src="assets/logo-mark.png" alt=""><b>Fitkit</b></div>
    <nav class="nav">{nav}</nav>
    <div class="me"><div class="ava c2">AK</div><div>Anna Koval<small>Buyer</small></div></div>
  </aside>
  <div class="body">
    <div class="top"><div class="search">Search request #, client, phone or tracking…<kbd>⌘K</kbd></div><div class="bell">{ic('bell', 18)}<i></i></div></div>
    <main class="main">{main}</main>
  </div>
</div></body></html>'''
def save(name, html): open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)

# ---------- 01 Requests ----------
P = {'#001':['stripe','jacket-black','jeans-black'],'#002':['hoodie'],'#003':['sweater-grey','jeans'],'#004':['hoodie','sweatpants','scarf'],'#005':['sneakers'],'#006':['scarf','loafers'],'#007':['stripe','sweatpants2','loafers']}
rows = [('#001','late','Maria Lebedenko','c2',3,'Zara, H&amp;M','₴7,777','bad','Overdue','red','−42 min'),
        ('#002','late','Ihor Sokolenko','c4',1,'Answear','₴2,499','bad','Overdue','red','−15 min'),
        ('#003','','Olha Petrenko','c3',2,'Reserved','₴3,170','new','New','org','8 min left'),
        ('#004','','Daria Vovk','c5',4,'ASOS','price not set','new','New','','29 min left'),
        ('#005','','Pavlo Tykhonenko','c2',1,'Nike','₴5,899','new','New','','35 min left'),
        ('#006','','Kseniia Orlyk','c4',2,'Mango, COS','₴4,270','new','New','','40 min left'),
        ('#007','','Artem Bilyk','c3',3,'Zara','price not set','new','New','','48 min left')]
def rrow(r):
    num, cls, name, c, n, shops, amt, st, stt, tc, tm = r
    a = f'<span class="sub">{amt}</span>' if 'not' in amt else amt
    return f'<tr class="{cls}"><td><div class="row" style="gap:14px"><div style="width:82px">{thumbs(P[num][:3], 32, 40)}</div><div><div class="num" style="font-size:16px">{num}</div><div class="sub" style="font-size:12px">{n} item{"s" if n > 1 else ""}</div></div></div></td><td><div class="who"><div class="ava {c}" style="width:30px;height:30px;font-size:11px">{ini(name)}</div>{name}</div></td><td class="sub">{shops}</td><td>{a}</td><td><span class="st {st}">{stt}</span></td><td><span class="timer {tc}">{tm}</span></td></tr>'
main1 = f'''
<div class="row"><h1 class="grow">Requests <span class="cnt">1,001</span></h1><button class="btn pri big">Take next request</button></div>
<div class="tabs"><a class="on">All <b>1,001</b></a><a>New <b>12</b></a><a class="red">Overdue <b>2</b></a></div>
<div class="card" style="overflow:hidden"><table>
<tr><th>Request</th><th>Client</th><th>Stores</th><th>Amount</th><th>Status</th><th>Due</th></tr>
{''.join(rrow(r) for r in rows)}
</table></div>'''
save('01-requests.html', shell('Requests', 'Requests', main1))

# ---------- 02 Request card ----------
css2 = '''
.cols { display: flex; gap: 20px; align-items: flex-start; }
.left { flex: 1; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.right { width: 330px; flex: none; display: flex; flex-direction: column; gap: 16px; }
.it { display: flex; gap: 16px; padding: 18px 20px; border-bottom: 1px solid var(--line); }
.it:last-child { border-bottom: 0; }
.it .name { font-size: 15.5px; font-weight: 600; }
.it .spec { margin: 6px 0 8px; font-size: 14px; }
.it .spec span { color: var(--faint); }
.it .q { font-size: 13px; color: var(--muted); font-style: italic; }
.it .acts { display: flex; flex-direction: column; gap: 8px; align-items: flex-end; flex: none; }
.rule { margin-top: 12px; border: 1px solid rgba(255,122,122,.3); background: var(--bad-bg); border-radius: 12px; padding: 10px 12px; font-size: 13px; }
.rule.ok { border-color: rgba(114,208,138,.3); background: var(--ok-bg); }
.rule .h { display: flex; gap: 6px; align-items: center; font-weight: 600; color: var(--bad); }
.rule.ok .h { color: var(--ok); }
.rule .d { color: var(--muted); margin: 2px 0 8px 20px; }
.rule .b { display: flex; gap: 8px; margin-left: 20px; }
.kv { display: flex; justify-content: space-between; padding: 5px 0; font-size: 13.5px; }
.kv span { color: var(--muted); }
.kv.total { border-top: 1px solid var(--line); margin-top: 6px; padding-top: 12px; font-size: 18px; font-weight: 600; }
.com { font-size: 13px; margin-bottom: 12px; }
.com b { font-weight: 600; } .com small { color: var(--faint); margin-left: 6px; }
.input { border: 1px solid var(--line-2); border-radius: 10px; padding: 9px 12px; color: var(--faint); background: var(--bg); font-size: 13px; }
'''
def item(ph, name, shop, size, qty, price, comment, status, rule=''):
    return f'''<div class="it">{photo(ph, 80, 100)}<div class="grow">
<div class="row" style="gap:8px"><div class="name">{name}</div><span class="tag">{shop}</span></div>
<div class="spec"><span>Size</span> {size} &nbsp;·&nbsp; <span>Qty</span> {qty} &nbsp;·&nbsp; {price}</div>
<div class="q">{comment}</div>{rule}</div>
<div class="acts">{status}<button class="btn">Open in store {ic('ext', 14)}</button></div></div>'''
r_oos = f'''<div class="rule"><div class="h">{ic('alert', 14)}Out of stock in M</div><div class="d">Rule: cancel the item and refund ₴3,999. The client gets “Item no longer available, money refunded”.</div>
<div class="b"><button class="btn sm pri">Cancel &amp; refund</button><button class="btn sm">Check other stores</button></div></div>'''
r_price = f'''<div class="rule ok"><div class="h">{ic('alert', 14)}Price up ₴50 (+3.6%)</div><div class="d">Within the 5% tolerance — Fitkit covers the difference, the client sees nothing.</div></div>'''
items = (item('stripe', 'Striped sweater', 'Zara', 'L', '1', '₴1,799', '“One size up, I like a loose fit”', '<span class="st ok">Checked</span>')
 + item('jacket-black', 'Black jacket', 'Zara', 'M', '1', '₴3,999', '“Need it by Nov 25”', '<span class="st bad">Sold out</span>', r_oos)
 + item('jeans-black', 'Wide-leg jeans', 'H&amp;M', 'W28 L32', '1', '₴1,399 → ₴1,449', '“Dark, like in the photo”', '<span class="st ok">Checked</span>', r_price))
main2 = f'''
<div class="row">
  <button class="btn iconbtn">{ic('back')}</button>
  <div class="grow"><div class="row" style="gap:10px"><h1 class="num" style="font-size:28px">#001</h1><span class="st wait">In progress</span></div>
  <div class="sub">Maria Lebedenko · received Nov 21, 08:40 · <span class="btn link">History</span></div></div>
  <button class="btn iconbtn">{ic('more')}</button>
</div>
<div class="cols">
  <div class="left">
    <div class="card">{items}</div>
    <div class="card"><div class="bd row" style="gap:30px;align-items:flex-start">
      <div><div class="lbl">Deliver to</div>Kyiv, 12 Velyka Vasylkivska St, apt 48<div class="sub">Maria Lebedenko · +380 67 ••• 45 12 · Nova Poshta courier</div></div>
      <span class="grow"></span><span class="btn link">{ic('copy', 14)} Copy</span>
    </div></div>
  </div>
  <div class="right">
    <div class="card"><div class="bd">
      <div class="kv"><span>Owner</span>Anna Koval</div>
      <div class="kv"><span>Due</span><span style="color:var(--wait);font-weight:600">1h 20m left</span></div>
      <div class="kv"><span>Client sees</span>Preparing your order</div>
      <div class="kv" style="margin-top:8px"><span>Client paid</span>₴7,777</div>
      <div class="kv"><span>Refund · jacket</span>−₴3,999</div>
      <div class="kv"><span>Fitkit fee</span>₴580</div>
      <div class="kv"><span>Fitkit covers</span>₴50</div>
      <div class="kv total"><span style="color:var(--text)">To buy</span><span class="num" style="color:var(--text)">₴3,248</span></div>
      <button class="btn pri big" style="width:100%;margin-top:16px">Move to “Purchased” →</button>
      <div class="row" style="gap:8px;margin-top:8px"><button class="btn" style="flex:1">Problem</button><button class="btn" style="flex:1">Hand over</button></div>
      <div style="text-align:center;margin-top:12px"><span class="btn link" style="color:var(--faint);font-weight:500">Cancel order</span></div>
    </div></div>
    <div class="card"><div class="bd">
      <div class="lbl">Team notes</div>
      <div class="com"><b>Iryna R.</b><small>09:20</small><div>Massimo Dutti has a similar jacket in M — check before refunding.</div></div>
      <div class="input">Add a note…</div>
    </div></div>
  </div>
</div>'''
save('02-order-card.html', shell('Requests', 'Request #001', main2, css2))

# ---------- 03 Current orders ----------
css3 = '''
.board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; align-items: start; }
.col { display: flex; flex-direction: column; gap: 10px; }
.colh { display: flex; align-items: center; gap: 8px; padding: 0 4px 4px; font-weight: 600; }
.colh .dot { width: 8px; height: 8px; border-radius: 50%; }
.colh b { font-weight: 500; color: var(--faint); }
.oc { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.oc.prob { box-shadow: inset 3px 0 0 var(--bad); }
.oc.wt { box-shadow: inset 3px 0 0 var(--wait); }
.oc .t { margin-left: auto; font-size: 12.5px; font-weight: 600; color: var(--muted); white-space: nowrap; }
.oc .t.red { color: var(--bad); } .oc .t.org { color: var(--wait); }
.note { font-size: 12.5px; color: var(--muted); }
.note.red { color: var(--bad); } .note.org { color: var(--wait); }
'''
def oc(num, ph, client, info, time, tc='', note=None, unread=False):
    cls = 'prob' if note and note[0] == 'red' else ('wt' if note else '')
    n = f'<div class="note {note[0]}">{note[1]}</div>' if note else ''
    u = '<span class="badge">1</span>' if unread else ''
    return f'''<div class="oc {cls}"><div class="row" style="gap:10px">{thumbs(ph)}<span class="num" style="font-size:16px">{num}</span>{u}<span class="t {tc}">{time}</span></div>
<div><div style="font-size:13.5px">{client}</div><div class="sub" style="font-size:12.5px">{info}</div></div>{n}</div>'''
def col(name, c, cnt, cards): return f'<div class="col"><div class="colh"><span class="dot" style="background:{c}"></span>{name} <b>{cnt}</b></div>{cards}</div>'
cw = (oc('#001', ['stripe','jacket-black','jeans-black'], 'Maria Lebedenko', '3 items · ₴7,777', '1h 20m', '', ('red', 'Jacket sold out — apply rule'))
 + oc('#008', ['jacket-black'], 'Olena Smyrnova', '1 item · ₴3,999', '2h')
 + oc('#0993', ['hoodie','sweatpants'], 'Artem Bilyk', '2 items · ₴5,380', '2h 40m')
 + oc('#0990', ['scarf'], 'Kseniia Orlyk', '1 item · ₴1,599', '3h')
 + oc('#0987', ['sweater-grey','jeans','loafers'], 'Olha Petrenko', '3 items · ₴12,480', '3h 30m'))
cwa = (oc('#0995', ['sneakers'], 'Ihor Sokolenko', '1 item · ₴5,899', '6h', 'org', ('org', 'Price +12% — confirmation sent'))
 + oc('#0981', ['stripe','sweatpants2'], 'Pavlo Tykhonenko', '2 items · ₴4,480', '26h', 'red', ('red', 'No answer 26h — auto-refund at 24h'))
 + oc('#0976', ['jeans-black'], 'Daria Vovk', '1 item · ₴1,899', '2h', 'org', ('org', 'Price +9% — confirmation sent')))
cp = (oc('#0968', ['loafers'], 'Olena Smyrnova', 'At warehouse · Nova Poshta', 'today')
 + oc('#0951', ['sneakers'], 'Pavlo Tykhonenko', 'Waiting for tracking · Nike', '3 days', 'red', ('red', 'No tracking for 3 days'))
 + oc('#0947', ['sweater-grey','scarf'], 'Kseniia Orlyk', 'In transit · Ukrposhta', '5 days', 'red', ('red', 'No movement for 5 days'))
 + oc('#0939', ['hoodie'], 'Artem Bilyk', 'In transit · Meest', 'yesterday'))
cs = (oc('#0932', ['jeans','stripe'], 'Olha Petrenko', 'Nova Poshta · due Nov 23', 'yesterday')
 + oc('#0918', ['jacket-black'], 'Maria Lebedenko', 'Courier delivers today', 'today'))
main3 = f'''
<div class="row"><h1 class="grow">Current orders <span class="cnt">14</span></h1><div class="tabs"><a class="on">Mine</a><a>All</a></div></div>
<div class="board">{col('In progress', 'var(--muted)', 5, cw)}{col('Awaiting confirmation', 'var(--wait)', 3, cwa)}{col('Purchased', 'var(--info)', 4, cp)}{col('Shipped', 'var(--ok)', 2, cs)}</div>'''
save('03-current-orders.html', shell('Current orders', 'Current orders', main3, css3))

# ---------- 04 Clients (support) ----------
css4 = '''
.main { padding: 0; gap: 0; }
.wrap { display: flex; height: 904px; }
.list { width: 290px; border-right: 1px solid var(--line); flex: none; display: flex; flex-direction: column; }
.list .hd2 { padding: 22px 18px 12px; }
.list .s2 { margin: 0 18px 12px; height: 34px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 12px; color: var(--faint); font-size: 13px; background: var(--bg); }
.list .tabs { padding: 0 14px 10px; }
.c { display: flex; gap: 10px; padding: 12px 18px; }
.c.on { background: var(--clay-veil); }
.c .t { flex: 1; min-width: 0; font-size: 13px; }
.c .t b { display: flex; justify-content: space-between; font-weight: 600; }
.c .t b small { color: var(--faint); font-weight: 400; font-size: 11.5px; }
.c .t p { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.chat { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.chat .head { display: flex; align-items: center; gap: 12px; padding: 16px 24px; border-bottom: 1px solid var(--line); }
.msgs { flex: 1; padding: 24px; display: flex; flex-direction: column; gap: 12px; }
.day { align-self: center; font-size: 11.5px; color: var(--faint); }
.m { max-width: 64%; padding: 10px 14px; border-radius: 16px; font-size: 14px; line-height: 1.45; }
.m small { display: block; font-size: 11px; color: var(--faint); margin-top: 4px; }
.m.cl { background: var(--panel); border: 1px solid var(--line); align-self: flex-start; border-bottom-left-radius: 5px; }
.m.me { background: rgba(240,174,194,.13); border: 1px solid rgba(240,174,194,.22); align-self: flex-end; border-bottom-right-radius: 5px; }
.sys { align-self: center; font-size: 12px; color: var(--muted); background: var(--panel); border: 1px solid var(--line); border-radius: 999px; padding: 4px 12px; }
.quick { display: flex; gap: 6px; padding: 0 24px 10px; }
.quick span { font-size: 12px; border: 1px solid var(--line-2); border-radius: 999px; padding: 3px 10px; color: var(--muted); }
.composer { border-top: 1px solid var(--line); padding: 14px 24px; display: flex; gap: 10px; align-items: center; }
.composer .in { flex: 1; height: 42px; border: 1px solid var(--line-2); border-radius: 12px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); background: var(--bg); }
.info { width: 310px; border-left: 1px solid var(--line); flex: none; padding: 22px 20px; display: flex; flex-direction: column; gap: 20px; }
.kv2 { font-size: 13.5px; padding: 3px 0; }
.kv2 span { color: var(--muted); display: inline-block; width: 70px; }
.ord { display: flex; align-items: center; gap: 8px; font-size: 13px; padding: 6px 0; }
'''
clients = [('Maria Lebedenko','c2','#001','When will my order arrive?','09:41',True,True),('Ihor Sokolenko','c4','#0995','Can I change the delivery address?','09:20',True,False),('Olha Petrenko','c3','#0932','Parcel says delivered but…','09:12',True,False),
           ('Daria Vovk','c5','#0976','Resolved · refund received','Nov 22',False,False),('Pavlo Tykhonenko','c2','#0981','Resolved · size question','Nov 21',False,False),
           ('Olena Smyrnova','c5','#0968','—','',False,False),('Kseniia Orlyk','c4','#0990','—','',False,False),('Artem Bilyk','c3','#0993','—','',False,False)]
def crow(c):
    n, col_, num, last, t, unread, on = c
    b = '<span class="badge" style="align-self:center">1</span>' if unread else ''
    return f'<div class="c {"on" if on else ""}"><div class="ava {col_}">{ini(n)}</div><div class="t"><b>{n}<small>{t}</small></b><p><span style="color:var(--clay)">{num}</span> · {last}</p></div>{b}</div>'
main4 = f'''
<div class="wrap">
  <div class="list">
    <div class="hd2"><h1>Clients</h1></div>
    <div class="s2">Find a client…</div>
    <div class="tabs"><a>All</a><a class="on">Open tickets <b>3</b></a></div>
    {''.join(crow(c) for c in clients)}
  </div>
  <div class="chat">
    <div class="head"><div class="grow"><b>Support ticket · Maria Lebedenko</b><div class="sub">Order #001 · client sees “Preparing your order”</div></div><button class="btn">Open order</button><button class="btn pri">Resolve</button></div>
    <div class="msgs">
      <div class="day">Today</div>
      <div class="sys">Item cancelled automatically: Black jacket · ₴3,999 refunded · client notified</div>
      <div class="m cl">Hi! I got a refund for the jacket, but when will the rest of my order arrive?<small>Maria · 09:41</small></div>
      <div class="m me">Hi Maria! The sweater and jeans are being prepared and will ship by Nov 24. You’ll get a Nova Poshta tracking number as soon as they leave our warehouse.<small>Fitkit Support · draft</small></div>
    </div>
    <div class="quick"><span>Order status</span><span>Refund info</span><span>Delivery date</span><span>Change address</span></div>
    <div class="composer"><div class="in">Reply as Fitkit Support…</div><button class="btn pri" style="height:42px">{ic('send')}Send</button></div>
  </div>
  <div class="info">
    <div><div class="lbl">Contacts</div>
      <div class="kv2"><span>Telegram</span>@maria_l</div><div class="kv2"><span>Phone</span>+380 67 ••• 45 12 <span class="btn link" style="width:auto">Show</span></div></div>
    <div><div class="lbl">Address</div><div style="font-size:13.5px">Kyiv, 12 Velyka Vasylkivska St, apt 48</div><div class="sub">Nova Poshta courier</div></div>
    <div><div class="lbl">Preferences</div>
      <div class="kv2"><span>Sizes</span>S–M · W28 L32 · 38</div><div class="kv2"><span>Stores</span>Zara, COS, Massimo Dutti</div><div class="kv2"><span>Dislikes</span><span style="color:var(--bad);width:auto">synthetics, loud prints</span></div>
      <div class="sub" style="margin-top:6px;font-size:12.5px">Zara runs small for her — take one size up.</div></div>
    <div><div class="lbl">Orders · 7</div>
      <div class="ord">{thumbs(['stripe','jeans-black'], 24, 30)}<span class="num">#001</span><span class="grow"></span><span class="st wait">In progress</span></div>
      <div class="ord">{thumbs(['sweater-grey'], 24, 30)}<span class="num">#0874</span><span class="grow"></span><span class="st ok">Delivered</span></div>
      <div class="ord">{thumbs(['loafers','scarf'], 24, 30)}<span class="num">#0812</span><span class="grow"></span><span class="st ok">Delivered</span></div>
    </div>
  </div>
</div>'''
save('04-clients.html', shell('Clients', 'Clients', main4, css4))

# ---------- 05 Tracking (two legs) ----------
css5 = '''
.cols { display: flex; gap: 20px; align-items: flex-start; }
.track { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12.5px; color: var(--muted); }
.leg { font-size: 11px; font-weight: 600; border-radius: 999px; padding: 1px 8px; border: 1px solid var(--line-2); color: var(--muted); }
.leg.in { color: var(--info); border-color: rgba(143,178,255,.35); } .leg.out { color: var(--ok); border-color: rgba(114,208,138,.35); }
.src { font-size: 11px; color: var(--faint); }
.panel { width: 350px; flex: none; }
.tl { position: relative; padding-left: 22px; margin-bottom: 6px; }
.tl:before { content: ""; position: absolute; left: 5px; top: 6px; bottom: 6px; width: 2px; background: var(--line-2); }
.ev { position: relative; padding-bottom: 12px; font-size: 13px; }
.ev:before { content: ""; position: absolute; left: -21px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--panel); border: 2px solid var(--faint); }
.ev.d:before { background: var(--clay); border-color: var(--clay); }
.ev small { display: block; color: var(--faint); font-size: 11.5px; }
.ev.f { color: var(--faint); }
.seen { background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font-size: 13px; margin: 6px 0 14px; }
.red { color: var(--bad); }
'''
ship = [('#0968',['loafers'],'Massimo Dutti','in','Nova Poshta · 2045 0088 1244 71','email','Arrived at warehouse','today, 10:12','on',False),
        ('#0972',['hoodie','sweatpants'],'AliExpress','in','Cainiao · LP00 4821 7730 15UA','email','Left sorting center, Shenzhen','today, 06:30','',False),
        ('#0951',['sneakers'],'Nike','in','— no tracking yet','','No tracking for 3 days','Nov 18','late',True),
        ('#0947',['sweater-grey','scarf'],'COS','in','DHL · 4821 0093 77','manual','No movement for 5 days','Nov 16','late',True),
        ('#0932',['jeans','stripe'],'—','out','Nova Poshta · 2045 0099 8211 67','created','On the way to client','yesterday','',False),
        ('#0918',['jacket-black'],'—','out','Nova Poshta · 2045 0055 3000 81','created','Courier delivers today','today, 09:55','',False)]
def srow(s):
    num, ph, shop, leg, tr, src, ev, t, cls, bad = s
    lg = '<span class="leg in">Store → warehouse</span>' if leg == 'in' else '<span class="leg out">Warehouse → client</span>'
    srcs = {'email': 'from store email', 'manual': 'entered by buyer', 'created': 'created via Nova Poshta API', '': ''}[src]
    e = f'<span class="red">{ev}</span>' if bad else ev
    return f'<tr class="{cls}"><td><div class="row" style="gap:12px"><div style="width:58px">{thumbs(ph, 30, 38)}</div><span class="num" style="font-size:15px">{num}</span></div></td><td>{lg}<div style="margin-top:4px">{shop if shop != "—" else ""}</div></td><td><div class="track">{tr}</div><div class="src">{srcs}</div></td><td>{e}<div class="sub" style="font-size:12px">{t}</div></td></tr>'
main5 = f'''
<h1>Tracking <span class="cnt">71</span></h1>
<div class="tabs"><a class="on">All <b>71</b></a><a>Store → warehouse <b>38</b></a><a>At warehouse <b>12</b></a><a>Warehouse → client <b>21</b></a><a class="red">Problems <b>2</b></a></div>
<div class="cols">
  <div class="card grow" style="overflow:hidden"><table><tr><th>Order</th><th>Leg</th><th>Carrier · tracking</th><th>Last event</th></tr>{''.join(srow(s) for s in ship)}</table></div>
  <div class="card panel"><div class="bd">
    <div class="row" style="gap:12px;margin-bottom:14px">{photo('loafers', 52, 66)}<div class="grow"><b class="num" style="font-size:17px">#0968</b><div style="font-size:13.5px">Leather loafers · 38</div><div class="sub">Olena Smyrnova</div></div></div>
    <div class="lbl">1 · Store → warehouse</div>
    <div class="tl">
      <div class="ev d"><b>Purchased at Massimo Dutti</b><small>Nov 17, 12:40</small></div>
      <div class="ev d"><b>Handed to Nova Poshta</b><small>tracking from store email · Nov 18</small></div>
      <div class="ev d"><b>Arrived at warehouse</b><small>checked, 3 photos · today, 10:12</small></div>
    </div>
    <div class="lbl">2 · Warehouse → client</div>
    <div class="tl"><div class="ev f"><b>Not shipped yet</b><small>Nova Poshta shipment is created by the app</small></div></div>
    <div class="lbl">Client sees</div>
    <div class="seen">“Preparing your order” · arrives by Nov 25</div>
    <button class="btn pri big" style="width:100%">Create shipment &amp; ship →</button>
  </div></div>
</div>'''
save('05-tracking.html', shell('Tracking', 'Tracking', main5, css5))

# ---------- 06 Client app ----------
page6 = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fitkit — in the Fitkit app</title>
<link rel="stylesheet" href="styles.css">
<style>
.stage {{ width: 1440px; height: 900px; display: flex; gap: 56px; padding: 60px 80px; background: var(--bg); align-items: center; }}
.phone {{ width: 340px; height: 740px; background: #000; border: 1px solid #2a2f37; border-radius: 46px; padding: 12px; box-shadow: 0 0 60px -20px rgba(240,174,194,.25); flex: none; }}
.screen {{ background: var(--bg); height: 100%; border-radius: 36px; overflow: hidden; display: flex; flex-direction: column; }}
.ptop {{ padding: 40px 18px 14px; display: flex; gap: 10px; align-items: center; }}
.pb {{ padding: 0 16px; display: flex; flex-direction: column; gap: 12px; flex: 1; }}
.cardp {{ background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 14px; font-size: 13.5px; }}
.steps {{ display: flex; flex-direction: column; gap: 10px; }}
.sp {{ display: flex; gap: 10px; align-items: center; font-size: 13.5px; color: var(--faint); }}
.sp i {{ width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--faint); flex: none; }}
.sp.d {{ color: var(--text); }} .sp.d i {{ background: var(--clay); border-color: var(--clay); }}
.sp.c {{ color: var(--text); font-weight: 600; }} .sp.c i {{ border-color: var(--clay); box-shadow: 0 0 0 4px rgba(240,174,194,.2); }}
.it {{ display: flex; gap: 10px; align-items: center; font-size: 13px; }}
.alert {{ border-color: rgba(240,180,92,.4); }}
.btns {{ display: flex; gap: 8px; margin-top: 10px; }}
.btns .btn {{ flex: 1; }}
.nt {{ display: flex; gap: 10px; padding: 12px 0; border-bottom: 1px solid var(--line); font-size: 13px; }}
.nt:last-child {{ border-bottom: 0; }}
.nt .dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--clay); margin-top: 6px; flex: none; }}
.nt small {{ display: block; color: var(--faint); font-size: 11.5px; margin-top: 2px; }}
.help {{ text-align: center; color: var(--clay); font-weight: 600; font-size: 13.5px; padding: 14px 0 26px; }}
.msg {{ background: var(--panel); border: 1px solid var(--line); border-radius: 14px 14px 14px 4px; padding: 9px 12px; font-size: 13px; max-width: 85%; }}
.msg.me {{ align-self: flex-end; background: var(--clay-veil); border-color: rgba(240,174,194,.3); border-radius: 14px 14px 4px 14px; }}
.sysm {{ align-self: center; text-align: center; font-size: 11.5px; color: var(--faint); }}
.inp {{ margin: 0 14px 22px; height: 40px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); font-size: 13px; }}
.expl {{ max-width: 420px; display: flex; flex-direction: column; gap: 14px; }}
.expl h1 {{ font-size: 28px; line-height: 1.2; }}
.expl p {{ color: var(--muted); font-size: 15px; }}
</style></head>
<body><div class="app" style="display:block;min-height:900px"><div class="stage">
  <div class="phone"><div class="screen">
    <div class="ptop"><img src="assets/logo-mark.png" style="width:28px;height:28px;filter:invert(1)"><b class="serif" style="font-size:20px;font-weight:600">Order #001</b></div>
    <div class="pb">
      <div class="cardp"><div class="steps">
        <div class="sp d"><i></i>Order confirmed</div><div class="sp c"><i></i>Preparing your order</div><div class="sp"><i></i>Shipped</div><div class="sp"><i></i>Delivered · by Nov 25</div>
      </div></div>
      <div class="cardp">
        <div class="it">{photo('stripe', 36, 46)}<div class="grow">Striped sweater · L</div>₴1,799</div>
        <div class="it" style="margin-top:8px">{photo('jeans-black', 36, 46)}<div class="grow">Wide-leg jeans · W28</div>₴1,399</div>
        <div class="it" style="margin-top:8px;opacity:.55">{photo('jacket-black', 36, 46)}<div class="grow">Black jacket · M<div class="sub" style="font-size:12px">Sold out · ₴3,999 refunded</div></div><s>₴3,999</s></div>
      </div>
    </div>
    <div class="help">Chat with Fitkit Support</div>
  </div></div>
  <div class="phone"><div class="screen">
    <div class="ptop"><img src="assets/logo-mark.png" style="width:28px;height:28px;filter:invert(1)"><div><b style="font-size:16px">Fitkit Support</b><div class="sub" style="font-size:11.5px">Chat in the Fitkit app</div></div></div>
    <div class="pb" style="gap:10px">
      <div class="sysm">Order #0995</div>
      <div class="cardp alert"><b>Price changed</b><div class="sub" style="margin-top:4px">Sneakers: ₴5,899 → ₴6,599. Keep the item at the new price?</div>
        <div class="btns"><button class="btn pri sm">Confirm</button><button class="btn sm">Remove item</button></div></div>
      <div class="msg me">Can I still change the delivery address?</div>
      <div class="msg">Sure! Send the new Nova Poshta branch and we’ll update it before shipping. — Fitkit Support</div>
      <div class="sysm">Order #001 · Black jacket (M) sold out · ₴3,999 refunded</div>
    </div>
    <div class="inp">Write a message…</div>
  </div></div>
  <div class="expl">
    <span class="tag" style="align-self:flex-start">Inside the existing Fitkit app</span>
    <h1>Order status and support chat — in the app clients already use</h1>
    <p>No separate client app. The Fitkit app gets an order screen with simple statuses and a chat with Fitkit Support. Price confirmations and refunds arrive in the same chat. No buyer names, no store tracking.</p>
  </div>
</div></div></body></html>'''
save('06-client-app.html', page6)
