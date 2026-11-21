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
 ('#001','late','Мария Лебедева','c2',3,['Zara','H&M'],'13 297 ₽','bad','Просрочена','08:40','<span class="timer red">−42 мин</span>','—'),
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
    th = ''.join('<div class="ph"></div>' for _ in range(min(n,3)))
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
def item(name, shop, size, qty, price, comment, status, extra_btn=''):
    pr = f'<b>{price}</b>' if price else '<b class="none">не указана</b>'
    return f'''<div class="it">
  <div class="ph" style="width:76px;height:96px"><span>фото</span></div>
  <div class="grow">
    <div class="row" style="gap:8px"><div class="name">{name}</div><span class="tag">{shop}</span></div>
    <div class="grid"><div><span>Размер</span><b>{size}</b></div><div><span>Количество</span><b>{qty}</b></div><div><span>Цена</span>{pr}</div></div>
    <div class="cmt"><span>Комментарий клиента</span>{comment}</div>
  </div>
  <div class="acts">{status}<button class="btn pri">Открыть в магазине {ic('ext')}</button>{extra_btn}</div>
</div>'''
items = (item('Рубашка оверсайз из хлопка','Zara','L','1','3 999 ₽','«Беру на размер больше, люблю свободно»','<span class="st ok">Проверен</span>')
 + item('Платье миди с поясом','Zara','M','1','5 999 ₽','«Нужно до 25 ноября. Если M нет — можно S, но только чёрное»','<span class="st bad">Нет размера</span>','<button class="btn sm">Предложить замену</button>')
 + item('Джинсы прямые','H&amp;M','W28 L32','1','','«Голубые, как на фото. Цену не нашла»','<span class="st wait">Проверяется</span>'))
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
        <div class="act"><div class="dot">{ic('alert')}</div><div><b>Найдена проблема</b><div class="sub">Платье: размера M нет в наличии</div></div><span class="d">21 ноя, 09:12</span></div>
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
        <div class="kv"><span>Товары (2 с ценой)</span>9 998 ₽</div>
        <div class="kv"><span>Джинсы</span><span>цена уточняется</span></div>
        <div class="kv"><span>Комиссия Fitkit</span>1 300 ₽</div>
        <div class="kv total"><b>Итого</b><b class="num">11 298 ₽</b></div>
      </div>
      <div class="blk"><div class="lbl">Изменить статус</div>
        <div class="stbtns"><button class="btn">Ждём клиента</button><button class="btn">Проблема</button><button class="btn pri" style="grid-column:1/3">Перевести в «Куплено» →</button><button class="btn danger" style="grid-column:1/3">Отменить заказ</button></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('alert')}<h2>Ошибки и проблемы · 2</h2><i class="mk">3</i></div>
      <div class="bd">
        <div class="prob bad">{ic('alert')}<div class="grow"><b>Нет размера M</b>Платье миди с поясом · Zara</div><button class="btn sm">Решить</button></div>
        <div class="prob wait">{ic('clock')}<div class="grow"><b>Цена не указана</b>Джинсы прямые · H&amp;M — проверить на сайте</div></div>
      </div>
    </div>
    <div class="card">
      <div class="hd">{ic('note')}<h2>Комментарии сотрудников</h2><i class="mk">4</i></div>
      <div class="bd">
        <div class="com"><div class="ava c3">ИР</div><div class="t"><b>Ирина Р.</b><small>старший смены · 09:20</small><div>Если платья S тоже нет — предложи Massimo Dutti, клиентка там уже брала.</div></div></div>
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
