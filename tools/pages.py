"""Builds the five pages of Space from shared partials.  Run: python3 tools/pages.py
Page bodies live here (home, about, pricing, contact) and in tools/src/features.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "src"

MARK = ('<svg class="logo__mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#CFFE25"/>'
        '<circle cx="16" cy="16" r="6.2" fill="#010104"/><ellipse cx="16" cy="16" rx="12" ry="4.2" fill="none" stroke="#010104" '
        'stroke-width="2.2" transform="rotate(-24 16 16)"/><circle cx="25" cy="8" r="1.6" fill="#010104"/></svg>')
LOGO = f'<a class="logo" href="index.html" aria-label="Space — на головну">{MARK}<span>Space<i>.</i></span></a>'
NAV = [("index.html", "Головна"), ("about.html", "Про нас"), ("features.html", "Можливості"), ("pricing.html", "Тарифи"), ("contact.html", "Контакти")]
CHECK = '<svg class="ck" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="#CFFE25"/><path d="m6 10.2 2.6 2.6L14 7.6" fill="none" stroke="#010104" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg viewBox="0 0 24 24"><path d="M12 2 15 9l7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z"/></svg>'


def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="nav" data-nav>
  {LOGO}
  <nav class="nav__links" aria-label="Основна навігація">{links}</nav>
  <a class="btn btn--white nav__cta" href="contact.html">Зв'язатися</a>
  <button class="nav__burger" type="button" aria-expanded="false" aria-controls="mnav" data-burger aria-label="Відкрити меню"><span></span><span></span></button>
</header>
<div class="mnav" id="mnav" hidden>
  {links}
  <a class="btn btn--lime" href="contact.html">Зв'язатися</a>
</div>"""


FOOTER = f"""<footer class="foot">
  <div class="foot__top">
    <div class="foot__brand">{LOGO}<p>Фінанси й процеси малого бізнесу з AI-помічником.</p><div class="foot__social"><a href="#" data-soon aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M6.5 9v9M6.5 6v.01M10.5 18v-5a3 3 0 0 1 6 0v5M10.5 9v9"/></svg></a><a href="#" data-soon aria-label="Instagram"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.5"/></svg></a><a href="#" data-soon aria-label="YouTube"><svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="4"/><path d="m10 9.5 5 2.5-5 2.5Z"/></svg></a></div><p class="foot__status"><i></i>Усі системи працюють</p></div>
    <nav class="foot__col" aria-label="Швидкі посилання"><p>Швидкі посилання</p>{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</nav>
    <nav class="foot__col" aria-label="Інші сторінки"><p>Сторінки</p><a href="#" data-soon>Блог</a><a href="#" data-soon>Кар'єра</a><a href="#" data-soon>Інтеграції</a><a href="#" data-soon>Статус сервісу</a></nav>
    <div class="foot__col"><p>Наш офіс</p><span>вул. Зоряна, 12, Київ, 01001, Україна</span><p class="foot__h2">Телефон</p><a href="tel:+380000000000">+380 00 000 00 00</a></div>
  </div>
  <div class="foot__bottom"><span>© 2026 Space. Концепт для портфоліо — бренд і тексти вигадані.</span><span class="foot__legal"><a href="#" data-soon>Політика конфіденційності</a><a href="#" data-soon>Умови використання</a></span></div>
</footer>"""


def page(fname, title, desc, body):
    modal = (SRC / "modal.html").read_text(encoding="utf-8")
    body = re.sub(r'<svg viewBox="0 0 32 32" aria-hidden="true">.*?</svg>', MARK.replace(' class="logo__mark"', ""), body, flags=re.S)
    html = f"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#010104">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/inter-cyrillic-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body class="pg-{fname.split('.')[0]}">
<a class="skip" href="#main">Перейти до вмісту</a>

{header(fname)}

<main id="main">
{body}
</main>

{FOOTER}

{modal}<div class="toast" data-toast role="status" aria-live="polite"></div>
<script src="js/main.js"></script>
</body>
</html>
"""
    (ROOT / fname).write_text(html, encoding="utf-8")


FEATURES = (SRC / "features.html").read_text(encoding="utf-8")
# shared blocks reused on several pages
LOGOS = re.search(r'<p class="logos__title">.*?</div>\s*</div>', FEATURES, re.S).group(0)
TRUST = re.search(r'<div class="trust__grid">.*?</article>\s*</div>', FEATURES, re.S).group(0)
REVIEWS = re.search(r'<!-- ===== reviews ===== -->.*?</section>', FEATURES, re.S).group(0)
FAQ = re.search(r'<!-- ===== faq ===== -->.*?</section>', FEATURES, re.S).group(0)
CTA = re.search(r'<!-- ===== cta ===== -->.*?</section>', FEATURES, re.S).group(0)
HERO_WIN = re.search(r'<div class="win">.*?</div>\s*</div>\s*</div>\s*</div>', FEATURES, re.S).group(0)
UI_OV = re.search(r'<div class="ov">.*?</div></div></div>', FEATURES, re.S).group(0)[:-12]

# ======================================================================
HOME = f"""<section class="hhero" id="top">
  <canvas class="stars" data-stars aria-hidden="true"></canvas>
  <div class="hhero__text">
    <p class="pill reveal"><i></i>Знайомтеся: AI-сервіс для фінансів бізнесу</p>
    <h1 class="h1 h1--xl reveal">Фінанси вашого бізнесу —<br>під повним контролем</h1>
    <p class="lead reveal">Space бачить усі ваші рахунки, платежі й податки одночасно — і підказує, що зробити сьогодні, щоб завтра заробити більше.</p>
    <div class="hhero__btns reveal"><button class="btn btn--lime" type="button" data-contact>→ Почати безкоштовно</button><a class="btn btn--white" href="pricing.html">Переглянути тарифи</a></div>
  </div>
  <div class="hhero__stage reveal" aria-hidden="true">
    <img class="hhero__planet" src="assets/photo/planet.webp" alt="">
    <div class="hhero__win">{HERO_WIN}</div>
  </div>
</section>
<section class="trust trust--home">
  {LOGOS}
  <p class="eyebrow reveal" style="margin-top:110px">Довіра</p>
  <h2 class="h2 center reveal">Нам довіряють понад<br>12&nbsp;000 компаній</h2>
  {TRUST}
</section>
<section class="bento-sec">
  <p class="eyebrow reveal">Платформа</p>
  <h2 class="h2 center reveal">Один простір для власника,<br>бухгалтера й команди</h2>
  <p class="lead center reveal">Один спільний простір для власника, бухгалтера й команди: кожен бачить своє і ніхто нічого не губить.</p>
  <div class="bento">
    <article class="card bento__big reveal">
      <span class="tag tag--green">Огляд інтерфейсу</span>
      <h3 class="h3">Зручний інтерфейс, який люблять з першого дня</h3>
      <p>Зрозуміла навігація й підказки замість інструкцій: розібратися з фінансами можна за п'ять хвилин.</p>
      <div class="win win--sm bento__ui" aria-hidden="true"><div class="win__bar"><i></i><i></i><i></i><span>Огляд</span></div>{UI_OV}</div>
    </article>
    <article class="card bento__card reveal">
      <h3>Легкі інтеграції</h3><p>Банки, каси, маркетплейси й бухгалтерські програми — підключення в кілька кліків.</p>
      <div class="integr" aria-hidden="true"><span style="--c:#CFFE25">mono</span><span style="--c:#7aa2ff">Приват</span><span style="--c:#ffb86b">Каса</span><span style="--c:#ff7a6b">Prom</span><span style="--c:#c9a2ff">M.E.Doc</span><span style="--c:#7af0c8">Google</span></div>
    </article>
    <article class="card bento__card bento__card--num reveal">
      <p class="bento__num">24/7</p><h3>Підтримка</h3><p>Відповідаємо українською вдень і вночі — у чаті, телефоном чи поштою.</p>
    </article>
    <article class="card bento__card reveal">
      <h3>Команда, якій довіряють</h3><p>Фінансисти й бухгалтери з досвідом понад 10 років допоможуть з налаштуванням.</p>
      <div class="faces" aria-hidden="true"><img src="assets/photo/review-1-sm.webp" alt=""><img src="assets/photo/review-2-sm.webp" alt=""><img src="assets/photo/review-3-sm.webp" alt=""><span>+12</span></div>
    </article>
  </div>
</section>
{REVIEWS}
<section class="sec-band">
  <div class="sec-band__head"><p class="eyebrow">Безпека</p><h2 class="h3">Захист даних банківського рівня</h2></div>
  <ul class="sec-band__list">
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg><b>Шифрування AES-256</b><span>Дані зашифровані під час передачі та зберігання</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg><b>Сервери в ЄС</b><span>Резервні копії щодня в двох дата-центрах</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.4 8 8 9 4.6-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg><b>Двофакторний вхід</b><span>Ролі й права доступу для кожного в команді</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg><b>Лише читання</b><span>Space не може провести платіж без вашого підтвердження</span></li>
  </ul>
</section>
{CTA}"""

# ----------------------------------------------------------------------
TEAM = [("Давид Чен", "Директор з маркетингу"), ("Яна Петрук", "UX-дизайнерка"), ("Леонід Жук", "Розробник"), ("Еміля Нгуєн", "Операційна директорка"),
        ("Михайло Бровко", "CEO"), ("Назар Романюк", "Продакт-менеджер"), ("Ольга Мартинюк", "Керівниця продажів"), ("Аліна Рахман", "Digital-стратегиня"),
        ("Євген Смик", "Бренд-менеджер"), ("Софія Кім", "SEO-спеціалістка")]
COLORS = ["#CFFE25", "#7aa2ff", "#ffb86b", "#ff7a6b", "#c9a2ff", "#7af0c8"]
TEAM_HTML = "".join(
    f'<article class="person reveal"><span class="person__av">{n.split()[0][0]}{n.split()[1][0]}</span><div><h3>{n}</h3><p>{r}</p></div><a class="person__in" href="#" data-soon aria-label="LinkedIn: {n}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 9v9M6.5 6v.01M10.5 18v-5a3 3 0 0 1 6 0v5M10.5 9v9" /></svg></a></article>'
    for i, (n, r) in enumerate(TEAM))
YEARS = [("2020", "Ідея на кухні", "Двоє друзів-бухгалтерів зробили таблицю, яка сама розносила платежі ФОП. За місяць нею користувалися 40 знайомих."),
         ("2021", "Перша версія", "Запустили веб-застосунок із підключенням банків і спільним доступом для бухгалтера й власника."),
         ("2022", "Аналітика", "Додали дашборди, прогноз грошового потоку та звіти, які можна показати банку чи інвестору."),
         ("2023", "Інтеграції", "Каси, маркетплейси й бухгалтерські програми — Space став центром фінансів бізнесу."),
         ("2024", "AI-помічник", "Автоматизація рутини: AI категоризує платежі, нагадує про податки й пише боржникам."),
         ("2025", "12 000 бізнесів", "Мобільний застосунок, нова швидкість і понад дванадцять тисяч компаній по всій Україні.")]
TL_BTNS = "".join(f'<button type="button" role="tab" aria-selected="{str(i == len(YEARS) - 1).lower()}" data-year="{i}">{y}</button>' for i, (y, _, _) in enumerate(YEARS))
TL_CARDS = "".join(f'<article class="tl__card{" is-on" if i == len(YEARS) - 1 else ""}" data-ycard="{i}"><span class="tag tag--green">{y}</span><h3 class="h3">{t}</h3><p>{d}</p></article>' for i, (y, t, d) in enumerate(YEARS))

ABOUT = f"""<section class="phero" id="top">
  <canvas class="stars" data-stars aria-hidden="true"></canvas>
  <div class="phero__text">
    <p class="pill reveal"><i></i>Про нас</p>
    <h1 class="h1 reveal">Ми — команда, яка допомагає бізнесу бачити свої гроші ясно</h1>
    <p class="lead reveal">Space створили бухгалтери, дизайнери й інженери, яким набридло, що підприємці дізнаються про проблеми з грошима останніми.</p>
  </div>
  <div class="phero__stats">
    <div class="card stat reveal"><span class="tag tag--green">Років на ринку</span><p class="stat__num"><span class="odo" data-odo="6">6</span><em>+</em></p><p>Від таблиці на кухні до сервісу для тисяч компаній.</p></div>
    <div class="card stat reveal"><span class="tag tag--yellow">Людей у команді</span><p class="stat__num"><span class="odo" data-odo="48">48</span></p><p>Київ, Львів і Дніпро — та віддалено по всьому світу.</p></div>
  </div>
</section>
<section class="trust">{LOGOS}</section>
<section class="values">
  <p class="eyebrow reveal">Цінності</p>
  <h2 class="h2 center reveal">Принципи, на яких<br>ми будуємо продукт</h2>
  <div class="values__grid">
    <article class="card value reveal"><span class="value__ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg></span><h3>Прозорість</h3><p>Ніяких дрібних шрифтів: ви завжди знаєте, що відбувається з вашими грошима й даними.</p></article>
    <article class="card value reveal"><span class="value__ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg></span><h3>Швидкість</h3><p>Випускаємо оновлення щотижня й відповідаємо в підтримці в середньому за 4 хвилини.</p></article>
    <article class="card value reveal"><span class="value__ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-9.3-9A5 5 0 0 1 12 6a5 5 0 0 1 9.3 5C19 15.6 12 20 12 20Z"/></svg></span><h3>Турбота</h3><p>Робимо продукт для людей, а не для звітів. Кожну функцію тестуємо з реальними підприємцями.</p></article>
  </div>
</section>
<section class="tl" data-timeline>
  <p class="eyebrow reveal">Історія</p>
  <h2 class="h2 center reveal">Шість років<br>зростання</h2>
  <p class="lead center reveal">Оберіть рік, щоб побачити, як ріс Space.</p>
  <div class="tl__track reveal" role="tablist" aria-label="Роки історії">{TL_BTNS}<span class="tl__bar" data-tl-bar></span></div>
  <div class="tl__cards" aria-live="polite">{TL_CARDS}</div>
</section>
<section class="team-sec">
  <p class="eyebrow reveal">Команда</p>
  <h2 class="h2 center reveal">Люди, які<br>створюють Space</h2>
  <div class="team-grid">{TEAM_HTML}</div>
</section>
{CTA}"""

# ----------------------------------------------------------------------
PLANS = [("start", "Старт", "Для ФОП і фрилансерів, які хочуть навести лад у фінансах.", False,
          ["1 бізнес і 2 банківські рахунки", "Автоматичні категорії платежів", "Нагадування про податки", "Рахунки клієнтам із шаблонів", "Підтримка в чаті"]),
         ("business", "Бізнес", "Для команд, які ростуть і працюють разом із бухгалтером.", True,
          ["До 5 бізнесів і без ліміту рахунків", "AI-помічник і прогноз грошового потоку", "Командний доступ і погодження витрат", "Інтеграції з касами й маркетплейсами", "Пріоритетна підтримка 24/7"]),
         ("corp", "Корпоративний", "Для мереж і холдингів зі складною структурою.", False,
          ["Необмежено бізнесів і користувачів", "Зведена звітність по групі компаній", "API та індивідуальні інтеграції", "Персональний менеджер", "SLA та аудит безпеки"])]
PLAN_HTML = "".join(f"""<article class="card plan{' plan--pop' if pop else ''} reveal">
      {'<span class="plan__pop">Найпопулярніший</span>' if pop else ''}
      <h3>{n}</h3><p class="plan__desc">{d}</p>
      <div class="plan__price"><b>Ціна за запитом</b><small data-bill>Щомісячна оплата · підберемо під ваш обсяг</small></div>
      <p class="plan__inc">Що входить:</p>
      <ul>{''.join(f'<li>{CHECK}{x}</li>' for x in items)}</ul>
      <button class="btn {'btn--lime' if pop else 'btn--white'} btn--wide" type="button" data-contact data-plan="{n}">Дізнатися ціну</button>
    </article>""" for pid, n, d, pop, items in PLANS)
ROWS = [("Бізнесів в акаунті", "1", "до 5", "Без ліміту"), ("Банківських рахунків", "2", "Без ліміту", "Без ліміту"), ("Користувачів", "2", "до 15", "Без ліміту"),
        ("AI-помічник", "—", "✓", "✓"), ("Прогноз грошового потоку", "—", "✓", "✓"), ("Інтеграції з касами", "—", "✓", "✓"),
        ("API та власні інтеграції", "—", "—", "✓"), ("Підтримка", "Чат", "24/7, телефон", "Персональний менеджер")]


def cell(v):
    if v == "✓":
        return f'<td>{CHECK}<span class="sr">Так</span></td>'
    if v == "—":
        return '<td class="no">—<span class="sr">Ні</span></td>'
    return f"<td>{v}</td>"


TABLE = "".join(f"<tr><th scope=\"row\">{r[0]}</th>{''.join(cell(v) for v in r[1:])}</tr>" for r in ROWS)

PRICING = f"""<section class="phero phero--center" id="top">
  <canvas class="stars" data-stars aria-hidden="true"></canvas>
  <div class="phero__text">
    <p class="pill reveal"><i></i>Тарифи</p>
    <h1 class="h1 reveal">Прості й прозорі тарифи,<br>створені для вас</h1>
    <p class="lead reveal">Ціну розраховуємо під кількість бізнесів, рахунків і людей у команді — щоб ви не платили за зайве. Перші 14 днів безкоштовно на будь-якому тарифі.</p>
    <div class="bill reveal" role="radiogroup" aria-label="Період оплати" data-bill-toggle>
      <button type="button" role="radio" aria-checked="true" data-period="month">Щомісяця</button>
      <button type="button" role="radio" aria-checked="false" data-period="year">Щороку <em>−20%</em></button>
    </div>
  </div>
</section>
<section class="plans-sec">
  <div class="plans">{PLAN_HTML}</div>
</section>
<section class="sec-band">
  <div class="sec-band__head"><p class="eyebrow">Безпека</p><h2 class="h3">Захист даних банківського рівня</h2></div>
  <ul class="sec-band__list">
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg><b>Шифрування AES-256</b><span>Дані зашифровані під час передачі та зберігання</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg><b>Сервери в ЄС</b><span>Резервні копії щодня в двох дата-центрах</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.4 8 8 9 4.6-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg><b>Двофакторний вхід</b><span>Ролі й права доступу для кожного в команді</span></li>
    <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg><b>Лише читання</b><span>Space не може провести платіж без вашого підтвердження</span></li>
  </ul>
</section>
<section class="compare">
  <p class="eyebrow reveal">Порівняння</p>
  <h2 class="h2 center reveal">Порівняйте тарифи</h2>
  <div class="compare__wrap reveal" tabindex="0" role="region" aria-label="Таблиця порівняння тарифів">
    <table class="compare__table">
      <thead><tr><th scope="col">Можливість</th><th scope="col">Старт</th><th scope="col" class="pop">Бізнес</th><th scope="col">Корпоративний</th></tr></thead>
      <tbody>{TABLE}<tr class="price-row"><th scope="row">Вартість</th><td><button class="link-btn" type="button" data-contact data-plan="Старт">Дізнатися ціну</button></td><td><button class="link-btn" type="button" data-contact data-plan="Бізнес">Дізнатися ціну</button></td><td><button class="link-btn" type="button" data-contact data-plan="Корпоративний">Дізнатися ціну</button></td></tr></tbody>
    </table>
  </div>
</section>
{FAQ}"""

# ----------------------------------------------------------------------
CONTACT = f"""<section class="phero phero--contact" id="top">
  <canvas class="stars" data-stars aria-hidden="true"></canvas>
  <div class="phero__text">
    <p class="pill reveal"><i></i>Зв'яжіться з нами</p>
    <h1 class="h1 reveal">Ваш наступний крок починається тут і зараз</h1>
    <p class="lead reveal">Розкажіть про свій бізнес — покажемо Space на ваших даних і підберемо тариф. Відповідаємо протягом години в робочий час.</p>
    <div class="card office reveal">
      <p class="office__h">Наш офіс</p>
      <div><small>Адреса</small><b>вул. Зоряна, 12, Київ, 01001</b></div>
      <div><small>Email</small><b><a href="mailto:hello@space.example">hello@space.example</a></b></div>
      <div><small>Телефон</small><b><a href="tel:+380000000000">+380 00 000 00 00</a></b></div>
    </div>
  </div>
  <div class="card cform reveal">
    <h2 class="h3">Пишіть нам будь-коли</h2>
    <form class="form" data-form="page" novalidate>
      <div class="form__row"><label>Ім'я<input name="name" autocomplete="name" placeholder="Олена"></label><label>Телефон<input name="phone" type="tel" autocomplete="tel" placeholder="+380 00 000 00 00"></label></div>
      <label>Email<input name="email" type="email" autocomplete="email" placeholder="olena@company.ua"></label>
      <label>Тема<select name="size"><option value="">Оберіть…</option><option>Демонстрація продукту</option><option>Питання про тарифи</option><option>Партнерство</option><option>Інше</option></select></label>
      <label>Повідомлення<textarea name="msg" rows="5" placeholder="Кілька слів про ваш бізнес і задачу"></textarea></label>
      <p class="form__err" data-err role="alert"></p>
      <p class="demo-note" role="note"><b>Це демо-сайт.</b> Повідомлення нікуди не надсилається — це концепт для портфоліо.</p>
      <button class="btn btn--lime btn--wide" type="submit">→ Надіслати повідомлення</button>
    </form>
    <div class="done" data-done hidden><span class="done__ok">✓</span><h3 class="h3">Повідомлення надіслано!</h3><p data-done-text></p><button class="btn btn--white" type="button" data-reset>Написати ще</button></div>
  </div>
</section>
{FAQ}"""

FEAT_BODY = FEATURES
page("index.html", "Space — фінанси та процеси бізнесу з AI", "Space — AI-сервіс для фінансів малого бізнесу: рахунки, платежі, податки й аналітика в одному вікні.", HOME)
page("features.html", "Можливості — Space", "Можливості Space: дашборди, конструктор звітів, шаблони, командна робота й онлайн-оплати.", FEAT_BODY)
page("about.html", "Про нас — Space", "Історія Space, наші цінності та команда, яка допомагає бізнесу бачити свої гроші ясно.", ABOUT)
page("pricing.html", "Тарифи — Space", "Тарифи Space: Старт, Бізнес і Корпоративний. Ціну підбираємо під ваш бізнес, 14 днів безкоштовно.", PRICING)
page("contact.html", "Контакти — Space", "Зв'яжіться з командою Space: демонстрація продукту, питання про тарифи та партнерство.", CONTACT)
print("built 5 pages")
