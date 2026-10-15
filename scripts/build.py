#!/usr/bin/env python3
"""Build the portfolio and its curated, bilingual public game guide. No dependencies."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
import shutil
import math

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://wolfs0ng.github.io/'
MEDIA = json.loads((ROOT / 'content/media.json').read_text())
LINKEDIN = 'https://www.linkedin.com/in/tarasenko-dmytro/'
HYDRA = 'https://www.linkedin.com/company/mad-hydra-production/'

def bi(ua, en):
    return f'<span data-i18n="ua">{ua}</span><span data-i18n="en" hidden>{en}</span>'

def ext(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{escape(url)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true"> ↗</span></a>'

def button(url, label, secondary=False, extra=''):
    if ".html" in url and "/wiki/" not in url and "data-wiki-entry" not in extra:
        extra += ' data-keep-lang'
    return f'<a class="button{" secondary" if secondary else ""}" href="{url}" {extra}>{label}</a>'

def current(active, value):
    return f'aria-current="{value}"' if active else ""

def header(prefix='', active='', fixed=None, alternate=None):
    home = prefix + 'index.html'
    projects = prefix + 'projects.html'
    contact = home + '#contact'
    nav = f'''<a class="brand" href="{home}" data-keep-lang aria-label="Dmytro Tarasenko — {"головна" if fixed != "en" else "home"}"><img class="brand-logo" src="{prefix}assets/images/branding/wolfsong-mark.webp" width="52" height="52" alt="" decoding="async"><span class="brand-name">Dmytro Tarasenko</span></a>
    <nav class="main-nav" aria-label="{ 'Основна навігація' if fixed != 'en' else 'Main navigation'}">
      <a href="{projects}" {'aria-current="page"' if active == 'projects' else ''} data-keep-lang>{bi('Проєкти', 'Work')}</a>
      <a href="{home}#experience" data-keep-lang>{bi('Досвід', 'Experience')}</a>
      <a href="{contact}" data-keep-lang>{bi('Контакти', 'Contact')}</a>
    </nav>'''
    if fixed:
        lang = ''.join(f'<a href="{alternate if l != fixed else "#"}" data-locale="{l}" lang="{"uk" if l == "ua" else "en"}" {current(l == fixed, "true")}>{l.upper()}</a>' for l in ['ua','en'])
    else:
        lang = '<button type="button" data-lang="ua" aria-pressed="true">UA</button><button type="button" data-lang="en" aria-pressed="false">EN</button>'
    return f'<a class="skip-link" href="#main">{bi("До вмісту", "Skip to content")}</a><header class="site-header"><div class="header-inner">{nav}<div class="language" aria-label="Language">{lang}</div></div></header>'

def footer(prefix=''):
    return f'''<footer class="footer wrap"><div><a class="footer-name" href="{prefix}index.html" data-keep-lang>Dmytro Tarasenko</a><p>{bi('Ігрові системи. Зрозумілі рішення.', 'Game systems. Thoughtful decisions.')}</p></div><div class="footer-links">{ext(LINKEDIN, 'LinkedIn')}{ext('https://github.com/Wolfs0ng','GitHub')}<a href="mailto:nemesidik@gmail.com">Email ↗</a></div><small>© <span data-year>2026</span> Dmytro Tarasenko</small></footer>'''

def document(body, title, desc, path, prefix='', active='', fixed=None, alternate=None, extra=''):
    lang = 'en' if fixed == 'en' else 'uk'
    en_title = title if fixed else title.replace('Дмитро Тарасенко', 'Dmytro Tarasenko').replace('Проєкти', 'Selected work')
    canonical = BASE + path
    alternate_tags = ''
    if fixed and alternate:
        from urllib.parse import urljoin
        alternate_tags = f'<link rel="alternate" hreflang="{"en" if fixed == "ua" else "uk"}" href="{urljoin(canonical, alternate)}">'
    out = f'''<!doctype html>
<html lang="{lang}" {f'data-fixed-lang="{fixed}"' if fixed else ''}>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark"><title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}"><link rel="canonical" href="{canonical}">{alternate_tags}
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}assets/images/social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{escape(desc)}"><meta name="twitter:image" content="{BASE}assets/images/social-card.png"><meta name="theme-color" content="#101322">
<link rel="icon" href="{prefix}assets/images/favicon.ico?v=2" sizes="any">
<link rel="icon" href="{prefix}assets/images/favicon-32.png?v=2" type="image/png" sizes="32x32">
<link rel="icon" href="{prefix}assets/images/favicon-192.png?v=2" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{prefix}assets/images/branding/wolfsong-180.png">
<link rel="stylesheet" href="{prefix}styles.css?v=20261015-readability2"><script src="{prefix}assets/js/site.js" defer></script>{extra}</head>
<body data-title-ua="{escape(title)}" data-title-en="{escape(en_title)}">{header(prefix,active,fixed,alternate)}{body}{footer(prefix)}
<dialog class="lightbox" aria-label="{ 'Image viewer' if fixed == 'en' else 'Перегляд зображення' }"><button type="button" class="lightbox-close" aria-label="{ 'Close' if fixed == 'en' else 'Закрити' }">×</button><img alt=""><p></p></dialog>
</body></html>'''
    if fixed == 'en':
        out = out.replace('data-i18n="ua">', 'data-i18n="ua" hidden>').replace('data-i18n="en" hidden>', 'data-i18n="en">')
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)

def shot(name, ua, en, prefix='', eager=False, cls=''):
    return f'''<a class="shot {cls}" href="{prefix}assets/images/carnage-club/{name}.webp" data-lightbox data-caption-ua="{escape(ua)}" data-caption-en="{escape(en)}"><img src="{prefix}assets/images/carnage-club/{name}-small.webp" width="432" height="768" alt="Carnage Club — {escape(en)}" loading="{'eager' if eager else 'lazy'}" decoding="async"></a>'''

def project_card(key, ua, en, role_ua, role_en):
    m=MEDIA[key]
    return f'''<article class="project-card"><a href="projects.html#{key}" class="project-card-media {key}" data-keep-lang><img src="{escape(m['screens'][0])}" alt="{escape(m['name'])} — official screenshot" loading="lazy" decoding="async" width="{'406' if key=='azzl' else '222' if key=='kitty' else '221'}" height="{'228' if key=='azzl' else '480'}"><span class="media-arrow" aria-hidden="true">↗</span></a><div class="project-card-body"><p class="eyebrow">{bi(role_ua,role_en)}</p><h3><a href="projects.html#{key}" data-keep-lang>{'AZZL' if key=='azzl' else m['name']}</a></h3><p>{bi(ua,en)}</p><a class="text-link" href="projects.html#{key}" data-keep-lang>{bi('Про мою роботу','My contribution')} <span aria-hidden="true">→</span></a></div></article>'''

def home():
    b=f'''<main id="main">
<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="tiny-line"></span> SENIOR / LEAD UNITY DEVELOPER</p><h1>{bi('Дмитро<br>Тарасенко<span class="dot">.</span>', 'Dmytro<br>Tarasenko<span class="dot">.</span>')}</h1><p class="hero-lead">{bi('Створюю ігри.<br>Від першої механіки до релізу.', 'Building games.<br>From the first mechanic to release.')}</p><p class="hero-description">{bi('13+ років у розробці мобільних та PC-ігор. Геймплей, архітектура, продуктивність і технічне лідерство.', '13+ years developing mobile and PC games. Gameplay, architecture, performance, and technical leadership.')}</p><div class="actions">{button('#work',bi('Дивитися проєкти','Explore my work')+' <span aria-hidden="true">↘</span>')}{button('assets/docs/Unity_Dmytro_Tarasenko.pdf',bi('Резюме','Resume')+' <span aria-hidden="true">↗</span>',True,'target="_blank" rel="noopener"')}</div><div class="hero-links">{ext(LINKEDIN,'LinkedIn','button secondary')}{button('mailto:nemesidik@gmail.com',bi('Написати мені','Contact me')+' <span aria-hidden="true">↗</span>',True)}</div></div>
<div class="hero-feature"><a href="projects/carnage-club/index.html" class="feature-label" data-keep-lang><span class="status-dot"></span>{bi('Мій авторський проєкт','My solo project')}<span aria-hidden="true">↗</span></a><div class="phone-stage">{shot('map','Дослідження карти','Exploring the map',eager=True,cls='phone-left')}{shot('battle-titan','Дуель із Titan','Duel with Titan',eager=True,cls='phone-main')}{shot('dialogue','Діалог з Experiment 403','Conversation with Experiment 403',eager=True,cls='phone-right')}</div><div class="feature-caption"><a href="projects/carnage-club/index.html" data-keep-lang><strong>Carnage Club</strong><span>{bi('Тактичні дуелі. Світ, що пам’ятає.', 'Tactical duels. A world that remembers.')}</span></a></div></div></section>
<div class="expertise-strip wrap"><div><span>01</span><strong>{bi('Геймплейні системи','Gameplay systems')}</strong><p>{bi('Механіки, прогресія, адаптивні супротивники','Mechanics, progression, adaptive opponents')}</p></div><div><span>02</span><strong>{bi('Архітектура й продуктивність','Architecture & performance')}</strong><p>{bi('Системи, які зручно розвивати й підтримувати','Systems built to evolve and stay maintainable')}</p></div><div><span>03</span><strong>{bi('Технічне лідерство','Technical leadership')}</strong><p>{bi('Планування, код-рев’ю та розвиток команди','Planning, code review, and team development')}</p></div></div>
<section id="work" class="section wrap"><div class="section-heading"><div><p class="eyebrow">{bi('ВІД ВЛАСНОЇ ГРИ ДО LIVE-ПРОДУКТІВ','FROM SOLO DEVELOPMENT TO LIVE PRODUCTS')}</p><h2>{bi('Вибрані проєкти','Selected work')}</h2></div><a class="text-link" href="projects.html" data-keep-lang>{bi('Усі проєкти','All projects')} →</a></div>
<article class="featured-work"><div><p class="eyebrow">SOLO DEVELOPER · UNITY · MOBILE</p><h3>Carnage Club</h3><p>{bi('Похмура покрокова RPG, де супротивники вчаться на твоїх звичках. Авторський проєкт: від бойової системи й AI до прогресії та ігрових інструментів.', 'A dark turn-based RPG where opponents learn your habits. A solo project spanning combat, adaptive AI, progression, and development tools.')}</p><div class="tags"><span>Adaptive AI</span><span>Turn-based RPG</span><span>{bi('У розробці','In development')}</span></div><div class="actions">{button('projects/carnage-club/index.html',bi('Познайомитися з грою','Discover the game')+' →')}{button('projects/carnage-club/wiki/ua/01-gdd.html',bi('Читати Wiki','Read the guide'),True,'data-wiki-entry')}</div></div><div class="featured-shots">{shot('map','Карта кампанії','Campaign map')}{shot('inventory','Спорядження героя','Character equipment')}</div></article>
<div class="project-grid">{project_card('kitty','Геймплей, UI/UX, аналітика й оптимізація мобільної puzzle-гри.', 'Gameplay, UI/UX, analytics, and optimization for a mobile puzzle game.','Senior Unity Developer · Smart Project','Senior Unity Developer · Smart Project')}{project_card('scatter','Розвиток live-продукту, монетизація, стабільність і робота команди.', 'Live product development, monetization, stability, and team leadership.','Lead Unity Developer · Murka','Lead Unity Developer · Murka')}{project_card('azzl','Ігровий контент і функціональність анімаційної puzzle-гри.', 'Game content and features for an animated puzzle game.','Unity Developer · Jutiful','Unity Developer · Jutiful')}</div></section>
<section id="experience" class="section wrap"><div class="section-heading"><div><p class="eyebrow">{bi('ПРАКТИКА, ЩО СТОЇТЬ ЗА ПРОЄКТАМИ','THE EXPERIENCE BEHIND THE WORK')}</p><h2>{bi('Досвід розробки','Experience')}</h2></div>{ext('assets/docs/Unity_Dmytro_Tarasenko.pdf',bi('Повне резюме','Full resume'))}</div><div class="experience-layout"><div class="experience-intro"><h3>{bi('Від прототипу<br>до живої гри.', 'From a prototype<br>to a live game.')}</h3><p>{bi('Працюю з механіками, системами й людьми. Поєдную розробку з плануванням, рев’ю архітектури та підтримкою команди.', 'I work across mechanics, systems, and teams, combining development with planning, architectural review, and mentoring.')}</p><div class="skill-list"><span>Unity / C# / .NET</span><span>UniTask / Addressables</span><span>Mirror / REST APIs</span><span>Profiling / CI/CD</span><span>Firebase / AppLovin MAX</span></div></div><div class="timeline">'''
    jobs=[
      ('08/2024 — 08/2025','Smart Project Development','Senior Unity Developer','Kitty Sort: геймплей, UI/UX, VFX та монетизація. Зростання рекламного доходу на 9%, скорочення часу запуску гри й рівнів на 27%.','Kitty Sort: gameplay, UI/UX, VFX, and monetization. Ad revenue increased by 9%; game and level startup times decreased by 27%.'),
      ('05/2024 — 08/2024','Utin Computer','Interim Chief Technology Officer','Технічні стандарти, архітектурні рев’ю та покращення процесів розробки кількох проєктів.','Technical standards, architectural reviews, and development process improvements across several projects.'),
      ('01/2023 — 12/2023','Whimsy Games','Lead Unity Developer','Мультиплеєрний brawler: геймплей і клієнт-серверна архітектура на Mirror, технічне планування й менторинг.','Multiplayer brawler: gameplay and client-server architecture with Mirror, technical planning, and mentoring.'),
      ('03/2017 — 12/2022','Murka','Lead Unity Developer','Scatter Slots і Slots on Tour: LiveOps, монетизація та стабільність. Зростання retention на 30%, річного доходу на 12%, стабільності — з 83% до 99%.','Scatter Slots and Slots on Tour: LiveOps, monetization, and stability. Retention increased by 30%, annual revenue by 12%, and runtime stability improved from 83% to 99%.'),
      ('2015 — 2017','eJaw','Lead Unity3D Developer','Ігрові системи для mobile, PC і VR; розробка космічної аркади від концепції до релізу.','Gameplay systems for mobile, PC, and VR; a space arcade game developed from concept to release.'),
      ('08/2014 — 12/2015','Jutiful','Unity3D Developer','Інвесторські демо, прототипи, ігровий контент і функціональність мобільної puzzle-гри.','Investor demos, prototypes, game content, and features for a mobile puzzle title.')]
    for date,company,role,ua,en in jobs:
        b+=f'<article class="timeline-item"><time>{date}</time><div><h3>{company}</h3><p class="job-role">{role}</p><p>{bi(ua,en)}</p></div></article>'
    b+=f'''</div></div></section><section id="contact" class="contact-section wrap"><div><p class="eyebrow">{bi('НАСТУПНА РОЗМОВА','LET’S TALK')}</p><h2>{bi('Маєш цікавий<br>ігровий проєкт?', 'Have a game<br>project in mind?')}</h2><p>{bi('Напиши — обговоримо гру, команду та технічні задачі.', 'Let’s talk about the game, the team, and the technical challenges.')}</p></div><div class="contact-actions"><a class="email-link" href="mailto:nemesidik@gmail.com">nemesidik@gmail.com <span aria-hidden="true">↗</span></a><div>{ext(LINKEDIN,'LinkedIn')}{ext('https://github.com/Wolfs0ng','GitHub')}{ext('https://t.me/Wolfs0ng','Telegram')}</div><a class="text-link" href="assets/docs/Unity_Dmytro_Tarasenko.pdf" download>{bi('Завантажити резюме','Download resume')} ↓</a></div></section></main>'''
    document(b,'Дмитро Тарасенко — Senior / Lead Unity Developer','Senior / Lead Unity Developer. 13+ years in mobile and PC games: gameplay, architecture, multiplayer, performance, and technical leadership.','index.html')

def media_gallery(key):
    m=MEDIA[key]
    width = 406 if key == "azzl" else 222 if key == "kitty" else 221
    height = 228 if key == "azzl" else 480
    images=''.join(f'<a href="{escape(m["full_screens"][i])}" data-lightbox data-caption-ua="{escape(m["name"])} — офіційний скриншот" data-caption-en="{escape(m["name"])} — official screenshot"><img src="{escape(u)}" alt="{escape(m["name"])} — official screenshot {i+1}" width="{width}" height="{height}" loading="lazy" decoding="async"></a>' for i,u in enumerate(m['screens']))
    result=f'<div class="external-gallery {key}">{images}</div>'
    if m.get('video'):
        result+=f'<a class="video-link" href="{m["video_source"]}" target="_blank" rel="noopener noreferrer"><span class="play-icon" aria-hidden="true">▶</span><span>{bi("Відео з Google Play", "Video from Google Play") if key == "kitty" else bi("Офіційний трейлер", "Official trailer")}<small>YouTube ↗</small></span></a>'
    result+=f'<p class="media-credit">{ext(m["source"],bi("Медіа власника гри · App Store", "Publisher media · App Store"))}</p>'
    return result

def projects():
    b=f'''<main id="main" class="wrap"><section class="page-intro"><p class="eyebrow">{bi('ПОРТФОЛІО','PORTFOLIO')}</p><h1>{bi('Ігри та моя<br>робота над ними<span class="dot">.</span>', 'The games.<br>The work behind them<span class="dot">.</span>')}</h1><p>{bi('Авторський проєкт, мобільні puzzle-ігри та продукти з тривалою live-підтримкою.', 'A solo project, mobile puzzle games, and products supported through years of live operation.')}</p><nav class="project-jump" aria-label="Projects"><a href="#carnage-club">Carnage Club</a><a href="#kitty">Kitty Sort</a><a href="#scatter">Scatter Slots</a><a href="#azzl">AZZL</a></nav></section>
<section id="carnage-club" class="project-detail"><div class="project-detail-copy"><p class="eyebrow">SOLO DEVELOPMENT · MOBILE · {bi('У РОЗРОБЦІ','IN DEVELOPMENT')}</p><h2>Carnage Club</h2><p class="project-lead">{bi('Тактична RPG, де супротивник запам’ятовує твій стиль.', 'A tactical RPG where your opponent remembers how you fight.')}</p><p>{bi('Покрокові дуелі, розвиток власного білда та дослідження похмурого готичного світу. Повністю авторська розробка: бойові механіки, адаптивні супротивники, прогресія й інструменти.', 'Turn-based duels, character builds, and exploration in a dark gothic world. Solo development covering combat mechanics, adaptive opponents, progression, and tools.')}</p><div class="tags"><span>Unity / C#</span><span>Adaptive AI</span><span>RPG</span></div><div class="actions">{button('projects/carnage-club/index.html',bi('Детальніше про гру','Explore the game')+' →')}{button('projects/carnage-club/wiki/ua/01-gdd.html',bi('Читати Wiki','Read the guide'),True,'data-wiki-entry')}</div></div><div class="featured-shots">{shot('battle-titan','Бій із Titan','Battle with Titan')}{shot('map','Карта кампанії','Campaign map')}</div></section>'''
    entries=[
      ('kitty','Smart Project Development · 08/2024 — 08/2025','Senior Unity Developer','Казуальна puzzle-гра з сортуванням кольорових котів.','A casual puzzle game about sorting colorful cats.',[
       ('Геймплейні системи, UI/UX, анімації та VFX.','Gameplay systems, UI/UX, animations, and VFX.'),('Інтеграція Firebase Analytics і монетизації AppLovin MAX.','Firebase Analytics and AppLovin MAX monetization integration.'),('Профілювання й оптимізація продуктивності на Android та iOS.','Profiling and performance optimization on Android and iOS.')],
       [('+9%','рекламного доходу','ad revenue'),('−27%','часу запуску гри й рівнів','game & level startup time')],
       'https://play.google.com/store/apps/details?id=org.smapps.sort'),
      ('scatter','Murka · 03/2017 — 12/2022','Lead Unity Developer','Соціальний казино-продукт із тривалою live-підтримкою.','A social casino product supported through long-term live operation.',[
       ('Геймплей, LiveOps-функції та монетизаційний контент.','Gameplay, LiveOps features, and monetization content.'),('Покращення стабільності та зменшення кількості збоїв у продакшені.','Production stability improvements and crash reduction.'),('Менторинг, документація, онбординг і процеси розробки.','Mentoring, documentation, onboarding, and development workflows.')],
       [('+30%','retention','retention'),('99%','стабільності виконання','runtime stability')],
       'https://play.google.com/store/apps/details?id=com.murka.scatterslots'),
      ('azzl','Jutiful · 08/2014 — 12/2015','Unity3D Developer','Анімаційна puzzle-гра, в якій зображення оживає після розв’язання.','An animated puzzle game where solving the image brings a scene to life.',[
       ('Створення ігрового контенту та реалізація функціональності.','Game content creation and feature implementation.'),('Робота над прототипами та proof-of-concept у команді Jutiful.','Prototypes and proof-of-concept development at Jutiful.')],[],None)]
    for key,company,role,ua,en,contributions,stats,play in entries:
        m=MEDIA[key]
        b+=f'<section id="{key}" class="project-detail"><div class="project-detail-copy"><p class="eyebrow">{company}</p><h2>{"AZZL" if key=="azzl" else m["name"]}</h2><p class="role-label">{role}</p><p class="project-lead">{bi(ua,en)}</p><h3>{bi("Мій внесок", "My contribution")}</h3><ul class="contributions">'+''.join(f'<li>{bi(a,c)}</li>' for a,c in contributions)+'</ul>'
        if stats:
            b+='<div class="result-row">'+''.join(f'<div><strong>{n}</strong><span>{bi(a,c)}</span></div>' for n,a,c in stats)+'</div>'
            if key=='scatter': b+=f'<p class="small muted">{bi("Результати з резюме стосуються роботи над продуктами Murka — Scatter Slots і Slots on Tour.", "Resume results cover work across Murka products: Scatter Slots and Slots on Tour.")}</p>'
        b+=f'<div class="actions">{ext(m["store"],"App Store","button secondary")}{ext(play,"Google Play","button secondary") if play else ""}</div></div><div class="project-media">{media_gallery(key)}</div></section>'
    b+=f'<p class="media-note">{bi("Скриншоти та трейлери комерційних ігор належать їхнім правовласникам. Публічні матеріали можуть показувати новіші версії, ніж ті, над якими я працював.", "Commercial game screenshots and trailers belong to their respective owners. Public media may show versions released after my involvement.")}</p><section class="compact-contact"><h2>{bi("Поговорімо про твій проєкт", "Let’s talk about your project")}</h2>{button("mailto:nemesidik@gmail.com",bi("Написати мені","Contact me")+" ↗")}</section></main>'
    document(b,'Проєкти — Дмитро Тарасенко','Selected game development work: Carnage Club, Kitty Sort, Scatter Slots, and AZZL. Roles, contributions, results, screenshots, and trailers.','projects.html',active='projects')

def carnage():
    pre='../../'
    b=f'''<main id="main"><section class="case-hero wrap"><div><a class="text-link back-link" href="../../projects.html" data-keep-lang>← {bi('Усі проєкти','All projects')}</a><p class="eyebrow">SOLO DEVELOPER · UNITY · MOBILE</p><h1>Carnage<br>Club<span class="dot">.</span></h1><p class="case-tagline">{bi('Світ пам’ятає<br>твої звички.', 'The world remembers<br>your habits.')}</p><p class="hero-description">{bi('Похмура покрокова RPG про тактичні дуелі, власний бойовий стиль і таємниці занепалого ордену мисливців.', 'A dark turn-based RPG about tactical duels, finding your own fighting style, and the secrets of a fallen hunters’ order.')}</p><div class="actions">{button('wiki/ua/01-gdd.html',bi('Читати про гру','Read the game guide')+' →',False,'data-wiki-entry')}{button('#gallery',bi('Скриншоти','Screenshots'),True)}</div><p class="development-status"><span class="status-dot"></span>{bi('Гра в розробці · Кадри поточної версії', 'In development · Screens from the current version')}</p></div><div class="case-stage">{shot('main-menu','Головне меню','Main menu',pre,True,'case-menu')}{shot('battle-titan','Дуель із Titan','Duel with Titan',pre,True,'case-battle')}</div></section>
<section class="case-facts wrap"><div><span>{bi('Моя роль','My role')}</span><strong>Solo Developer</strong></div><div><span>{bi('Формат','Format')}</span><strong>Single-player RPG</strong></div><div><span>{bi('Платформа','Platform')}</span><strong>Mobile</strong></div><div><span>{bi('Рушій','Engine')}</span><strong>Unity / C#</strong></div></section>
<section class="section wrap"><div class="section-heading"><div><p class="eyebrow">{bi('ПРО ГРУ','THE GAME')}</p><h2>{bi('Кожна дуель —<br>обмін рішеннями.', 'Every duel is<br>an exchange of decisions.')}</h2></div></div><div class="feature-grid"><article><span class="feature-number">01 / COMBAT</span><h3>{bi('Читати супротивника','Read your opponent')}</h3><p>{bi('Обирай напрямки атаки й захисту. Вирішуй, коли блокувати, коли парирувати та на що витратити сили.', 'Choose attack and defense directions. Decide when to block, when to parry, and where to spend your resources.')}</p></article><article><span class="feature-number">02 / ADAPTATION</span><h3>{bi('Змінювати звички','Change your habits')}</h3><p>{bi('Повторювані дії дають ворогу досвід. Власні рішення доводиться переглядати, а його поведінку — спостерігати.', 'Repeated actions give the opponent experience. Watch its behavior and reconsider the choices that have become predictable.')}</p></article><article><span class="feature-number">03 / YOUR BUILD</span><h3>{bi('Знаходити свій стиль','Find your own style')}</h3><p>{bi('Поєднуй зброю, атрибути, перки та здібності. Розвивай героя навколо тактики, яка цікава саме тобі.', 'Combine weapons, attributes, perks, and abilities. Build a character around the tactics you enjoy.')}</p></article></div></section>
<section id="gallery" class="section wrap"><div class="section-heading"><div><p class="eyebrow">{bi('БЕЗ СЮЖЕТНИХ СПОЙЛЕРІВ','A LOOK INSIDE')}</p><h2>{bi('Гра в кадрах','Screens from the game')}</h2></div><p class="small muted">{bi('Натисни, щоб роздивитися','Select an image to take a closer look')}</p></div><div class="game-gallery">'''
    shots=[('battle-titan','Тактична дуель','Tactical duel'),('map','Дослідження світу','World exploration'),('inventory','Спорядження','Equipment'),('dialogue','Зустрічі й діалоги','Encounters & dialogue'),('abilities','Активні здібності','Active abilities'),('perks','Пасивні перки','Passive perks')]
    for name,ua,en in shots:
        b+=f'<figure>{shot(name,ua,en,pre)}<figcaption>{bi(ua,en)}</figcaption></figure>'
    b+=f'''</div></section><section class="section wrap"><div class="guide-callout"><div><p class="eyebrow">{bi('ПУБЛІЧНА WIKI','PUBLIC GAME GUIDE')}</p><h2>{bi('Більше про механіки.<br>Без розкриття таємниць.', 'A closer look at the mechanics.<br>The mysteries stay in the game.')}</h2><p>{bi('Знайомство з дуелями, ресурсами, розвитком героя та світом Carnage Club.', 'Explore the duels, resources, character progression, and world of Carnage Club.')}</p></div>{button('wiki/ua/01-gdd.html',bi('Відкрити Wiki','Open the guide')+' →',False,'data-wiki-entry')}</div></section>
<section id="development" class="section wrap"><div class="development-layout"><div><p class="eyebrow">{bi('АВТОРСЬКА РОЗРОБКА','SOLO DEVELOPMENT')}</p><h2>{bi('Від правил дуелі<br>до ігрового світу.', 'From the rules of a duel<br>to the world around it.')}</h2></div><div><p>{bi('Я розробляю Carnage Club як цілісний проєкт: проєктую й реалізую бойові системи, адаптивних супротивників, прогресію, спорядження та взаємодії кампанії. Окрема частина роботи — інструменти, що допомагають розвивати гру.', 'I develop Carnage Club as a complete project: designing and implementing combat, adaptive opponents, progression, equipment, and campaign interactions. Development tools are another part of making the game practical to build and evolve.')}</p><div class="studio-link"><img class="studio-logo" src="../../assets/images/branding/mad-hydra.webp" width="88" height="88" alt="Mad Hydra Production" loading="lazy" decoding="async"><div><strong>Mad Hydra Production</strong><p>{bi('Новини розробки та історія створення гри','Development updates and the story behind the game')}</p>{ext(HYDRA,bi('Стежити в LinkedIn','Follow on LinkedIn'))}</div></div></div></div></section></main>'''
    document(b,'Carnage Club — Dmytro Tarasenko','A solo-developed mobile RPG with tactical turn-based duels, adaptive opponents, character builds, and a dark gothic world.','projects/carnage-club/index.html',pre,'projects')

class TextOnly(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data): self.parts.append(data)

def plain(s):
    p=TextOnly();p.feed(s);return ' '.join(' '.join(p.parts).split())

def guide():
    data=json.loads((ROOT/'content/guide.json').read_text())
    labels=data['groups']
    pages=data['pages']
    for lang in ['ua','en']:
        index=[]
        for i,page in enumerate(pages):
            title=page[lang]['title']; summary=page[lang]['summary']; body=page[lang]['body']
            # All source material is editorially curated before it reaches this renderer.
            if re.search(r'<script|on\w+\s*=|javascript:',body,re.I): raise ValueError('Unsafe public guide HTML')
            toc=[]
            counter=[0]
            def heading(m):
                counter[0]+=1; slug='section-'+str(counter[0]); text=m.group(1)
                toc.append((slug,plain(text)))
                return f'<h2 id="{slug}">{text}<a class="heading-anchor" href="#{slug}" aria-label="Link to section">#</a></h2>'
            body=re.sub(r'<h2>(.*?)</h2>',heading,body,flags=re.S)
            sidebar=''
            for group,local in labels.items():
                entries=[p for p in pages if p['group']==group]
                sidebar+=f'<div class="guide-nav-group"><h2>{local[lang]}</h2>'
                sidebar+=''.join(f'<a href="{p["slug"]}.html" {current(p["slug"] == page["slug"], "page")}>{escape(p[lang]["title"])}</a>' for p in entries)+'</div>'
            reading=max(1,math.ceil(len(plain(body).split())/180))
            other='en' if lang=='ua' else 'ua'
            previous=pages[i-1] if i else None; following=pages[i+1] if i<len(pages)-1 else None
            pager='<nav class="guide-pager" aria-label="'+('Статті' if lang=='ua' else 'Articles')+'">'
            if previous: pager+=f'<a href="{previous["slug"]}.html"><small>← {"Попередня" if lang=="ua" else "Previous"}</small><strong>{previous[lang]["title"]}</strong></a>'
            if following: pager+=f'<a href="{following["slug"]}.html"><small>{"Далі" if lang=="ua" else "Next"} →</small><strong>{following[lang]["title"]}</strong></a>'
            pager+='</nav>'
            t=''.join(f'<li><a href="#{slug}">{escape(label)}</a></li>' for slug,label in toc)
            aside=f'<aside class="article-toc" aria-label="{"На цій сторінці" if lang=="ua" else "On this page"}"><p class="eyebrow">{"НА ЦІЙ СТОРІНЦІ" if lang=="ua" else "ON THIS PAGE"}</p><ul>{t}</ul></aside>'
            b=f'''<main id="main" class="guide-wrap" data-search-index="search.json"><div class="guide-top"><a class="text-link" href="../../index.html" data-keep-lang>← Carnage Club</a><span class="guide-badge">{"Публічна Wiki" if lang=="ua" else "Public game guide"}</span></div><div class="guide-layout"><aside class="guide-sidebar"><details class="guide-menu" open><summary>{"Розділи Wiki" if lang=="ua" else "Guide contents"}<span aria-hidden="true">⌄</span></summary><div class="guide-menu-content"><label class="search-label" for="wiki-search">{"Пошук у Wiki" if lang=="ua" else "Search the guide"}</label><input id="wiki-search" type="search" placeholder="{"Наприклад, парирування" if lang=="ua" else "Try parrying"}" autocomplete="off" aria-controls="search-results"><div id="search-results" class="search-results" role="region" aria-label="{"Результати пошуку" if lang=="ua" else "Search results"}" hidden></div><p class="search-status" role="status" aria-live="polite"></p><nav class="guide-nav" aria-label="Wiki">{sidebar}</nav></div></details></aside><article class="guide-article"><p class="eyebrow">{labels[page['group']][lang]}</p><h1>{escape(title)}</h1><p class="article-summary">{escape(summary)}</p><p class="reading-time">{reading} {"хв читання" if lang=="ua" else "min read"}</p><div class="mobile-toc"><details><summary>{"На цій сторінці" if lang=="ua" else "On this page"}</summary><ul>{t}</ul></details></div><div class="article-body">{body}</div>{pager}</article>{aside}</div></main>'''
            path=f'projects/carnage-club/wiki/{lang}/{page["slug"]}.html'
            document(b,f'{title} — Carnage Club',summary,path,'../../../../','projects',lang,f'../{other}/{page["slug"]}.html',extra='<script src="../../../../assets/js/guide.js" defer></script>')
            index.append({'title':title,'summary':summary,'text':plain(body),'url':page['slug']+'.html','group':labels[page['group']][lang]})
        (ROOT/f'projects/carnage-club/wiki/{lang}/search.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')))

def redirect(path,destination):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={destination}"><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}projects/carnage-club/index.html"><title>Carnage Club</title></head><body><p><a href="{destination}">Continue to Carnage Club →</a></p></body></html>')

def main():
    home();projects();carnage();guide()
    not_found = f'''<main id="main" class="wrap"><section class="page-intro"><p class="eyebrow">404</p><h1>{bi('Ця сторінка<br>змінила адресу.', 'This page<br>has moved.')}</h1><p>{bi('Оновлені проєкти й довідник Carnage Club доступні за посиланнями нижче.', 'Find the updated portfolio and Carnage Club guide below.')}</p><div class="actions" style="margin-top:28px">{button('/index.html',bi('На головну','Home'))}{button('/projects/carnage-club/wiki/ua/01-gdd.html',bi('Wiki Carnage Club','Carnage Club guide'),True,'data-wiki-entry')}</div></section></main>'''
    document(not_found,'Page not found — Dmytro Tarasenko','Find the updated portfolio and Carnage Club game guide.','404.html','/',extra='<meta name="robots" content="noindex">')
    redirect('projects/carnage-club/carnage-club-wiki.html','wiki/ua/01-gdd.html')
    redirect('projects/carnage-club/carnage-club-gdd.html','wiki/ua/01-gdd.html')
    redirect('projects/carnage-club/carnage-club-code.html','index.html#development')
    redirect('projects/carnage-club/wiki/index.html','ua/01-gdd.html')
    urls=['index.html','projects.html','projects/carnage-club/index.html']
    urls += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'projects/carnage-club/wiki').rglob('*.html')) if p.name!='index.html']
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{p}</loc></url>' for p in urls)+'</urlset>')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
    print(f'Built {len(urls)} public pages.')

if __name__=='__main__': main()
