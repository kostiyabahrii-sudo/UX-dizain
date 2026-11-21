# Генератор макетов 01-requests.html и 02-order-card.html: python3 mockups/build.py mockups
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
    items = [('inbox','Заявки','<span class="n red">12</span>'),('bag','Текущие заказы','<span class="n">14</span>'),('users','Клиенты',''),('truck','Отслеживание','<span class="n">2</span>'),('msg','Сообщения','<span class="n red">3</span>'),('chart','Аналитика','')]
    nav = ''.join(f'<a class="{"on" if t==active else ""}">{ic(i)}{t}{n}</a>' for i,t,n in items)
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>Fitkit — {title}</title>
<link rel="stylesheet" href="styles.css">
<style>{extra_css}</style></head>
<body><div class="app">
  <aside class="side">
    <div class="logo"><img src="assets/logo-mark.png" alt=""><b>Fitkit</b></div>
    <div class="cap">Основное</div>
    <nav class="nav">{nav}</nav>
    <div class="me"><div class="ava c2">АК</div><div>Анна Ковалёва<small>Байер · на смене</small></div></div>
  </aside>
  <div class="body">
    <div class="top"><div class="search">Поиск: № заявки, клиент, телефон, трек-номер…<kbd>⌘K</kbd></div><div class="bell">{ic('bell')}<i></i></div></div>
    <main class="main">{main}</main>
  </div>
</div></body></html>'''

# ---------- 01 Заявки ----------
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
 ('#001','late','Мария Лебедева','c2',3,['Zara','H&M'],'14 298 ₽','bad','Просрочена','08:40','<span class="timer red">−42 мин</span>','—'),
 ('#002','late','Игорь Соколов','c4',1,['Lamoda'],'5 490 ₽','bad','Просрочена','09:05','<span class="timer red">−15 мин</span>','—'),
 ('#003','','Ольга Петрова','c3',2,['Uniqlo'],'6 980 ₽','wait','Ожидает обработки','09:31','<span class="timer org">осталось 8 мин</span>','—'),
 ('#004','','Дарья Волкова','c5',4,['ASOS'],'цена не указана','new','Новая','09:52','<span class="timer">осталось 29 мин</span>','—'),
 ('#005','','Павел Тихонов','c2',1,['Nike'],'12 990 ₽','new','Новая','09:58','<span class="timer">осталось 35 мин</span>','—'),
 ('#006','','Ксения Орлова','c4',2,['Mango','COS'],'9 400 ₽','new','Новая','10:03','<span class="timer">осталось 40 мин</span>','—'),
 ('#007','','Артём Белов','c3',3,['Zara'],'цена не указана','new','Новая','10:11','<span class="timer">осталось 48 мин</span>','—'),
 ('#008','','Елена Смирнова','c5',1,['Massimo Dutti'],'8 999 ₽','','В работе','07:20','<span class="timer">—</span>','<div class="who"><div class="ava c2" style="width:24px;height:24px;font-size:10px">АК</div>Анна К.</div>'),
]
def tr(r):
    num,cls,name,c,n,shops,sum_,st,stt,date,tm,resp = r
    initials = ''.join(w[0] for w in name.split())
    P = {'#001':['stripe','jacket-black','jeans-black'],'#002':['hoodie'],'#003':['sweater-grey','jeans'],'#004':['hoodie','sweatpants','scarf'],'#005':['sneakers'],'#006':['scarf','loafers'],'#007':['stripe','sweatpants2','loafers'],'#008':['jacket-black']}
    th = ''.join(f'<img class="ph" src="assets/photos/{x}.jpg">' for x in P[num][:3])
    tags = ' '.join(f'<span class="tag">{s}</span>' for s in shops)
    word = 'товар' if n==1 else ('товара' if n<5 else 'товаров')
    sumcell = f'<span class="sub">{sum_}</span>' if 'не' in sum_ else sum_
    return f'<tr class="{cls}"><td><div class="cb"></div></td><td><div class="row" style="gap:12px"><div class="thumbs">{th}</div><div><div class="num">{num}</div><div class="sub" style="font-size:12px">{n} {word}</div></div></div></td><td><div class="who"><div class="ava {c}">{initials}</div>{name}</div></td><td>{tags}</td><td>{sumcell}</td><td><span class="st {st}">{stt}</span></td><td class="sub">{date}</td><td>{tm}</td><td>{resp}</td></tr>'
main1 = f'''
<div class="row">
  <div class="hicon">{ic('inbox')}</div>
  <div class="grow"><h1>Заявки <span class="sub" style="font-size:22px;font-weight:500">· 1 001</span></h1><div class="sub">Все поступившие заявки: новые, ожидающие обработки и просроченные</div></div>
  <button class="btn">{ic('download')}Экспорт</button>
  <button class="btn pri">Взять следующую заявку</button><i class="mk">1</i>
</div>
<div class="tabs"><a class="on">Все <b>1 001</b></a><a>Новые <b>12</b></a><a>Ожидают обработки <b>7</b></a><a class="red">Просроченные <b>2</b></a><i class="mk" style="align-self:center;margin-left:6px">2</i></div>
<div class="filters">
  <button class="btn sel">Все магазины</button><button class="btn sel">Последние 7 дней</button><button class="btn">{ic('cal')}15 ноя — 21 ноя 2026</button>
  <span class="grow"></span><button class="btn iconbtn">{ic('filter')}</button><button class="btn iconbtn">{ic('sliders')}</button>
</div>
<div class="card" style="overflow:hidden">
  <table>
    <tr><th style="width:44px"><div class="cb"></div></th><th>Заявка</th><th>Клиент</th><th>Магазины</th><th>Сумма</th><th>Статус</th><th>Поступила (сегодня)</th><th>Срок <i class="mk" style="width:16px;height:16px;font-size:10px">3</i></th><th>Ответственный</th></tr>
    {''.join(tr(r) for r in rows)}
  </table>
  <div class="foot">Страница 1 из 126<span class="grow"></span><button class="btn sm">← Назад</button><button class="btn sm">Вперёд →</button></div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Система выдаёт самую старую заявку — выбирать не нужно</span>
  <span><i class="mk">2</i>Вкладки: все, новые, ожидающие обработки, просроченные</span>
  <span><i class="mk">3</i>Сколько осталось до просрочки; просроченные — сверху, с красной полосой</span>
  <span>Клик по строке открывает карточку заявки</span>
</div>'''
open(os.path.join(OUT,'01-requests.html'),'w').write(shell('Заявки','Заявки',main1,css1))

# ---------- 02 Карточка заявки ----------
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
    pr = f'<b>{price}</b>' if price else '<b class="none">не указана</b>'
    return f'''<div class="it">
  <img class="ph" src="assets/photos/{photo}.jpg" style="width:76px;height:96px">
  <div class="grow">
    <div class="row" style="gap:8px"><div class="name">{name}</div><span class="tag">{shop}</span></div>
    <div class="grid"><div><span>Размер</span><b>{size}</b></div><div><span>Количество</span><b>{qty}</b></div><div><span>Цена</span>{pr}</div></div>
    <div class="cmt"><span>Комментарий клиента</span>{comment}</div>
  </div>
  <div class="acts">{status}<button class="btn pri">Открыть в магазине {ic('ext')}</button>{extra_btn}</div>
</div>'''
items = (item('stripe','Свитер в полоску','Zara','L','1','3 999 ₽','«Беру на размер больше, люблю свободно»','<span class="st ok">Проверен</span>')
 + item('jacket-black','Чёрный жакет','Zara','M','1','8 999 ₽','«Нужно до 25 ноября. Если M нет — можно S»','<span class="st bad">Нет размера</span>','<button class="btn sm">Написать клиенту</button>')
 + item('jeans-black','Джинсы широкие','H&amp;M','W28 L32','1','','«Тёмные, как на фото. Цену не нашла»','<span class="st wait">Проверяется</span>'))
main2 = f'''
<div class="row">
  <div class="hicon">{ic('back')}</div>
  <div class="grow">
    <div class="row" style="gap:10px"><h1 class="num" style="font-size:26px">#001</h1><span class="st wait">В работе</span></div>
    <div class="sub">Поступила 21 ноября 2026, 08:40 · из Telegram-бота · Мария Лебедева</div>
  </div>
  <button class="btn">{ic('msg')}Написать клиенту</button><button class="btn">{ic('users')}Передать коллеге</button>
</div>
<div class="cols">
  <div class="left">
    <div class="card">
      <div class="hd">{ic('bag')}<h2>Товары · 3</h2><i class="mk">1</i><span class="grow"></span><span class="sub">1 из 3 проверен</span></div>
      {items}
    </div>
    <div class="card">
      <div class="hd">{ic('user')}<h2>Клиент и доставка</h2></div>
      <div class="bd row" style="align-items:flex-start;gap:28px">
        <div class="who row" style="gap:10px"><div class="ava c2" style="width:40px;height:40px">МЛ</div><div><b>Мария Лебедева</b><div class="sub">7-й заказ · Telegram @maria_l</div><div class="sub">+7 916 ••• 45 12</div></div></div>
        <div class="grow"><div class="lbl">Адрес доставки</div>Москва, ул. Профсоюзная, 12, кв. 48<div class="sub">Курьер, 10:00–18:00</div><span class="copy">{ic('copy')}Копировать адрес</span></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('history')}<h2>История</h2></div>
      <div class="bd" style="padding-top:8px;padding-bottom:8px">
        <div class="act"><div class="dot">{ic('alert')}</div><div><b>Найдена проблема</b><div class="sub">Жакет: размера M нет в наличии</div></div><span class="d">21 ноя, 09:12</span></div>
        <div class="act"><div class="dot">{ic('user')}</div><div><b>Заявку взяла Анна Ковалёва</b><div class="sub">Статус: Новая → В работе</div></div><span class="d">21 ноя, 09:01</span></div>
        <div class="act"><div class="dot">{ic('inbox')}</div><div><b>Заявка поступила</b><div class="sub">3 товара, 6 фото, из Telegram-бота</div></div><span class="d">21 ноя, 08:40</span></div>
      </div>
    </div>
  </div>

  <div class="right">
    <div class="card">
      <div class="hd">{ic('sliders')}<h2>Управление заказом</h2><i class="mk">2</i></div>
      <div class="blk"><div class="lbl">Текущий статус</div><div class="row"><span class="st wait">В работе</span><span class="grow"></span><span class="sub">с 09:01 · осталось 1 ч 20 мин</span></div></div>
      <div class="blk"><div class="lbl">Ответственный</div><div class="row"><div class="ava c2">АК</div><div class="grow"><b>Анна Ковалёва</b><div class="sub">Байер</div></div><button class="btn sm">Сменить</button></div></div>
      <div class="blk"><div class="lbl">Общая стоимость</div>
        <div class="kv"><span>Товары (2 с ценой)</span>12 998 ₽</div>
        <div class="kv"><span>Джинсы</span><span>цена уточняется</span></div>
        <div class="kv"><span>Комиссия Fitkit</span>1 300 ₽</div>
        <div class="kv total"><b>Итого</b><b class="num">14 298 ₽</b></div>
      </div>
      <div class="blk"><div class="lbl">Изменить статус</div>
        <div class="stbtns"><button class="btn">Ждём клиента</button><button class="btn">Проблема</button><button class="btn pri" style="grid-column:1/3">Перевести в «Куплено» →</button><button class="btn danger" style="grid-column:1/3">Отменить заказ</button></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('alert')}<h2>Ошибки и проблемы · 2</h2><i class="mk">3</i></div>
      <div class="bd">
        <div class="prob bad">{ic('alert')}<div class="grow"><b>Нет размера M</b>Чёрный жакет · Zara</div><button class="btn sm">Спросить клиента</button></div>
        <div class="prob wait">{ic('clock')}<div class="grow"><b>Цена не указана</b>Джинсы широкие · H&amp;M — проверить на сайте</div></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('note')}<h2>Комментарии сотрудников</h2><i class="mk">4</i></div>
      <div class="bd">
        <div class="com"><div class="ava c3">ИР</div><div class="t"><b>Ирина Р.</b><small>старший смены · 09:20</small><div>Если жакета S тоже нет — предложи Massimo Dutti, клиентка там уже брала.</div></div></div>
        <div class="com"><div class="ava c2">АК</div><div class="t"><b>Анна К.</b><small>09:25</small><div>Ок, проверю наличие S и напишу клиенту.</div></div></div>
        <div class="input">Комментарий для коллег (клиент не увидит)…</div>
      </div>
    </div>
  </div>
</div>
<div class="legend">
  <span><i class="mk">1</i>Слева — товары: размер, количество, цена (если известна), комментарий клиента и кнопка перехода в магазин</span>
  <span><i class="mk">2</i>Справа — управление: статус, ответственный, стоимость и кнопки смены статуса</span>
  <span><i class="mk">3</i>Список ошибок и проблем по заявке</span>
  <span><i class="mk">4</i>Внутренние комментарии сотрудников</span>
</div>'''
open(os.path.join(OUT,'02-order-card.html'),'w').write(shell('Заявки','Заявка #001',main2,css2))

# ---------- 03 Сообщения (сотрудник) ----------
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
    <div class="hd row"><h2 class="grow">Сообщения</h2><i class="mk">1</i></div>
    <div class="search2">Найти клиента или заявку…</div>
    <div class="chips"><span class="chip on">Все</span><span class="chip">Без ответа · 3</span><span class="chip">Мои</span></div>
    {chatrow('Мария Лебедева','c2','#001','Давайте S, спасибо!','09:41','1',True)}
    {chatrow('Игорь Соколов','c4','#002','А почему цена выросла?','09:20','1')}
    {chatrow('Ольга Петрова','c3','#003','Скинула ещё одну ссылку','09:12','1')}
    {chatrow('Дарья Волкова','c5','#004','Вы: Проверяю наличие, вернусь…','08:55')}
    {chatrow('Павел Тихонов','c2','#005','Вы: Трек будет завтра','вчера')}
    {chatrow('Елена Смирнова','c4','#008','Спасибо, всё пришло!','вчера')}
  </div>
  <div class="conv">
    <div class="top2"><div class="ava c2">МЛ</div><div class="grow"><b>Мария Лебедева</b><div class="sub">заявка <span class="num" style="font-size:14px">#001</span> · Telegram · была в сети 2 мин назад</div></div><button class="btn">{ic('bag')}Открыть заявку</button></div>
    <div class="msgs">
      <div class="day">Сегодня</div>
      <div class="m cl">Здравствуйте! Скинула 3 вещи, посмотрите, пожалуйста 🙏<small>08:40</small></div>
      <div class="m me">Добрый день, Мария! Я Анна, ваш байер. Проверяю наличие и размеры, скоро напишу.<small>Анна · 09:05</small></div>
      <div class="m me">Чёрного жакета в размере M, к сожалению, нет. Есть S — та же цена, ссылка ниже. По меркам он вам подойдёт — берём S?
        <div class="prod"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:44px;height:56px"><div><b>Чёрный жакет</b><div class="sub">Zara · S · 8 999 ₽</div><div class="sub" style="color:var(--clay)">zara.com ↗</div></div></div>
        <small>Анна · 09:30</small></div>
      <div class="m cl">Давайте S, спасибо!<small>09:41</small></div>
    </div>
    <div class="composer"><button class="btn iconbtn">{ic('clip')}</button><button class="btn iconbtn">{ic('img')}</button><div class="in">Написать клиенту…</div><button class="btn pri">{ic('send')}Отправить</button><i class="mk">2</i></div>
  </div>
  <div class="ctx">
    <div class="row"><h2 class="grow">Заявка <span class="num">#001</span></h2><span class="st wait">В работе</span></div>
    <div><div class="lbl" style="font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px">Товары</div>
      <div class="mini"><img class="ph" src="assets/photos/stripe.jpg" style="width:32px;height:40px"><div class="grow">Свитер в полоску<div class="sub">L · 3 999 ₽</div></div><span class="st ok">ОК</span></div>
      <div class="mini"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:32px;height:40px"><div class="grow">Чёрный жакет<div class="sub">M → S · 8 999 ₽</div></div><span class="st wait">Изменить</span></div>
      <div class="mini"><img class="ph" src="assets/photos/jeans-black.jpg" style="width:32px;height:40px"><div class="grow">Джинсы широкие<div class="sub">W28 L32 · цена ?</div></div><span class="st">Проверка</span></div>
    </div>
    <div class="note">Клиент ответил «S». Поменяйте размер в заявке вручную — кнопка «Открыть заявку».<i class="mk" style="margin-left:6px;vertical-align:middle">3</i></div>
  </div>
</div>
<div class="legendbar"><div class="legend">
  <span><i class="mk">1</i>Все чаты с клиентами; каждый привязан к заявке</span>
  <span><i class="mk">2</i>Обычный чат: текст, фото, ссылка на товар — без автоматики и кнопок выбора</span>
  <span><i class="mk">3</i>Ответ клиента сотрудник сам переносит в заявку</span>
</div></div>'''
open(os.path.join(OUT,'03-messages.html'),'w').write(shell('Сообщения','Сообщения',main3,css3))

# ---------- 04 Чат у клиента ----------
page4 = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>Fitkit — чат клиента</title>
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
    <div class="ptop"><img src="assets/logo-mark.png" style="width:32px;height:32px;filter:invert(1)"><div class="grow"><b class="serif" style="font-size:18px;font-weight:600">Fitkit</b><div class="sub" style="font-size:12px">Связь с менеджером · Анна онлайн</div></div></div>
    <div class="ord"><span>Заказ <b style="color:var(--text)">#001</b> · 3 товара</span><span>В работе</span></div>
    <div class="pm">
      <div class="b me">Здравствуйте! Скинула 3 вещи, посмотрите, пожалуйста 🙏<small>08:40</small></div>
      <div class="b mgr">Добрый день, Мария! Я Анна, ваш байер. Проверяю наличие и размеры, скоро напишу.<small>Анна · 09:05</small></div>
      <div class="b mgr">Чёрного жакета в M нет. Есть S — та же цена, ссылка ниже. Берём S?
        <div class="prod"><img class="ph" src="assets/photos/jacket-black.jpg" style="width:38px;height:48px"><div><b>Чёрный жакет</b><div class="sub" style="font-size:11.5px">Zara · S · 8 999 ₽</div></div></div><small>Анна · 09:30</small></div>
      <div class="b me">Давайте S, спасибо!<small>09:41 ✓✓</small></div>
    </div>
    <div class="pin"><div class="in">Написать менеджеру…</div><div class="round">{ic('send')}</div></div>
  </div></div>
  <div class="expl">
    <div class="row" style="gap:10px"><span class="tag">Что видит клиент</span><i class="mk">1</i></div>
    <h1>Обычный чат с менеджером — без кнопок и автоматики</h1>
    <div class="pt"><div class="hicon">{ic('msg')}</div><div><b>Связь с менеджером</b>Клиент в любой момент пишет своему байеру — как в мессенджере. В шапке видно, кто его ведёт и что он онлайн.</div></div>
    <div class="pt"><div class="hicon">{ic('img')}</div><div><b>Фото и ссылки</b>Байер присылает фото или ссылку на вариант, клиент может прислать свои фото и ссылки в ответ.</div></div>
    <div class="pt"><div class="hicon">{ic('bag')}</div><div><b>Заказ сверху</b>Над перепиской — номер заказа и его статус, чтобы клиент понимал, о чём речь.</div></div>
  </div>
</div></div></body></html>'''
open(os.path.join(OUT,'04-client-chat.html'),'w').write(page4)
