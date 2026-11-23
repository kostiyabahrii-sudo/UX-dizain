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
rows = [('#001','late','Maria Lebedenko','c2',3,'Zara, H&amp;M','₴6,378','bad','Overdue','red','−42 min'),
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
.warn { margin-top: 10px; font-size: 13px; color: var(--bad); display: flex; gap: 6px; align-items: center; }
.kv { display: flex; justify-content: space-between; padding: 5px 0; font-size: 13.5px; }
.kv span { color: var(--muted); }
.kv.total { border-top: 1px solid var(--line); margin-top: 6px; padding-top: 12px; font-size: 18px; font-weight: 600; }
.com { font-size: 13px; margin-bottom: 12px; }
.com b { font-weight: 600; } .com small { color: var(--faint); margin-left: 6px; }
.input { border: 1px solid var(--line-2); border-radius: 10px; padding: 9px 12px; color: var(--faint); background: var(--bg); font-size: 13px; }
'''
def item(ph, name, shop, size, qty, price, comment, status, warn=''):
    pr = price if price else '<span>price not set</span>'
    w = f'<div class="warn">{ic("alert", 14)}{warn} <span class="btn link" style="margin-left:6px">Ask client</span></div>' if warn else ''
    return f'''<div class="it">{photo(ph, 80, 100)}<div class="grow">
<div class="row" style="gap:8px"><div class="name">{name}</div><span class="tag">{shop}</span></div>
<div class="spec"><span>Size</span> {size} &nbsp;·&nbsp; <span>Qty</span> {qty} &nbsp;·&nbsp; {pr}</div>
<div class="q">{comment}</div>{w}</div>
<div class="acts">{status}<button class="btn">Open in store {ic('ext', 14)}</button></div></div>'''
items = (item('stripe', 'Striped sweater', 'Zara', 'L', '1', '₴1,799', '“One size up, I like a loose fit”', '<span class="st ok">Checked</span>')
 + item('jacket-black', 'Black jacket', 'Zara', 'M', '1', '₴3,999', '“Need it by Nov 25. If no M — S is fine”', '<span class="st bad">Size missing</span>', 'No size M in stock')
 + item('jeans-black', 'Wide-leg jeans', 'H&amp;M', 'W28 L32', '1', '', '“Dark, like in the photo. Couldn’t find the price”', '<span class="st wait">Checking</span>'))
main2 = f'''
<div class="row">
  <button class="btn iconbtn">{ic('back')}</button>
  <div class="grow"><div class="row" style="gap:10px"><h1 class="num" style="font-size:28px">#001</h1><span class="st wait">In progress</span></div>
  <div class="sub">Maria Lebedenko · received Nov 21, 08:40 · <span class="btn link">History</span></div></div>
  <button class="btn">{ic('msg')}Message client</button><button class="btn iconbtn">{ic('more')}</button>
</div>
<div class="cols">
  <div class="left">
    <div class="card">{items}</div>
    <div class="card"><div class="bd row" style="gap:30px;align-items:flex-start">
      <div><div class="lbl">Deliver to</div>Kyiv, 12 Velyka Vasylkivska St, apt 48<div class="sub">Maria Lebedenko · +380 67 ••• 45 12 · courier 10:00–18:00</div></div>
      <span class="grow"></span><span class="btn link">{ic('copy', 14)} Copy</span>
    </div></div>
  </div>
  <div class="right">
    <div class="card"><div class="bd">
      <div class="kv"><span>Owner</span>Anna Koval</div>
      <div class="kv"><span>Due</span><span style="color:var(--wait);font-weight:600">1h 20m left</span></div>
      <div class="kv" style="margin-top:8px"><span>Items (2 priced)</span>₴5,798</div>
      <div class="kv"><span>Fitkit fee</span>₴580</div>
      <div class="kv total"><span style="color:var(--text)">Total</span><span class="num" style="color:var(--text)">₴6,378</span></div>
      <button class="btn pri big" style="width:100%;margin-top:16px">Move to “Purchased” →</button>
      <div class="row" style="gap:8px;margin-top:8px"><button class="btn" style="flex:1">Waiting for client</button><button class="btn" style="flex:1">Problem</button></div>
      <div style="text-align:center;margin-top:12px"><span class="btn link" style="color:var(--faint);font-weight:500">Cancel order</span></div>
    </div></div>
    <div class="card"><div class="bd">
      <div class="lbl">Team notes</div>
      <div class="com"><b>Iryna R.</b><small>09:20</small><div>If S is also gone — suggest Massimo Dutti, she has bought there before.</div></div>
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
cw = (oc('#001', ['stripe','jacket-black','jeans-black'], 'Maria Lebedenko', '3 items · ₴6,378', '1h 20m', '', ('red', 'No size M — asked in chat'), True)
 + oc('#008', ['jacket-black'], 'Olena Smyrnova', '1 item · ₴3,999', '2h')
 + oc('#0993', ['hoodie','sweatpants'], 'Artem Bilyk', '2 items · ₴5,380', '2h 40m')
 + oc('#0990', ['scarf'], 'Kseniia Orlyk', '1 item · ₴1,599', '3h')
 + oc('#0987', ['sweater-grey','jeans','loafers'], 'Olha Petrenko', '3 items · ₴12,480', '3h 30m'))
cwa = (oc('#0995', ['sneakers'], 'Ihor Sokolenko', '1 item · ₴5,899', '6h', 'org', ('org', 'Asked about ₴290 extra'), True)
 + oc('#0981', ['stripe','sweatpants2'], 'Pavlo Tykhonenko', '2 items · ₴4,480', '26h', 'red', ('red', 'Client silent for over a day'))
 + oc('#0976', ['jeans-black'], 'Daria Vovk', '1 item · price ?', '2h', 'org', ('org', 'Asked: W29 or W30?')))
cp = (oc('#0968', ['loafers'], 'Olena Smyrnova', 'At warehouse · Nova Poshta', 'today')
 + oc('#0951', ['sneakers'], 'Pavlo Tykhonenko', 'Waiting for tracking · Nike', '3 days', 'red', ('red', 'No tracking for 3 days'))
 + oc('#0947', ['sweater-grey','scarf'], 'Kseniia Orlyk', 'In transit · Ukrposhta', '5 days', 'red', ('red', 'No movement for 5 days'))
 + oc('#0939', ['hoodie'], 'Artem Bilyk', 'In transit · Meest', 'yesterday'))
cs = (oc('#0932', ['jeans','stripe'], 'Olha Petrenko', 'Nova Poshta · due Nov 23', 'yesterday')
 + oc('#0918', ['jacket-black'], 'Maria Lebedenko', 'Courier delivers today', 'today'))
main3 = f'''
<div class="row"><h1 class="grow">Current orders <span class="cnt">14</span></h1><div class="tabs"><a class="on">Mine</a><a>All</a></div></div>
<div class="board">{col('In progress', 'var(--muted)', 5, cw)}{col('Waiting for client', 'var(--wait)', 3, cwa)}{col('Purchased', 'var(--info)', 4, cp)}{col('Shipped', 'var(--ok)', 2, cs)}</div>'''
save('03-current-orders.html', shell('Current orders', 'Current orders', main3, css3))

# ---------- 04 Clients (with chat) ----------
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
.prod { display: flex; gap: 10px; background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 8px; margin-top: 8px; font-size: 12.5px; }
.composer { border-top: 1px solid var(--line); padding: 14px 24px; display: flex; gap: 10px; align-items: center; }
.composer .in { flex: 1; height: 42px; border: 1px solid var(--line-2); border-radius: 12px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); background: var(--bg); }
.info { width: 310px; border-left: 1px solid var(--line); flex: none; padding: 22px 20px; display: flex; flex-direction: column; gap: 20px; }
.kv2 { font-size: 13.5px; padding: 3px 0; }
.kv2 span { color: var(--muted); display: inline-block; width: 70px; }
.ord { display: flex; align-items: center; gap: 8px; font-size: 13px; padding: 6px 0; }
'''
clients = [('Maria Lebedenko','c2','#001','Let’s go with S, thanks!','09:41',True,True),('Ihor Sokolenko','c4','#002','Why did the price go up?','09:20',True,False),('Olha Petrenko','c3','#003','Sent one more link','09:12',True,False),
           ('Daria Vovk','c5','#004','You: Checking stock, back soon…','08:55',False,False),('Pavlo Tykhonenko','c2','#005','You: Tracking number tomorrow','yesterday',False,False),
           ('Olena Smyrnova','c5','#008','Thanks, everything arrived!','yesterday',False,False),('Kseniia Orlyk','c4','#0990','You: Bought, waiting for tracking','Nov 20',False,False),('Artem Bilyk','c3','#0993','Ok, thank you','Nov 19',False,False)]
def crow(c):
    n, col_, num, last, t, unread, on = c
    b = '<span class="badge" style="align-self:center">1</span>' if unread else ''
    return f'<div class="c {"on" if on else ""}"><div class="ava {col_}">{ini(n)}</div><div class="t"><b>{n}<small>{t}</small></b><p><span style="color:var(--clay)">{num}</span> · {last}</p></div>{b}</div>'
main4 = f'''
<div class="wrap">
  <div class="list">
    <div class="hd2"><h1>Clients</h1></div>
    <div class="s2">Find a client…</div>
    <div class="tabs"><a class="on">All</a><a class="red">Unread <b>3</b></a></div>
    {''.join(crow(c) for c in clients)}
  </div>
  <div class="chat">
    <div class="head"><div class="ava c2">ML</div><div class="grow"><b>Maria Lebedenko</b><div class="sub">Telegram · online 2 min ago</div></div><span class="tag">#001 · In progress</span><button class="btn">Open request</button></div>
    <div class="msgs">
      <div class="day">Today</div>
      <div class="m cl">Hi! I sent 3 items, please take a look 🙏<small>08:40</small></div>
      <div class="m me">Hi Maria! I’m Anna, your buyer. Checking stock and sizes, I’ll be back shortly.<small>09:05</small></div>
      <div class="m me">Unfortunately the black jacket is out of stock in M. S is the same price — shall we take S?
        <div class="prod">{photo('jacket-black', 40, 50)}<div><b>Black jacket</b><div class="sub" style="font-size:12px">Zara · S · ₴3,999</div><div style="color:var(--clay);font-size:12px">zara.com ↗</div></div></div><small>09:30</small></div>
      <div class="m cl">Let’s go with S, thanks!<small>09:41</small></div>
    </div>
    <div class="composer"><button class="btn iconbtn" style="height:42px;width:42px">{ic('clip')}</button><div class="in">Message Maria…</div><button class="btn pri" style="height:42px">{ic('send')}Send</button></div>
  </div>
  <div class="info">
    <div><div class="lbl">Contacts</div>
      <div class="kv2"><span>Telegram</span>@maria_l</div><div class="kv2"><span>Phone</span>+380 67 ••• 45 12 <span class="btn link" style="width:auto">Show</span></div></div>
    <div><div class="lbl">Address</div><div style="font-size:13.5px">Kyiv, 12 Velyka Vasylkivska St, apt 48</div><div class="sub">Courier, 10:00–18:00</div></div>
    <div><div class="lbl">Preferences</div>
      <div class="kv2"><span>Sizes</span>S–M · W28 L32 · 38</div><div class="kv2"><span>Stores</span>Zara, COS, Massimo Dutti</div><div class="kv2"><span>Dislikes</span><span style="color:var(--bad);width:auto">synthetics, loud prints</span></div>
      <div class="sub" style="margin-top:6px;font-size:12.5px">Zara runs small for her — take one size up.</div></div>
    <div><div class="lbl">Orders · 7</div>
      <div class="ord">{thumbs(['stripe','jacket-black'], 24, 30)}<span class="num">#001</span><span class="grow"></span><span class="st wait">In progress</span></div>
      <div class="ord">{thumbs(['sweater-grey'], 24, 30)}<span class="num">#0874</span><span class="grow"></span><span class="st ok">Delivered</span></div>
      <div class="ord">{thumbs(['loafers','scarf'], 24, 30)}<span class="num">#0812</span><span class="grow"></span><span class="st ok">Delivered</span></div>
    </div>
  </div>
</div>'''
save('04-clients.html', shell('Clients', 'Clients', main4, css4))

# ---------- 05 Tracking ----------
css5 = '''
.cols { display: flex; gap: 20px; align-items: flex-start; }
.track { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12.5px; color: var(--muted); }
.steps { display: flex; align-items: center; }
.steps i { width: 9px; height: 9px; border-radius: 50%; background: rgba(238,241,245,.14); }
.steps i.d { background: var(--clay); } .steps i.x { background: var(--bad); }
.steps s { width: 14px; height: 2px; background: rgba(238,241,245,.14); } .steps s.d { background: var(--clay); }
.panel { width: 330px; flex: none; }
.tl { position: relative; padding-left: 22px; }
.tl:before { content: ""; position: absolute; left: 5px; top: 6px; bottom: 6px; width: 2px; background: var(--line-2); }
.ev { position: relative; padding-bottom: 14px; font-size: 13px; }
.ev:before { content: ""; position: absolute; left: -21px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--panel); border: 2px solid var(--faint); }
.ev.d:before { background: var(--clay); border-color: var(--clay); }
.ev small { display: block; color: var(--faint); font-size: 11.5px; }
.ev.f { color: var(--faint); }
.red { color: var(--bad); }
'''
def steps(n, bad=False):
    o = ''
    for i in range(5):
        c = 'd' if i <= n and not (bad and i == n) else ('x' if bad and i == n else '')
        if i: o += f'<s class="{"d" if i <= n else ""}"></s>'
        o += f'<i class="{c}"></i>'
    return f'<div class="steps">{o}</div>'
ship = [('#0968',['loafers'],'Massimo Dutti · Nova Poshta','2045 0088 1244 71',2,False,'Arrived at warehouse','today, 10:12','on'),
        ('#0951',['sneakers'],'Nike','—',1,True,'No tracking for 3 days','Nov 18','late'),
        ('#0947',['sweater-grey','scarf'],'COS · Ukrposhta','0503 6448 1203 0',1,True,'No movement for 5 days','Nov 16','late'),
        ('#0939',['hoodie'],'Zara · Meest','MEEST 8830 2215',1,False,'On the way to warehouse','today, 08:40',''),
        ('#0932',['jeans','stripe'],'Reserved · Nova Poshta','2045 0099 8211 67',3,False,'Shipped to client','yesterday',''),
        ('#0918',['jacket-black'],'Zara · Nova Poshta','2045 0055 3000 81',3,False,'Courier delivers today','today, 09:55','')]
def srow(s):
    num, ph, shop, tr, n, bad, ev, t, cls = s
    e = f'<span class="red">{ev}</span>' if bad else ev
    return f'<tr class="{cls}"><td><div class="row" style="gap:12px"><div style="width:58px">{thumbs(ph, 30, 38)}</div><span class="num" style="font-size:15px">{num}</span></div></td><td>{shop}<div class="track">{tr}</div></td><td>{steps(n, bad)}</td><td>{e}<div class="sub" style="font-size:12px">{t}</div></td></tr>'
main5 = f'''
<h1>Tracking <span class="cnt">71</span></h1>
<div class="tabs"><a class="on">All <b>71</b></a><a>To warehouse <b>38</b></a><a>At warehouse <b>12</b></a><a>To clients <b>21</b></a><a class="red">Problems <b>2</b></a></div>
<div class="cols">
  <div class="card grow" style="overflow:hidden"><table><tr><th>Order</th><th>Store · tracking</th><th>Stage</th><th>Last event</th></tr>{''.join(srow(s) for s in ship)}</table></div>
  <div class="card panel"><div class="bd">
    <div class="row" style="gap:12px;margin-bottom:16px">{photo('loafers', 52, 66)}<div class="grow"><b class="num" style="font-size:17px">#0968</b><div style="font-size:13.5px">Leather loafers · 38</div><div class="sub">Olena Smyrnova</div></div></div>
    <div class="row" style="margin-bottom:18px"><span class="track grow">Nova Poshta 2045 0088 1244 71</span><span class="btn link">{ic('copy', 14)}</span></div>
    <div class="tl">
      <div class="ev d"><b>Purchased</b><small>Nov 17, 12:40</small></div>
      <div class="ev d"><b>Handed to Nova Poshta</b><small>Nov 18, 09:15</small></div>
      <div class="ev d"><b>Arrived at warehouse</b><small>checked, 3 photos · today, 10:12</small></div>
      <div class="ev f"><b>Ship to client</b><small>today</small></div>
      <div class="ev f"><b>Delivered</b><small>expected Nov 23</small></div>
    </div>
    <button class="btn pri big" style="width:100%;margin-top:6px">Ship to client →</button>
  </div></div>
</div>'''
save('05-tracking.html', shell('Tracking', 'Tracking', main5, css5))

# ---------- 06 Client chat (phone) ----------
page6 = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fitkit — client chat</title>
<link rel="stylesheet" href="styles.css">
<style>
.stage {{ width: 1440px; height: 900px; display: flex; gap: 80px; padding: 60px 110px; background: var(--bg); align-items: center; }}
.phone {{ width: 360px; height: 760px; background: #000; border: 1px solid #2a2f37; border-radius: 46px; padding: 12px; box-shadow: 0 0 60px -20px rgba(240,174,194,.25); flex: none; }}
.screen {{ background: var(--bg); height: 100%; border-radius: 36px; overflow: hidden; display: flex; flex-direction: column; }}
.ptop {{ padding: 40px 16px 12px; display: flex; gap: 10px; align-items: center; border-bottom: 1px solid var(--line); background: var(--paper); }}
.ordr {{ margin: 10px 14px 0; border: 1px solid var(--line); border-radius: 12px; padding: 8px 12px; font-size: 12.5px; color: var(--muted); display: flex; justify-content: space-between; background: var(--panel); }}
.pm {{ flex: 1; padding: 14px; display: flex; flex-direction: column; gap: 10px; }}
.b {{ max-width: 82%; padding: 9px 12px; border-radius: 16px; font-size: 13.5px; }}
.b small {{ display: block; font-size: 10.5px; color: var(--faint); margin-top: 3px; }}
.b.mgr {{ background: var(--panel); border: 1px solid var(--line); align-self: flex-start; border-bottom-left-radius: 5px; }}
.b.me {{ background: rgba(240,174,194,.16); border: 1px solid rgba(240,174,194,.25); align-self: flex-end; border-bottom-right-radius: 5px; }}
.prod {{ display: flex; gap: 8px; background: var(--bg); border: 1px solid var(--line); border-radius: 10px; padding: 6px; margin-top: 6px; font-size: 12px; }}
.pin {{ display: flex; gap: 8px; align-items: center; padding: 10px 12px 26px; border-top: 1px solid var(--line); background: var(--paper); }}
.pin .in {{ flex: 1; height: 40px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); font-size: 13px; background: var(--bg); }}
.round {{ width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: linear-gradient(180deg,#f6c4d3,var(--clay-deep)); color: #1c1013; box-shadow: 0 0 16px -2px var(--glow); }}
.expl {{ max-width: 520px; display: flex; flex-direction: column; gap: 14px; }}
.expl h1 {{ font-size: 30px; line-height: 1.2; }}
.expl p {{ color: var(--muted); font-size: 16px; }}
</style></head>
<body><div class="app" style="display:block;min-height:900px"><div class="stage">
  <div class="phone"><div class="screen">
    <div class="ptop"><img src="assets/logo-mark.png" style="width:32px;height:32px;filter:invert(1)"><div class="grow"><b class="serif" style="font-size:18px;font-weight:600">Fitkit</b><div class="sub" style="font-size:12px">Contact your manager · Anna online</div></div></div>
    <div class="ordr"><span>Order <b style="color:var(--text)">#001</b> · 3 items</span><span>In progress</span></div>
    <div class="pm">
      <div class="b me">Hi! I sent 3 items, please take a look 🙏<small>08:40</small></div>
      <div class="b mgr">Hi Maria! I’m Anna, your buyer. Checking stock and sizes, I’ll be back shortly.<small>Anna · 09:05</small></div>
      <div class="b mgr">The black jacket is out of stock in M. S is the same price — shall we take S?
        <div class="prod">{photo('jacket-black', 38, 48)}<div><b>Black jacket</b><div class="sub" style="font-size:11.5px">Zara · S · ₴3,999</div></div></div><small>Anna · 09:30</small></div>
      <div class="b me">Let’s go with S, thanks!<small>09:41 ✓✓</small></div>
    </div>
    <div class="pin"><div class="in">Message your manager…</div><div class="round">{ic('send', 17)}</div></div>
  </div></div>
  <div class="expl">
    <span class="tag" style="align-self:flex-start">What the client sees</span>
    <h1>A plain chat with their buyer</h1>
    <p>No buttons, no automation. The client writes any time, sends photos and links, and sees the order number and status above the chat.</p>
  </div>
</div></div></body></html>'''
save('06-client-chat.html', page6)
