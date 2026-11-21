# Mockup generator for all screens: python3 mockups/build.py mockups
import sys, os
OUT = sys.argv[1]
I = {
 'inbox': '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
 'bag': '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'truck': '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 'msg': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'chart': '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
 'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
 'back': '<path d="m15 18-6-6 6-6"/>',
 'ext': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
 'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
 'note': '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h5"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'filter': '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 'sliders': '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 'wallet': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
 'history': '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
 'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
}
def ic(n, extra=''): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"{extra}>{I[n]}</svg>'
def shell(active, title, main, extra_css=''):
    items = [('inbox','Requests','<span class="n red">12</span>'),('bag','Current orders','<span class="n">14</span>'),('users','Clients',''),('truck','Tracking','<span class="n">2</span>'),('msg','Messages','<span class="n red">3</span>'),('chart','Analytics','')]
    nav = ''.join(f'<a class="{"on" if t==active else ""}">{ic(i)}{t}{n}</a>' for i,t,n in items)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fitkit — {title}</title>
<link rel="stylesheet" href="styles.css">
<style>{extra_css}</style></head>
<body><div class="app">
  <aside class="side">
    <div class="logo"><img src="assets/logo-mark.png" alt=""><b>Fitkit</b></div>
    <div class="cap">Main</div>
    <nav class="nav">{nav}</nav>
    <div class="me"><div class="ava c2">AK</div><div>Anna Koval<small>Buyer · on shift</small></div></div>
  </aside>
  <div class="body">
    <div class="top"><div class="search">Search: request #, client, phone, tracking number…<kbd>⌘K</kbd></div><div class="bell">{ic('bell')}<i></i></div></div>
    <main class="main">{main}</main>
  </div>
</div></body></html>'''

# ---------- 01 Requests ----------
css1 = '''
.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); }
.tabs a { padding: 10px 14px; font-weight: 500; color: var(--muted); display: flex; gap: 7px; align-items: center; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tabs a.on { color: var(--text); font-weight: 600; border-bottom-color: var(--clay-ink); }
.tabs a b { font-weight: 600; font-size: 12px; background: rgba(20,17,15,.06); border-radius: 9px; padding: 0 7px; }
.tabs a.red b { background: var(--bad); color: #fff; }
.filters { display: flex; gap: 8px; align-items: center; }
.sel:after { content: "▾"; font-size: 10px; color: var(--muted); margin-left: 4px; }
.iconbtn { width: 34px; padding: 0; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; font-size: 12px; font-weight: 500; color: var(--muted); padding: 11px 10px; border-bottom: 1px solid var(--line); background: var(--paper); }
td { white-space: nowrap; padding: 11px 10px; border-bottom: 1px solid var(--line); vertical-align: middle; }
tr:last-child td { border-bottom: 0; }
tr.hl td { background: rgba(240,174,194,.06); }
tr.late td:first-child { box-shadow: inset 3px 0 0 var(--bad); }
.cb { width: 15px; height: 15px; border: 1.5px solid var(--line-2); border-radius: 4px; }
.num { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-weight: 600; font-size: 16px; letter-spacing: -.01em; }
.thumbs { display: flex; width: 82px; }
.thumbs .ph { width: 34px; height: 42px; border: 2px solid var(--panel); margin-left: -10px; border-radius: 7px; }
.thumbs .ph:first-child { margin-left: 0; }
.who { display: flex; gap: 9px; align-items: center; }
.timer { font-weight: 600; font-size: 12.5px; }
.timer.red { color: var(--bad); } .timer.org { color: var(--wait); }
.foot { display: flex; align-items: center; padding: 12px 14px; border-top: 1px solid var(--line); color: var(--muted); font-size: 12.5px; gap: 8px; }
'''
rows = [
 ('#001','late','Maria Lebedenko','c2',3,['Zara','H&M'],'₴6,378','bad','Overdue','08:40','<span class="timer red">−42 min</span>','—'),
 ('#002','late','Ihor Sokolenko','c4',1,['Answear'],'₴2,499','bad','Overdue','09:05','<span class="timer red">−15 min</span>','—'),
 ('#003','','Olha Petrenko','c3',2,['Reserved'],'₴3,170','wait','Awaiting','09:31','<span class="timer org">8 min left</span>','—'),
 ('#004','','Daria Vovk','c5',4,['ASOS'],'price not set','new','New','09:52','<span class="timer">29 min left</span>','—'),
 ('#005','','Pavlo Tykhonenko','c2',1,['Nike'],'₴5,899','new','New','09:58','<span class="timer">35 min left</span>','—'),
 ('#006','','Kseniia Orlyk','c4',2,['Mango','COS'],'₴4,270','new','New','10:03','<span class="timer">40 min left</span>','—'),
 ('#007','','Artem Bilyk','c3',3,['Zara'],'price not set','new','New','10:11','<span class="timer">48 min left</span>','—'),
 ('#008','','Olena Smyrnova','c5',1,['Massimo Dutti'],'₴3,999','','In progress','07:20','<span class="timer">—</span>','<div class="who"><div class="ava c2" style="width:24px;height:24px;font-size:10px">AK</div>Anna K.</div>'),
]
def tr(r):
    num,cls,name,c,n,shops,sum_,st,stt,date,tm,resp = r
    initials = ''.join(w[0] for w in name.split())
    P = {'#001':['stripe','jacket-black','jeans-black'],'#002':['hoodie'],'#003':['sweater-grey','jeans'],'#004':['hoodie','sweatpants','scarf'],'#005':['sneakers'],'#006':['scarf','loafers'],'#007':['stripe','sweatpants2','loafers'],'#008':['jacket-black']}
    th = ''.join(f'<img class="ph" src="assets/photos/{x}.jpg">' for x in P[num][:3])
    tags = ' '.join(f'<span class="tag">{s}</span>' for s in shops)
    word = 'item' if n==1 else ('items' if n<5 else 'items')
    sumcell = f'<span class="sub">{sum_}</span>' if 'not' in sum_ else sum_
    return f'<tr class="{cls}"><td><div class="cb"></div></td><td><div class="row" style="gap:12px"><div class="thumbs">{th}</div><div><div class="num">{num}</div><div class="sub" style="font-size:12px">{n} {word}</div></div></div></td><td><div class="who"><div class="ava {c}">{initials}</div>{name}</div></td><td>{tags}</td><td>{sumcell}</td><td><span class="st {st}">{stt}</span></td><td class="sub">{date}</td><td>{tm}</td><td>{resp}</td></tr>'
main1 = f'''
<div class="row">
  <div class="hicon">{ic('inbox')}</div>
  <div class="grow"><h1>Requests <span class="sub" style="font-size:22px;font-weight:500">· 1,001</span></h1><div class="sub">All incoming requests: new, awaiting and overdue</div></div>
  <button class="btn">{ic('download')}Export</button>
  <button class="btn pri">Take next request</button><i class="mk">1</i>
</div>
<div class="tabs"><a class="on">All <b>1,001</b></a><a>New <b>12</b></a><a>Awaiting <b>7</b></a><a class="red">Overdue <b>2</b></a><i class="mk" style="align-self:center;margin-left:6px">2</i></div>
<div class="filters">
  <button class="btn sel">All stores</button><button class="btn sel">Last 7 days</button><button class="btn">{ic('cal')}Nov 15 — Nov 21, 2026</button>
  <span class="grow"></span><button class="btn iconbtn">{ic('filter')}</button><button class="btn iconbtn">{ic('sliders')}</button>
</div>
<div class="card" style="overflow:hidden">
  <table>
    <tr><th style="width:44px"><div class="cb"></div></th><th>Request</th><th>Client</th><th>Stores</th><th>Amount</th><th>Status</th><th>Received (today)</th><th>Due <i class="mk" style="width:16px;height:16px;font-size:10px">3</i></th><th>Owner</th></tr>
    {''.join(tr(r) for r in rows)}
  </table>
  <div class="foot">Page 1 of 126<span class="grow"></span><button class="btn sm">← Back</button><button class="btn sm">Next →</button></div>
</div>
<div class="legend">
  <span><i class="mk">1</i>The system hands out the oldest request — no picking</span>
  <span><i class="mk">2</i>Tabs: all, new, awaiting, overdue</span>
  <span><i class="mk">3</i>Time left before overdue; overdue ones on top with a red bar</span>
  <span>Click a row to open the request card</span>
</div>'''
open(os.path.join(OUT,'01-requests.html'),'w').write(shell('Requests','Requests',main1,css1))

# ---------- 02 Request card ----------
css2 = '''
.cols { display: flex; gap: 18px; align-items: flex-start; }
.left { flex: 1; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.right { width: 390px; flex: none; display: flex; flex-direction: column; gap: 16px; }
.num { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-weight: 600; letter-spacing: -.02em; }
.it { display: flex; gap: 16px; padding: 16px 18px; border-bottom: 1px solid var(--line); }
.it:last-child { border-bottom: 0; }
.it .name { font-size: 15px; font-weight: 600; }
.grid { display: grid; grid-template-columns: repeat(3, 120px); gap: 2px 16px; margin: 10px 0; }
.grid span { display: block; font-size: 11.5px; color: var(--muted); }
.grid b { font-weight: 600; font-size: 14px; }
.grid .none { color: var(--faint); font-weight: 500; }
.cmt { background: var(--bg); border-radius: 10px; padding: 8px 12px; font-size: 13px; color: var(--text); }
.cmt span { color: var(--muted); font-size: 11.5px; display: block; }
.it .acts { display: flex; flex-direction: column; gap: 8px; align-items: flex-end; flex: none; width: 200px; }
.kv { display: flex; justify-content: space-between; padding: 7px 0; font-size: 13.5px; }
.kv span { color: var(--muted); }
.kv.total { border-top: 1px solid var(--line); margin-top: 4px; padding-top: 12px; }
.kv.total b { font-size: 20px; }
.lbl { font-size: 11.5px; color: var(--muted); font-weight: 500; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 7px; }
.blk { padding: 14px 18px; border-bottom: 1px solid var(--line); }
.blk:last-child { border-bottom: 0; }
.prob { display: flex; gap: 10px; align-items: flex-start; padding: 10px 12px; border-radius: 10px; margin-bottom: 8px; font-size: 13px; }
.prob:last-child { margin-bottom: 0; }
.prob.bad { background: var(--bad-bg); } .prob.wait { background: var(--wait-bg); }
.prob svg { width: 16px; height: 16px; flex: none; margin-top: 1px; }
.prob.bad svg { color: var(--bad); } .prob.wait svg { color: var(--wait); }
.prob b { display: block; }
.com { display: flex; gap: 10px; margin-bottom: 12px; font-size: 13px; }
.com .t small { color: var(--faint); margin-left: 6px; }
.input { border: 1px solid var(--line-2); border-radius: 10px; padding: 9px 12px; color: var(--faint); background: var(--bg); font-size: 13px; }
.stbtns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.stbtns .btn { width: 100%; }
.act { display: flex; gap: 12px; padding: 9px 0; font-size: 13px; }
.act .dot { width: 26px; height: 26px; border-radius: 50%; background: var(--bg); border: 1px solid var(--line); flex: none; display: grid; place-items: center; }
.act .dot svg { width: 13px; height: 13px; color: var(--muted); }
.act .d { margin-left: auto; color: var(--faint); font-size: 11.5px; white-space: nowrap; }
.copy { color: var(--clay-ink); font-weight: 600; font-size: 12.5px; display: inline-flex; gap: 5px; align-items: center; }
.copy svg { width: 13px; height: 13px; }
'''
def item(photo, name, shop, size, qty, price, comment, status, extra_btn=''):
    pr = f'<b>{price}</b>' if price else '<b class="none">not set</b>'
    return f'''<div class="it">
  <img class="ph" src="assets/photos/{photo}.jpg" style="width:76px;height:96px">
  <div class="grow">
    <div class="row" style="gap:8px"><div class="name">{name}</div><span class="tag">{shop}</span></div>
    <div class="grid"><div><span>Size</span><b>{size}</b></div><div><span>Quantity</span><b>{qty}</b></div><div><span>Price</span>{pr}</div></div>
    <div class="cmt"><span>Client comment</span>{comment}</div>
  </div>
  <div class="acts">{status}<button class="btn pri">Open in store {ic('ext')}</button>{extra_btn}</div>
</div>'''
items = (item('stripe','Striped sweater','Zara','L','1','₴1,799','“One size up, I like a loose fit”','<span class="st ok">Checked</span>')
 + item('jacket-black','Black jacket','Zara','M','1','₴3,999','“Need it by Nov 25. If no M — S is fine”','<span class="st bad">Size missing</span>','<button class="btn sm">Message client</button>')
 + item('jeans-black','Wide-leg jeans','H&amp;M','W28 L32','1','','“Dark, like in the photo. Couldn’t find the price”','<span class="st wait">Checking</span>'))
main2 = f'''
<div class="row">
  <div class="hicon">{ic('back')}</div>
  <div class="grow">
    <div class="row" style="gap:10px"><h1 class="num" style="font-size:26px">#001</h1><span class="st wait">In progress</span></div>
    <div class="sub">Received Nov 21, 2026, 08:40 · via Telegram bot · Maria Lebedenko</div>
  </div>
  <button class="btn">{ic('msg')}Message client</button><button class="btn">{ic('users')}Hand over</button>
</div>
<div class="cols">
  <div class="left">
    <div class="card">
      <div class="hd">{ic('bag')}<h2>Items · 3</h2><i class="mk">1</i><span class="grow"></span><span class="sub">1 of 3 checked</span></div>
      {items}
    </div>
    <div class="card">
      <div class="hd">{ic('user')}<h2>Client & delivery</h2></div>
      <div class="bd row" style="align-items:flex-start;gap:28px">
        <div class="who row" style="gap:10px"><div class="ava c2" style="width:40px;height:40px">ML</div><div><b>Maria Lebedenko</b><div class="sub">7th order · Telegram @maria_l</div><div class="sub">+380 67 ••• 45 12</div></div></div>
        <div class="grow"><div class="lbl">Delivery address</div>Kyiv, 12 Velyka Vasylkivska St, apt 48<div class="sub">Courier, 10:00–18:00</div><span class="copy">{ic('copy')}Copy address</span></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('history')}<h2>History</h2></div>
      <div class="bd" style="padding-top:8px;padding-bottom:8px">
        <div class="act"><div class="dot">{ic('alert')}</div><div><b>Problem found</b><div class="sub">Jacket: size M out of stock</div></div><span class="d">Nov 21, 09:12</span></div>
        <div class="act"><div class="dot">{ic('user')}</div><div><b>Taken by Anna Koval</b><div class="sub">Status: New → In progress</div></div><span class="d">Nov 21, 09:01</span></div>
        <div class="act"><div class="dot">{ic('inbox')}</div><div><b>Request received</b><div class="sub">3 items, 6 photos, via Telegram bot</div></div><span class="d">Nov 21, 08:40</span></div>
      </div>
    </div>
  </div>

  <div class="right">
    <div class="card">
      <div class="hd">{ic('sliders')}<h2>Order management</h2><i class="mk">2</i></div>
      <div class="blk"><div class="lbl">Current status</div><div class="row"><span class="st wait">In progress</span><span class="grow"></span><span class="sub">since 09:01 · 1h 20m left</span></div></div>
      <div class="blk"><div class="lbl">Owner</div><div class="row"><div class="ava c2">AK</div><div class="grow"><b>Anna Koval</b><div class="sub">Buyer</div></div><button class="btn sm">Change</button></div></div>
      <div class="blk"><div class="lbl">Total cost</div>
        <div class="kv"><span>Items (2 priced)</span>₴5,798</div>
        <div class="kv"><span>Jeans</span><span>price pending</span></div>
        <div class="kv"><span>Fitkit fee</span>₴580</div>
        <div class="kv total"><b>Total</b><b class="num">₴6,378</b></div>
      </div>
      <div class="blk"><div class="lbl">Change status</div>
        <div class="stbtns"><button class="btn">Waiting for client</button><button class="btn">Problem</button><button class="btn pri" style="grid-column:1/3">Move to “Purchased” →</button><button class="btn danger" style="grid-column:1/3">Cancel order</button></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('alert')}<h2>Issues & problems · 2</h2><i class="mk">3</i></div>
      <div class="bd">
        <div class="prob bad">{ic('alert')}<div class="grow"><b>No size M</b>Black jacket · Zara</div><button class="btn sm">Ask client</button></div>
        <div class="prob wait">{ic('clock')}<div class="grow"><b>Price not set</b>Wide-leg jeans · H&amp;M — check on the site</div></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('note')}<h2>Team comments</h2><i class="mk">4</i></div>
      <div class="bd">
        <div class="com"><div class="ava c3">IR</div><div class="t"><b>Iryna R.</b><small>shift lead · 09:20</small><div>If S is also gone — suggest Massimo Dutti, she has bought there before.</div></div></div>
        <div class="com"><div class="ava c2">AK</div><div class="t"><b>Anna K.</b><small>09:25</small><div>OK, I’ll check S and message the client.</div></div></div>
        <div class="input">Comment for the team (client won’t see it)…</div>
      </div>
    </div>
  </div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Left — items: size, quantity, price (if known), client comment and a link to the store</span>
  <span><i class="mk">2</i>Right — management: status, owner, cost and status buttons</span>
  <span><i class="mk">3</i>Issues and problems for this request</span>
  <span><i class="mk">4</i>Internal team comments</span>
</div>'''
open(os.path.join(OUT,'02-order-card.html'),'w').write(shell('Requests','Request #001',main2,css2))

# ---------- 03 Messages (employee) ----------
I['clip'] = '<path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>'
I['send'] = '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>'
I['img'] = '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>'
css3 = '''
.main { padding: 0; gap: 0; }
.chat { display: flex; height: 904px; }
.list { width: 300px; border-right: 1px solid var(--line); background: var(--paper); display: flex; flex-direction: column; flex: none; }
.list .hd { padding: 18px 16px 12px; }
.list .search2 { margin: 0 16px 10px; height: 34px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 12px; color: var(--faint); font-size: 13px; background: var(--bg); }
.chips { display: flex; gap: 6px; padding: 0 16px 10px; }
.chip { height: 26px; padding: 0 10px; border-radius: 999px; border: 1px solid var(--line-2); font-size: 12px; display: inline-flex; align-items: center; color: var(--muted); }
.chip.on { background: var(--clay-veil); color: var(--clay); border-color: rgba(240,174,194,.35); }
.c { display: flex; gap: 10px; padding: 12px 16px; border-top: 1px solid var(--line); }
.c.on { background: var(--clay-veil); }
.c .t { flex: 1; min-width: 0; font-size: 13px; }
.c .t b { display: flex; justify-content: space-between; font-weight: 600; }
.c .t b small { color: var(--faint); font-weight: 400; font-size: 11.5px; }
.c .t p { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.c .badge { background: var(--clay); color: #1c1013; font-size: 11px; font-weight: 700; border-radius: 9px; padding: 0 6px; align-self: center; }
.conv { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.conv .top2 { display: flex; align-items: center; gap: 12px; padding: 14px 22px; border-bottom: 1px solid var(--line); background: var(--paper); }
.msgs { flex: 1; padding: 22px; display: flex; flex-direction: column; gap: 12px; }
.day { align-self: center; font-size: 11.5px; color: var(--faint); }
.m { max-width: 62%; padding: 10px 14px; border-radius: 16px; font-size: 14px; line-height: 1.45; }
.m small { display: block; font-size: 11px; color: var(--faint); margin-top: 4px; }
.m.cl { background: var(--panel); border: 1px solid var(--line); align-self: flex-start; border-bottom-left-radius: 5px; }
.m.me { background: rgba(240,174,194,.13); border: 1px solid rgba(240,174,194,.22); align-self: flex-end; border-bottom-right-radius: 5px; }
.prod { display: flex; gap: 10px; background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 8px; margin-top: 8px; font-size: 12.5px; }
.prod .sub { font-size: 12px; }
.composer { border-top: 1px solid var(--line); padding: 14px 22px; display: flex; gap: 10px; align-items: center; background: var(--paper); }
.composer .in { flex: 1; height: 42px; border: 1px solid var(--line-2); border-radius: 12px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); background: var(--bg); }
.iconbtn { width: 38px; padding: 0; height: 38px; }
.ctx { width: 300px; border-left: 1px solid var(--line); background: var(--paper); padding: 18px 16px; display: flex; flex-direction: column; gap: 14px; flex: none; }
.ctx .mini { display: flex; gap: 10px; align-items: center; font-size: 13px; padding: 8px 0; border-bottom: 1px solid var(--line); }
.ctx .mini:last-child { border-bottom: 0; }
.ctx .note { background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font-size: 12.5px; color: var(--muted); }
.legendbar { padding: 12px 22px; border-top: 1px solid var(--line); }
'''
def chatrow(name,c,num,last,time,badge='',on=False):
    ini=''.join(w[0] for w in name.split())
    b=f'<span class="badge">{badge}</span>' if badge else ''
    return f'<div class="c {"on" if on else ""}"><div class="ava {c}">{ini}</div><div class="t"><b>{name}<small>{time}</small></b><p><span style="color:var(--clay)">{num}</span> · {last}</p></div>{b}</div>'
main3 = f'''
<div class="chat">
  <div class="list">
    <div class="hd row"><h2 class="grow">Messages</h2><i class="mk">1</i></div>
    <div class="search2">Find a client or request…</div>
    <div class="chips"><span class="chip on">All</span><span class="chip">Unanswered · 3</span><span class="chip">Mine</span></div>
    {chatrow('Maria Lebedenko','c2','#001','Let’s go with S, thanks!','09:41','1',True)}
    {chatrow('Ihor Sokolenko','c4','#002','Why did the price go up?','09:20','1')}
    {chatrow('Olha Petrenko','c3','#003','Sent one more link','09:12','1')}
    {chatrow('Daria Vovk','c5','#004','You: Checking stock, back soon…','08:55')}
    {chatrow('Pavlo Tykhonenko','c2','#005','You: Tracking number tomorrow','yesterday')}
    {chatrow('Olena Smyrnova','c4','#008','Thanks, everything arrived!','yesterday')}
  </div>
  <div class="conv">
    <div class="top2"><div class="ava c2">ML</div><div class="grow"><b>Maria Lebedenko</b><div class="sub">request <span class="num" style="font-size:14px">#001</span> · Telegram · online 2 min ago</div></div><button class="btn">{ic('bag')}Open request</button></div>
    <div class="msgs">
      <div class="day">Today</div>
      <div class="m cl">Hi! I sent 3 items, please take a look 🙏<small>08:40</small></div>
      <div class="m me">Hi Maria! I’m Anna, your buyer. Checking stock and sizes, I’ll be back shortly.<small>Anna · 09:05</small></div>
      <div class="m me">Unfortunately the black jacket is out of stock in M. S is available at the same price, link below. It should fit your measurements — shall we take S?
        <div class="prod"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:44px;height:56px"><div><b>Black jacket</b><div class="sub">Zara · S · ₴3,999</div><div class="sub" style="color:var(--clay)">zara.com ↗</div></div></div>
        <small>Anna · 09:30</small></div>
      <div class="m cl">Let’s go with S, thanks!<small>09:41</small></div>
    </div>
    <div class="composer"><button class="btn iconbtn">{ic('clip')}</button><button class="btn iconbtn">{ic('img')}</button><div class="in">Message the client…</div><button class="btn pri">{ic('send')}Send</button><i class="mk">2</i></div>
  </div>
  <div class="ctx">
    <div class="row"><h2 class="grow">Request <span class="num">#001</span></h2><span class="st wait">In progress</span></div>
    <div><div class="lbl" style="font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Items</div>
      <div class="mini"><img class="ph" src="assets/photos/stripe.jpg" style="width:32px;height:40px"><div class="grow">Striped sweater<div class="sub">L · ₴1,799</div></div><span class="st ok">OK</span></div>
      <div class="mini"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:32px;height:40px"><div class="grow">Black jacket<div class="sub">M → S · ₴3,999</div></div><span class="st wait">Change</span></div>
      <div class="mini"><img class="ph" src="assets/photos/jeans-black.jpg" style="width:32px;height:40px"><div class="grow">Wide-leg jeans<div class="sub">W28 L32 · price ?</div></div><span class="st">Checking</span></div>
    </div>
    <div class="note">The client replied “S”. Change the size in the request yourself — “Open request”.<i class="mk" style="margin-left:6px;vertical-align:middle">3</i></div>
  </div>
</div>
<div class="legendbar"><div class="legend">
  <span><i class="mk">1</i>All client chats; each is linked to a request</span>
  <span><i class="mk">2</i>Plain chat: text, photos, product links — no automation or choice buttons</span>
  <span><i class="mk">3</i>The employee copies the client’s answer into the request</span>
</div></div>'''
open(os.path.join(OUT,'03-messages.html'),'w').write(shell('Messages','Messages',main3,css3))

# ---------- 04 Client chat ----------
page4 = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Fitkit — client chat</title>
<link rel="stylesheet" href="styles.css">
<style>
.stage {{ width: 1440px; height: 960px; display: flex; gap: 70px; padding: 50px 90px; background: var(--bg); align-items: center; position: relative; }}
.phone {{ width: 360px; height: 760px; background: #000; border: 1px solid #2a2f37; border-radius: 46px; padding: 12px; box-shadow: 0 0 60px -20px rgba(240,174,194,.25); flex: none; }}
.screen {{ background: var(--bg); height: 100%; border-radius: 36px; overflow: hidden; display: flex; flex-direction: column; }}
.ptop {{ padding: 40px 16px 12px; display: flex; gap: 10px; align-items: center; border-bottom: 1px solid var(--line); background: var(--paper); }}
.ord {{ margin: 10px 14px 0; border: 1px solid var(--line); border-radius: 12px; padding: 8px 12px; font-size: 12.5px; color: var(--muted); display: flex; justify-content: space-between; background: var(--panel); }}
.pm {{ flex: 1; padding: 14px; display: flex; flex-direction: column; gap: 10px; }}
.b {{ max-width: 82%; padding: 9px 12px; border-radius: 16px; font-size: 13.5px; }}
.b small {{ display: block; font-size: 10.5px; color: var(--faint); margin-top: 3px; }}
.b.mgr {{ background: var(--panel); border: 1px solid var(--line); align-self: flex-start; border-bottom-left-radius: 5px; }}
.b.me {{ background: rgba(240,174,194,.16); border: 1px solid rgba(240,174,194,.25); align-self: flex-end; border-bottom-right-radius: 5px; }}
.prod {{ display: flex; gap: 8px; background: var(--bg); border: 1px solid var(--line); border-radius: 10px; padding: 6px; margin-top: 6px; font-size: 12px; }}
.pin {{ display: flex; gap: 8px; align-items: center; padding: 10px 12px 26px; border-top: 1px solid var(--line); background: var(--paper); }}
.pin .in {{ flex: 1; height: 40px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 14px; color: var(--faint); font-size: 13px; background: var(--bg); }}
.round {{ width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: linear-gradient(180deg,#f6c4d3,var(--clay-deep)); box-shadow: 0 0 16px -2px var(--glow); }}
.round svg {{ width: 17px; height: 17px; color: #1c1013; }}
.expl {{ max-width: 560px; display: flex; flex-direction: column; gap: 18px; }}
.expl h1 {{ font-size: 30px; line-height: 1.2; }}
.pt {{ display: flex; gap: 14px; align-items: flex-start; font-size: 15px; color: var(--muted); }}
.pt b {{ color: var(--text); display: block; font-size: 15.5px; margin-bottom: 2px; }}
</style></head>
<body><div class="app" style="display:block"><div class="stage">
  <div class="phone"><div class="screen">
    <div class="ptop"><img src="assets/logo-mark.png" style="width:32px;height:32px;filter:invert(1)"><div class="grow"><b class="serif" style="font-size:18px;font-weight:600">Fitkit</b><div class="sub" style="font-size:12px">Contact your manager · Anna online</div></div></div>
    <div class="ord"><span>Order <b style="color:var(--text)">#001</b> · 3 items</span><span>In progress</span></div>
    <div class="pm">
      <div class="b me">Hi! I sent 3 items, please take a look 🙏<small>08:40</small></div>
      <div class="b mgr">Hi Maria! I’m Anna, your buyer. Checking stock and sizes, I’ll be back shortly.<small>Anna · 09:05</small></div>
      <div class="b mgr">The black jacket is out of stock in M. S is the same price, link below. Shall we take S?
        <div class="prod"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:38px;height:48px"><div><b>Black jacket</b><div class="sub" style="font-size:11.5px">Zara · S · ₴3,999</div></div></div><small>Anna · 09:30</small></div>
      <div class="b me">Let’s go with S, thanks!<small>09:41 ✓✓</small></div>
    </div>
    <div class="pin"><div class="in">Message your manager…</div><div class="round">{ic('send')}</div></div>
  </div></div>
  <div class="expl">
    <div class="row" style="gap:10px"><span class="tag">What the client sees</span><i class="mk">1</i></div>
    <h1>A plain chat with a manager — no buttons, no automation</h1>
    <div class="pt"><div class="hicon">{ic('msg')}</div><div><b>Contact your manager</b>The client can message their buyer any time — just like a messenger. The header shows who handles the order and that they are online.</div></div>
    <div class="pt"><div class="hicon">{ic('img')}</div><div><b>Photos and links</b>The buyer sends a photo or a link to an option; the client can reply with their own photos and links.</div></div>
    <div class="pt"><div class="hicon">{ic('bag')}</div><div><b>Order on top</b>Above the chat — the order number and status, so the client knows what it is about.</div></div>
  </div>
</div></div></body></html>'''
open(os.path.join(OUT,'04-client-chat.html'),'w').write(page4)

# ---------- 05 Analytics ----------
I['up'] = '<path d="m18 15-6-6-6 6"/>'
css5 = '''
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi { padding: 16px 18px; }
.kpi .l { color: var(--muted); font-size: 12.5px; display: flex; gap: 8px; align-items: center; }
.kpi .v { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-weight: 600; font-size: 34px; letter-spacing: -.02em; margin-top: 6px; line-height: 1.1; }
.kpi .v small { font-family: "Inter Variable", sans-serif; font-size: 15px; font-weight: 500; color: var(--muted); }
.kpi .d { font-size: 12.5px; margin-top: 4px; color: var(--muted); }
.good { color: var(--ok); font-weight: 600; } .badc { color: var(--bad); font-weight: 600; }
.grid2 { display: grid; gap: 16px; }
.chart text { font-family: "Inter Variable", sans-serif; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; font-size: 12px; font-weight: 500; color: var(--muted); padding: 10px 12px; border-bottom: 1px solid var(--line); }
td { padding: 10px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; font-size: 13.5px; }
tr:last-child td { border-bottom: 0; }
.bar { height: 6px; border-radius: 3px; background: rgba(238,241,245,.08); width: 90px; display: inline-block; vertical-align: middle; margin-left: 8px; }
.bar i { display: block; height: 100%; border-radius: 3px; background: var(--clay); }
.who { display: flex; gap: 9px; align-items: center; }
'''
days = [('Mon',128),('Tue',142),('Wed',151),('Thu',163),('Fri',170),('Sat',129),('Sun',118)]
def bars_svg():
    W,H,l,b,t = 600,230,36,30,14
    mx = 200; bw = 44; gap = (W-l-10-bw*len(days))/(len(days)-1)
    g = ''
    for v in [0,50,100,150,200]:
        y = H-b-(H-b-t)*v/mx
        g += f'<line x1="{l}" x2="{W-6}" y1="{y:.1f}" y2="{y:.1f}" stroke="rgba(238,241,245,.08)"/><text x="{l-8}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#6b7480">{v}</text>'
    for i,(d,v) in enumerate(days):
        x = l+i*(bw+gap); h = (H-b-t)*v/mx; y = H-b-h
        hl = d=='Fri'
        g += f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="6" fill="{"#f0aec2" if hl else "rgba(240,174,194,.38)"}"/>'
        g += f'<text x="{x+bw/2:.1f}" y="{y-6:.1f}" text-anchor="middle" font-size="11.5" font-weight="600" fill="{"#eef1f5" if hl else "#99a3b0"}">{v}</text>'
        g += f'<text x="{x+bw/2:.1f}" y="{H-10}" text-anchor="middle" font-size="12" fill="#99a3b0">{d}</text>'
    return f'<svg class="chart" viewBox="0 0 {W} {H}" width="100%">{g}</svg>'
speed = [('Mon',2.1),('Tue',1.9),('Wed',2.0),('Thu',1.7),('Fri',1.6),('Sat',1.8),('Sun',1.5)]
def line_svg():
    W,H,l,b,t = 460,230,40,30,14; mx = 3.0
    X = lambda i: l+12+i*(W-l-30)/(len(speed)-1); Y = lambda v: H-b-(H-b-t)*v/mx
    g = ''
    for v in [0,1,2,3]:
        g += f'<line x1="{l}" x2="{W-6}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="rgba(238,241,245,.08)"/><text x="{l-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="11" fill="#6b7480">{v}h</text>'
    g += f'<line x1="{l}" x2="{W-6}" y1="{Y(2):.1f}" y2="{Y(2):.1f}" stroke="#f0b45c" stroke-dasharray="5 5" stroke-width="1.3"/><text x="{(X(3)+X(4))/2:.1f}" y="{Y(2)+15:.1f}" text-anchor="middle" font-size="11" fill="#f0b45c">goal — 2h</text>'
    pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i,(d,v) in enumerate(speed))
    area = f'{X(0):.1f},{Y(0):.1f} ' + pts + f' {X(len(speed)-1):.1f},{Y(0):.1f}'
    g += f'<polygon points="{area}" fill="rgba(240,174,194,.10)"/><polyline points="{pts}" fill="none" stroke="#f0aec2" stroke-width="2.4" stroke-linejoin="round"/>'
    for i,(d,v) in enumerate(speed):
        last = i==len(speed)-1
        g += f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="{5 if last else 3.5}" fill="{"#f0aec2" if last else "#171a20"}" stroke="#f0aec2" stroke-width="2"/>'
        g += f'<text x="{X(i):.1f}" y="{H-10}" text-anchor="middle" font-size="12" fill="#99a3b0">{d}</text>'
    g += f'<text x="{X(len(speed)-1):.1f}" y="{Y(1.5)-12:.1f}" text-anchor="middle" font-size="12" font-weight="600" fill="#eef1f5">1.5h</text>'
    return f'<svg class="chart" viewBox="0 0 {W} {H}" width="100%">{g}</svg>'
errs = [('Size missing',18),('Price went up',11),('Payment declined',7),('Store cancelled order',5),('Parcel delayed',5)]
def hbars():
    mx = 18; out = ''
    for n,v in errs:
        out += f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px"><div style="width:170px;font-size:13px">{n}</div><div style="flex:1;height:10px;background:rgba(238,241,245,.06);border-radius:5px"><div style="width:{v/mx*100:.0f}%;height:100%;border-radius:5px;background:{"#ff7a7a" if v==18 else "rgba(255,122,122,.45)"}"></div></div><div style="width:28px;text-align:right;font-weight:600">{v}</div></div>'
    return out
staff = [('Anna Koval','c2','Buyer',214,'1h 32m','1.4%',6),('Iryna Romanenko','c3','Shift lead',168,'1h 41m','2.0%',5),('Svitlana Kim','c5','Buyer',183,'1h 49m','2.7%',9),('Dmytro Orlov','c4','Buyer',197,'1h 55m','3.6%',10),('Maksym Bilyi','c4','Buyer',239,'2h 10m','5.4%',16)]
def staffrows():
    out=''
    for n,c,r,cnt,t,late,e in staff:
        ini=''.join(w[0] for w in n.split())
        latecls = 'badc' if float(late.rstrip('% ').replace(',','.'))>4 else ''
        out += f'<tr><td><div class="who"><div class="ava {c}" style="width:28px;height:28px;font-size:11px">{ini}</div><div>{n}<div class="sub" style="font-size:11.5px">{r}</div></div></div></td><td>{cnt}<span class="bar"><i style="width:{cnt/239*100:.0f}%"></i></span></td><td>{t}</td><td class="{latecls}">{late}</td><td>{e}</td></tr>'
    return out
main5 = f'''
<div class="row">
  <div class="hicon">{ic('chart')}</div>
  <div class="grow"><h1>Analytics</h1><div class="sub">Request volume, processing speed, issues and team performance</div></div>
  <button class="btn sel">Last 7 days</button><button class="btn">{ic('cal')}Nov 15 — Nov 21, 2026</button><button class="btn">{ic('download')}Export</button>
</div>
<div class="kpis">
  <div class="card kpi"><div class="l">Requests this week<i class="mk">1</i></div><div class="v">1,001</div><div class="d"><span class="good">+12%</span> vs last week</div></div>
  <div class="card kpi"><div class="l">Avg. processing time</div><div class="v">1.8 <small>h</small></div><div class="d"><span class="good">−9 min</span> · from request to “Purchased”</div></div>
  <div class="card kpi"><div class="l">Overdue</div><div class="v">3.1 <small>%</small></div><div class="d">31 requests not taken in time</div></div>
  <div class="card kpi"><div class="l">Issues & problems</div><div class="v">46</div><div class="d"><span class="badc">4.6%</span> of orders · most often “size missing”</div></div>
</div>
<div class="grid2" style="grid-template-columns: 1.3fr 1fr">
  <div class="card"><div class="hd">{ic('inbox')}<h2>Requests by day</h2><i class="mk">2</i><span class="grow"></span><span class="sub">peak — Friday, 170</span></div><div class="bd">{bars_svg()}</div></div>
  <div class="card"><div class="hd">{ic('clock')}<h2>Processing speed</h2><i class="mk">3</i><span class="grow"></span><span class="sub">daily average</span></div><div class="bd">{line_svg()}</div></div>
</div>
<div class="grid2" style="grid-template-columns: 1fr 1.6fr">
  <div class="card"><div class="hd">{ic('alert')}<h2>Issues & problems · 46</h2><i class="mk">4</i></div><div class="bd">{hbars()}<div class="sub" style="margin-top:4px">“Size missing” is 39% of all problems: worth checking stock when taking a request</div></div></div>
  <div class="card" style="overflow:hidden"><div class="hd">{ic('users')}<h2>Team performance</h2><i class="mk">5</i><span class="grow"></span><span class="sub">sorted by avg. time</span></div>
    <table><tr><th>Employee</th><th>Requests</th><th>Avg. time</th><th>Overdue</th><th>Issues</th></tr>{staffrows()}</table></div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Key numbers for the period vs the previous one</span>
  <span><i class="mk">2</i>How many requests came in each day</span>
  <span><i class="mk">3</i>Time from request to purchase; dashed line — goal</span>
  <span><i class="mk">4</i>Which problems happen most</span>
  <span><i class="mk">5</i>A buyer sees only their row; the shift lead sees the whole team</span>
</div>'''
open(os.path.join(OUT,'05-analytics.html'),'w').write(shell('Analytics','Analytics',main5,css5))

# ---------- shared styles for 06–08 ----------
I['phone'] = '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'
I['mail'] = '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'
I['heart'] = '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7z"/>'
I['box'] = '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>'
I['check'] = '<path d="M20 6 9 17l-5-5"/>'
css_common = '''
table { width: 100%; border-collapse: collapse; }
th { text-align: left; font-size: 12px; font-weight: 500; color: var(--muted); padding: 10px 12px; border-bottom: 1px solid var(--line); background: var(--paper); white-space: nowrap; }
td { padding: 10px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; vertical-align: middle; }
tr:last-child td { border-bottom: 0; }
.num { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-weight: 600; letter-spacing: -.01em; }
.who { display: flex; gap: 10px; align-items: center; }
.lbl { font-size: 11.5px; color: var(--muted); font-weight: 500; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.lbl .btn.link { margin-left: auto; text-transform: none; letter-spacing: 0; font-size: 12.5px; }
.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); }
.tabs a { padding: 10px 14px; font-weight: 500; color: var(--muted); display: flex; gap: 7px; align-items: center; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tabs a.on { color: var(--text); font-weight: 600; border-bottom-color: var(--clay-ink); }
.tabs a b { font-weight: 600; font-size: 12px; background: rgba(238,241,245,.08); border-radius: 9px; padding: 0 7px; }
.tabs a.red b { background: var(--bad); color: #fff; }
.sel:after { content: "▾"; font-size: 10px; color: var(--muted); margin-left: 4px; }
.badc { color: var(--bad); font-weight: 600; }
.th { width: 36px; height: 44px; border-radius: 7px; }
'''

# ---------- 06 Clients ----------
css6 = css_common + '''
.cols { display: flex; gap: 18px; align-items: flex-start; }
.clist { width: 430px; flex: none; }
.clist .search2 { margin: 14px 16px 6px; height: 34px; border: 1px solid var(--line-2); border-radius: 999px; display: flex; align-items: center; padding: 0 12px; color: var(--faint); font-size: 13px; background: var(--bg); }
.clist tr.on td { background: var(--clay-veil); }
.clist tr.on td:first-child { box-shadow: inset 3px 0 0 var(--clay); }
.prof { flex: 1; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid var(--line); }
.stats div { padding: 14px 18px; border-right: 1px solid var(--line); }
.stats div:last-child { border-right: 0; }
.stats b { display: block; font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-size: 24px; font-weight: 600; letter-spacing: -.02em; }
.stats span { font-size: 12px; color: var(--muted); }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.kv { display: flex; gap: 10px; align-items: center; padding: 6px 0; font-size: 13.5px; }
.kv svg { width: 15px; height: 15px; color: var(--clay); flex: none; }
.addr { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; margin-bottom: 8px; font-size: 13px; background: var(--bg); }
.pref { display: grid; grid-template-columns: 110px 1fr; gap: 8px 12px; font-size: 13.5px; align-items: center; }
.pref span { color: var(--muted); font-size: 12.5px; }
.chips { display: flex; gap: 6px; flex-wrap: wrap; }
.chip { height: 24px; padding: 0 10px; border-radius: 999px; border: 1px solid var(--line-2); font-size: 12px; display: inline-flex; align-items: center; }
.chip.no { border-color: rgba(255,122,122,.35); color: var(--bad); }
.chip.yes { border-color: rgba(240,174,194,.35); color: var(--clay); }
.thumbs { display: flex; } .thumbs img { width: 30px; height: 38px; border-radius: 6px; border: 2px solid var(--panel); margin-left: -8px; object-fit: cover; } .thumbs img:first-child { margin-left: 0; }
.note { background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font-size: 13px; margin-bottom: 8px; }
.note small { display: block; color: var(--faint); font-size: 11.5px; margin-top: 3px; }
'''
clients = [('Maria Lebedenko','c2','@maria_l · Telegram',7,'₴38,500','today',True),('Ihor Sokolenko','c4','+380 50 ••• 18 40',3,'₴9,680','today',False),('Olha Petrenko','c3','@olga_p · Telegram',12,'₴64,950','today',False),('Daria Vovk','c5','daria.v@•••.ua',1,'—','today',False),('Pavlo Tykhonenko','c2','@pavel_t · Telegram',5,'₴29,140','Nov 19',False),('Kseniia Orlyk','c4','+380 93 ••• 77 03',2,'₴8,500','Nov 15',False),('Artem Bilyk','c3','@artem_b · Telegram',4,'₴17,950','Nov 12',False),('Olena Smyrnova','c5','@elena_s · Telegram',9,'₴53,730','Nov 8',False)]
def crow(c):
    n,col,contact,cnt,total,last,on=c
    ini=''.join(w[0] for w in n.split())
    return f'<tr class="{"on" if on else ""}"><td><div class="who"><div class="ava {col}">{ini}</div><div><b style="font-weight:600">{n}</b><div class="sub" style="font-size:12px">{contact}</div></div></div></td><td style="text-align:right">{cnt}<div class="sub" style="font-size:12px">{total}</div></td><td class="sub" style="font-size:12.5px">{last}</td></tr>'
hist = [('#001',['stripe','jacket-black','jeans-black'],'Zara, H&amp;M','₴6,378','wait','In progress','Nov 21'),('#0874',['sweater-grey'],'COS','₴3,629','ok','Delivered','Nov 2'),('#0812',['loafers','scarf'],'Massimo Dutti','₴11,090','ok','Delivered','Oct 18'),('#0755',['hoodie','sweatpants'],'Zara','₴5,380','ok','Delivered','Sep 30'),('#0690',['jeans'],'Reserved','₴2,269','','Cancelled','Sep 11')]
def hrow(h):
    num,ph,shop,sm,st,stt,d=h
    imgs=''.join(f'<img src="assets/photos/{p}.jpg">' for p in ph)
    return f'<tr><td><div class="row" style="gap:10px"><div class="thumbs" style="width:78px">{imgs}</div><span class="num" style="font-size:15px">{num}</span></div></td><td class="sub">{shop}</td><td>{sm}</td><td><span class="st {st}">{stt}</span></td><td class="sub">{d}</td></tr>'
main6 = f'''
<div class="row">
  <div class="hicon">{ic('users')}</div>
  <div class="grow"><h1>Clients <span class="sub" style="font-size:22px;font-weight:500">· 2,318</span></h1><div class="sub">Contacts, addresses, preferences and order history</div></div>
  <button class="btn sel">All clients</button><button class="btn">{ic('download')}Export</button>
</div>
<div class="cols">
  <div class="card clist" style="overflow:hidden">
    <div class="search2">Name, phone, Telegram or order #…</div>
    <table><tr><th>Client <i class="mk" style="width:16px;height:16px;font-size:10px;vertical-align:middle">1</i></th><th style="text-align:right">Orders</th><th>Last</th></tr>{''.join(crow(c) for c in clients)}</table>
  </div>
  <div class="prof">
    <div class="card">
      <div class="bd row" style="gap:16px">
        <div class="ava c2" style="width:56px;height:56px;font-size:18px">ML</div>
        <div class="grow"><h1 style="font-size:22px">Maria Lebedenko</h1><div class="sub">Client since March 2026 · handled by Anna Koval</div></div>
        <button class="btn">{ic('msg')}Message</button><button class="btn pri">{ic('bag')}Open current request</button>
      </div>
      <div class="stats"><div><b>7</b><span>orders</span></div><div><b>₴38,500</b><span>total spent</span></div><div><b>₴5,500</b><span>avg. order</span></div><div><b>0</b><span>returns</span></div></div>
    </div>
    <div class="two">
      <div class="card"><div class="bd">
        <div class="lbl">Contacts <i class="mk">2</i></div>
        <div class="kv">{ic('msg')}Telegram @maria_l <span class="tag" style="margin-left:auto">main</span></div>
        <div class="kv">{ic('phone')}+380 67 ••• 45 12 <span class="btn link" style="margin-left:auto">Show</span></div>
        <div class="kv">{ic('mail')}maria.l@•••.ua</div>
        <div class="lbl" style="margin-top:14px">Delivery addresses<span class="btn link">+ Add</span></div>
        <div class="addr"><b>Kyiv, 12 Velyka Vasylkivska St, apt 48</b> <span class="tag" style="margin-left:6px">default</span><div class="sub">Courier, 10:00–18:00 · entrance 3, floor 7</div></div>
        <div class="addr"><b>Kyiv, 10 Dniprovska Embankment, office 1204</b><div class="sub">Nova Poshta branch #12 · for weekday orders</div></div>
      </div></div>
      <div class="card"><div class="bd">
        <div class="lbl">Preferences <i class="mk">3</i><span class="btn link">Change</span></div>
        <div class="pref">
          <span>Tops</span><div>S–M, likes a loose fit</div>
          <span>Bottoms</span><div>W28 L32</div>
          <span>Shoes</span><div>38</div>
          <span>Stores</span><div class="chips"><span class="chip yes">Zara</span><span class="chip yes">COS</span><span class="chip yes">Massimo Dutti</span></div>
          <span>Colours</span><div class="chips"><span class="chip">black</span><span class="chip">grey</span><span class="chip">beige</span></div>
          <span>Dislikes</span><div class="chips"><span class="chip no">synthetics</span><span class="chip no">loud prints</span></div>
        </div>
        <div class="lbl" style="margin-top:16px">Team notes</div>
        <div class="note">Zara runs small for her — take one size up.<small>Anna K. · Oct 2</small></div>
      </div></div>
    </div>
    <div class="card" style="overflow:hidden">
      <div class="hd">{ic('history')}<h2>Order history · 7</h2><i class="mk">4</i><span class="grow"></span><span class="btn link">All orders →</span></div>
      <table><tr><th>Order</th><th>Stores</th><th>Amount</th><th>Status</th><th>Date</th></tr>{''.join(hrow(h) for h in hist)}</table>
    </div>
  </div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Searchable list; the selected client opens on the right</span>
  <span><i class="mk">2</i>Contacts: main channel marked, phone hidden until clicked</span>
  <span><i class="mk">3</i>Sizes, favourite stores, colours and dislikes — visible with every request</span>
  <span><i class="mk">4</i>All client orders with item photos</span>
</div>'''
open(os.path.join(OUT,'06-clients.html'),'w').write(shell('Clients','Clients',main6,css6))

# ---------- 07 Tracking ----------
css7 = css_common + '''
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi { padding: 14px 18px; display: flex; gap: 14px; align-items: center; }
.kpi b { font-family: "Fraunces Variable", Georgia, serif; font-variation-settings: "opsz" 48, "SOFT" 20, "WONK" 1; font-size: 30px; font-weight: 600; letter-spacing: -.02em; line-height: 1; }
.kpi .sub { font-size: 12.5px; }
.kpi.alert { border-color: rgba(255,122,122,.35); }
.kpi.alert b { color: var(--bad); }
.cols { display: flex; gap: 18px; align-items: flex-start; }
.tbl { flex: 1; min-width: 0; }
tr.on td { background: var(--clay-veil); }
tr.on td:first-child { box-shadow: inset 3px 0 0 var(--clay); }
tr.late td:first-child { box-shadow: inset 3px 0 0 var(--bad); }
.track { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12.5px; }
.steps { display: flex; align-items: center; gap: 0; }
.steps i { width: 10px; height: 10px; border-radius: 50%; background: rgba(238,241,245,.14); flex: none; }
.steps i.d { background: var(--clay); }
.steps i.c { background: var(--clay); box-shadow: 0 0 0 3px rgba(240,174,194,.25); }
.steps i.x { background: var(--bad); box-shadow: 0 0 0 3px rgba(255,122,122,.25); }
.steps s { width: 16px; height: 2px; background: rgba(238,241,245,.14); text-decoration: none; }
.steps s.d { background: var(--clay); }
.panel { width: 360px; flex: none; }
.tl { position: relative; padding-left: 22px; }
.tl:before { content: ""; position: absolute; left: 5px; top: 6px; bottom: 6px; width: 2px; background: var(--line-2); }
.ev { position: relative; padding-bottom: 14px; font-size: 13px; }
.ev:before { content: ""; position: absolute; left: -21px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--panel); border: 2px solid var(--faint); }
.ev.d:before { background: var(--clay); border-color: var(--clay); }
.ev.c:before { background: var(--clay); border-color: var(--clay); box-shadow: 0 0 0 4px rgba(240,174,194,.25); }
.ev small { display: block; color: var(--faint); font-size: 11.5px; }
.ev.f { color: var(--faint); }
'''
def steps(n, bad=False):
    out=''
    for i in range(5):
        cls = 'd' if i < n else ('x' if (bad and i==n) else ('c' if i==n else ''))
        if i: out += f'<s class="{"d" if i<=n else ""}"></s>'
        out += f'<i class="{cls}"></i>'
    return f'<div class="steps">{out}</div>'
ship = [
 ('#0968',['loafers'],'Massimo Dutti','Nova Poshta','2045 0088 1244 71',2,False,'Arrived at Fitkit warehouse','today, 10:12','on'),
 ('#0951',['sneakers'],'Nike','—','no tracking',1,True,'No tracking for 3 days','Nov 18','late'),
 ('#0947',['sweater-grey','scarf'],'COS','Ukrposhta','0503 6448 1203 0',1,True,'No movement for 5 days','Nov 16','late'),
 ('#0939',['hoodie'],'Zara','Meest Express','MEEST 8830 2215',1,False,'On the way to warehouse','today, 08:40',''),
 ('#0932',['jeans','stripe'],'Reserved','Nova Poshta','2045 0099 8211 67',3,False,'Shipped to client','yesterday, 19:05',''),
 ('#0925',['sweatpants'],'H&amp;M','Meest Express','2045 0019 3774 12',4,False,'Delivered to client','yesterday, 14:30',''),
 ('#0918',['jacket-black'],'Zara','Nova Poshta','2045 0055 3000 81',3,False,'Courier delivers today','today, 09:55',''),
]
def srow(s):
    num,ph,shop,car,tr,n,bad,ev,t,cls = s
    imgs=''.join(f'<img src="assets/photos/{p}.jpg" class="th" style="margin-left:{-8 if k else 0}px;border:2px solid var(--panel);object-fit:cover">' for k,p in enumerate(ph))
    trk = f'<span class="badc" style="font-size:12.5px;font-weight:600">{tr}</span>' if tr=='no tracking' else f'<span class="track">{tr}</span>'
    evc = 'badc' if bad else ''
    return f'<tr class="{cls}"><td><div class="row" style="gap:10px"><div class="row" style="gap:0;width:62px">{imgs}</div><span class="num" style="font-size:15px">{num}</span></div></td><td>{shop}<div class="sub" style="font-size:12px">{car}</div></td><td>{trk}</td><td>{steps(n,bad)}</td><td><span class="{evc}" style="font-size:13px">{ev}</span><div class="sub" style="font-size:11.5px">{t}</div></td></tr>'
main7 = f'''
<div class="row">
  <div class="hicon">{ic('truck')}</div>
  <div class="grow"><h1>Tracking</h1><div class="sub">Placed purchases, tracking numbers, delivery and problems in transit</div></div>
  <button class="btn sel">All stores</button><button class="btn sel">All carriers</button>
</div>
<div class="kpis">
  <div class="card kpi"><div class="hicon">{ic('truck')}</div><div><b>38</b><div class="sub">coming from stores to warehouse</div></div></div>
  <div class="card kpi"><div class="hicon">{ic('box')}</div><div><b>12</b><div class="sub">at warehouse, waiting to ship</div></div></div>
  <div class="card kpi"><div class="hicon">{ic('send')}</div><div><b>21</b><div class="sub">on the way to clients</div></div></div>
  <div class="card kpi alert"><div class="hicon">{ic('alert')}</div><div><b>2</b><div class="sub">problems: no tracking or parcel stuck</div></div><i class="mk" style="margin-left:auto">1</i></div>
</div>
<div class="tabs"><a class="on">All <b>71</b></a><a>Store → warehouse <b>38</b></a><a>At warehouse <b>12</b></a><a>Warehouse → client <b>21</b></a><a class="red">Problems <b>2</b></a></div>
<div class="cols">
  <div class="card tbl" style="overflow:hidden">
    <table><tr><th>Order</th><th>Store · carrier</th><th>Tracking number</th><th>Stage <i class="mk" style="width:16px;height:16px;font-size:10px;vertical-align:middle">2</i></th><th>Last event</th></tr>{''.join(srow(s) for s in ship)}</table>
  </div>
  <div class="card panel">
    <div class="hd">{ic('box')}<h2>Parcel <span class="num">#0968</span></h2><i class="mk">3</i><span class="grow"></span><span class="st wait">At warehouse</span></div>
    <div class="bd">
      <div class="row" style="gap:12px;margin-bottom:14px"><img src="assets/photos/loafers.jpg" class="th" style="width:52px;height:66px;object-fit:cover"><div class="grow"><b>Leather loafers</b><div class="sub">Massimo Dutti · 38 · ₴5,899</div><div class="sub">Client: Olena Smyrnova</div></div></div>
      <div class="lbl">Tracking number</div>
      <div class="row" style="margin-bottom:16px"><span class="track grow">Nova Poshta 2045 0088 1244 71</span><span class="btn link">{ic('copy')} Copy</span></div>
      <div class="lbl">Parcel journey</div>
      <div class="tl">
        <div class="ev d"><b>Purchase placed</b><small>Massimo Dutti · Nov 17, 12:40</small></div>
        <div class="ev d"><b>Handed to Nova Poshta</b><small>Kyiv, store warehouse · Nov 18, 09:15</small></div>
        <div class="ev c"><b>Arrived at Fitkit warehouse</b><small>checked, 3 photos taken · today, 10:12</small></div>
        <div class="ev f"><b>Shipping to client</b><small>expected today</small></div>
        <div class="ev f"><b>Delivered</b><small>expected Nov 23</small></div>
      </div>
      <div class="row" style="gap:8px;margin-top:6px"><button class="btn" style="flex:1">{ic('msg')}Message client</button><button class="btn pri" style="flex:1">Ship →</button></div>
    </div>
  </div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Problems in transit are visible at once and have their own tab</span>
  <span><i class="mk">2</i>Stage: placed → in transit → warehouse → to client → delivered</span>
  <span><i class="mk">3</i>Click a row — parcel journey, copyable tracking and the next action</span>
</div>'''
open(os.path.join(OUT,'07-tracking.html'),'w').write(shell('Tracking','Tracking',main7,css7))

# ---------- 08 Current orders ----------
I['grid'] = '<rect x="3" y="3" width="7" height="18" rx="1.5"/><rect x="14" y="3" width="7" height="11" rx="1.5"/>'
I['list'] = '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'
css8 = css_common + '''
.seg { display: inline-flex; border: 1px solid var(--line-2); border-radius: 10px; overflow: hidden; }
.seg a { display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px; font-size: 13px; color: var(--muted); }
.seg a svg { width: 15px; height: 15px; }
.seg a.on { background: var(--clay-veil); color: var(--clay); font-weight: 600; }
.board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; align-items: start; }
.col { background: var(--paper); border: 1px solid var(--line); border-radius: 14px; padding: 10px; display: flex; flex-direction: column; gap: 10px; }
.colh { display: flex; align-items: center; gap: 8px; padding: 4px 6px 2px; font-weight: 600; }
.colh .dot { width: 8px; height: 8px; border-radius: 50%; }
.colh b { font-weight: 600; font-size: 12px; background: rgba(238,241,245,.08); border-radius: 9px; padding: 0 7px; color: var(--muted); }
.oc { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
.oc.prob { border-color: rgba(255,122,122,.4); box-shadow: inset 3px 0 0 var(--bad); }
.oc.drag { transform: rotate(-2deg); box-shadow: 0 14px 30px -12px rgba(0,0,0,.7), 0 0 0 1px rgba(240,174,194,.45); }
.oc .otop { display: flex; align-items: center; gap: 8px; }
.oc .thumbs { display: flex; } .oc .thumbs img { width: 30px; height: 38px; border-radius: 6px; border: 2px solid var(--panel); margin-left: -8px; object-fit: cover; } .oc .thumbs img:first-child { margin-left: 0; }
.oc .t { margin-left: auto; white-space: nowrap; font-size: 12px; font-weight: 600; color: var(--muted); }
.oc .t.red { color: var(--bad); } .oc .t.org { color: var(--wait); }
.flag { font-size: 12px; border-radius: 8px; padding: 5px 8px; display: flex; gap: 6px; align-items: center; }
.flag svg { width: 13px; height: 13px; flex: none; }
.flag.bad { background: var(--bad-bg); color: var(--bad); } .flag.wait { background: var(--wait-bg); color: var(--wait); }
.oc .bot { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 8px; }
.oc .bot svg { width: 14px; height: 14px; }
.unread { background: var(--clay); color: #1c1013; font-weight: 700; font-size: 11px; border-radius: 8px; padding: 0 6px; }
.addz { border: 1px dashed var(--line-2); border-radius: 12px; padding: 14px; text-align: center; color: var(--faint); font-size: 12.5px; }
'''
def oc(num, ph, client, c, info, time='', tcls='', flag=None, unread=0, resp=('AK','c2'), extra=''):
    imgs=''.join(f'<img src="assets/photos/{p}.jpg">' for p in ph)
    ini=''.join(w[0] for w in client.split())
    fl=''
    if flag:
        kind,text=flag; fl=f'<div class="flag {kind}">{ic("alert" if kind=="bad" else "clock")}{text}</div>'
    un=f'<span class="unread">{unread}</span>' if unread else ''
    return f'''<div class="oc {extra}"><div class="otop"><div class="thumbs">{imgs}</div><span class="num" style="font-size:16px">{num}</span><span class="t {tcls}">{time}</span></div>
<div class="who" style="gap:8px;font-size:13px"><div class="ava {c}" style="width:24px;height:24px;font-size:10px">{ini}</div><div class="grow">{client}<div class="sub" style="font-size:12px">{info}</div></div></div>{fl}
<div class="bot">{ic('msg')}{un or '—'}<span class="grow"></span><div class="ava {resp[1]}" style="width:22px;height:22px;font-size:9.5px">{resp[0]}</div></div></div>'''
def col(name, dotc, cnt, cards, add=False):
    a = '<div class="addz">drag a card to change its status</div>' if add else ''
    return f'<div class="col"><div class="colh"><span class="dot" style="background:{dotc}"></span>{name}<b>{cnt}</b></div>{cards}{a}</div>'
c_work = (oc('#001',['stripe','jacket-black','jeans-black'],'Maria Lebedenko','c2','3 items · ₴6,378','1h 20m','',('bad','No size M — asked in chat'),1)
 + oc('#008',['jacket-black'],'Olena Smyrnova','c5','1 item · ₴3,999','2h')
 + oc('#0993',['hoodie','sweatpants'],'Artem Bilyk','c3','2 items · ₴5,380','2h 40m')
 + oc('#0990',['scarf'],'Kseniia Orlyk','c4','1 item · ₴1,599','3h')
 + oc('#0987',['sweater-grey','jeans','loafers'],'Olha Petrenko','c3','3 items · ₴12,480','3h 30m','',None,0,('AK','c2'),'drag'))
c_wait = (oc('#0995',['top' if False else 'sneakers'],'Ihor Sokolenko','c4','1 item · ₴5,899','waiting 6h','org',('wait','Asked about ₴290 extra'),1)
 + oc('#0981',['stripe','sweatpants2'],'Pavlo Tykhonenko','c2','2 items · ₴4,480','waiting 26h','red',('bad','Client silent for over a day'))
 + oc('#0976',['jeans-black'],'Daria Vovk','c5','1 item · price ?','waiting 2h','org',('wait','Asked: W29 or W30?')))
c_bought = (oc('#0968',['loafers'],'Olena Smyrnova','c5','At warehouse · Nova Poshta','today','',None,0)
 + oc('#0951',['sneakers'],'Pavlo Tykhonenko','c2','Waiting for tracking · Nike','3 days','red',('bad','No tracking for 3 days'))
 + oc('#0947',['sweater-grey','scarf'],'Kseniia Orlyk','c4','In transit · Ukrposhta','5 days','red',('bad','No movement for 5 days'))
 + oc('#0939',['hoodie'],'Artem Bilyk','c3','In transit · Meest','yesterday'))
c_sent = (oc('#0932',['jeans','stripe'],'Olha Petrenko','c3','Nova Poshta · due Nov 23','yesterday')
 + oc('#0918',['jacket-black'],'Maria Lebedenko','c2','Courier delivers today','today'))
main8 = f'''
<div class="row">
  <div class="hicon">{ic('bag')}</div>
  <div class="grow"><h1>Current orders <span class="sub" style="font-size:22px;font-weight:500">· 14</span></h1><div class="sub">Orders the team is already working on</div></div>
  <div class="seg"><a class="on">Mine · 14</a><a>All · 96</a></div><i class="mk">1</i>
  <div class="seg"><a class="on">{ic('grid')}Board</a><a>{ic('list')}Table</a></div><i class="mk">2</i>
</div>
<div class="filters row" style="gap:8px">
  <button class="btn sel">All stores</button><button class="btn sel">Problems only</button><button class="btn sel">Sort: by due time</button>
  <span class="grow"></span><span class="sub">Time on a card is what’s left before due. Red ones have a problem</span><i class="mk">3</i>
</div>
<div class="board">
  {col('In progress','var(--muted)',5,c_work,True)}
  {col('Waiting for client','var(--wait)',3,c_wait)}
  {col('Purchased','var(--info)',4,c_bought)}
  {col('Shipped','var(--ok)',2,c_sent)}
</div>
<div class="legend">
  <span><i class="mk">1</i>“Mine” — your orders, “All” — the whole team (for the shift lead)</span>
  <span><i class="mk">2</i>Status board or a plain table</span>
  <span><i class="mk">3</i>Problems, due time and unread messages right on the card</span>
  <span>Drag a card to another column — the order status changes</span>
</div>'''
open(os.path.join(OUT,'08-current-orders.html'),'w').write(shell('Current orders','Current orders',main8,css8))
