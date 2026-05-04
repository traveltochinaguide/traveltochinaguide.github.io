#!/usr/bin/env python3
"""Generate city pages for 6 new cities in all 8 language versions."""
import os, re

BASE = '/home/ubuntu/traveltochinaguide.github.io'
with open(f'{BASE}/xian.html', 'r') as f:
    xian_template = f.read()

CITIES = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang']
LANGS = ['en', 'zh-CN', 'ja', 'ko', 'es', 'fr', 'de', 'ru']

LANG_ATTRS = {
    'en':    {'html_lang': 'en',    'lang_key': 'en',    'hreflang': 'en'},
    'zh-CN': {'html_lang': 'zh-CN', 'lang_key': 'zh-CN', 'hreflang': 'zh-CN'},
    'ja':    {'html_lang': 'ja',    'lang_key': 'ja',    'hreflang': 'ja'},
    'ko':    {'html_lang': 'ko',    'lang_key': 'ko',    'hreflang': 'ko'},
    'es':    {'html_lang': 'es',    'lang_key': 'es',    'hreflang': 'es'},
    'fr':    {'html_lang': 'fr',    'lang_key': 'fr',    'hreflang': 'fr'},
    'de':    {'html_lang': 'de',    'lang_key': 'de',    'hreflang': 'de'},
    'ru':    {'html_lang': 'ru',    'lang_key': 'ru',    'hreflang': 'ru'},
}

CITY_DATA = {
    'chongqing': {'lat': 29.4316, 'lon': 106.9121},
    'guangzhou': {'lat': 23.1291, 'lon': 113.2644},
    'shenzhen':  {'lat': 22.5431, 'lon': 114.0579},
    'kunming':   {'lat': 25.0389, 'lon': 102.7183},
    'dali':      {'lat': 25.6065, 'lon': 100.2679},
    'lijiang':   {'lat': 26.8721, 'lon': 100.2289},
}
CANONICAL_BASE = 'https://travelchinaguide.dpdns.org'

CITY_NAMES = {
    'chongqing': {'en': 'Chongqing', 'zh-CN': '重庆', 'ja': 'Chongqing', 'ko': '충칭', 'es': 'Chongqing', 'fr': 'Chongqing', 'de': 'Chongqing', 'ru': 'Чунцин'},
    'guangzhou': {'en': 'Guangzhou', 'zh-CN': '广州', 'ja': 'Guangzhou', 'ko': '광저우', 'es': 'Cantón', 'fr': 'Canton', 'de': 'Guangzhou', 'ru': 'Гуанчжоу'},
    'shenzhen':  {'en': 'Shenzhen',  'zh-CN': '深圳', 'ja': 'Shenzhen',  'ko': '선전',  'es': 'Shenzhen', 'fr': 'Shenzhen', 'de': 'Shenzhen', 'ru': 'Шэньчжэнь'},
    'kunming':   {'en': 'Kunming',   'zh-CN': '昆明', 'ja': 'Kunming',   'ko': '쿤밍',  'es': 'Kunming', 'fr': 'Kunming', 'de': 'Kunming', 'ru': 'Куньмин'},
    'dali':      {'en': 'Dali',      'zh-CN': '大理', 'ja': 'Dali',      'ko': '다리',   'es': 'Dali', 'fr': 'Dali', 'de': 'Dali', 'ru': 'Да-ли'},
    'lijiang':   {'en': 'Lijiang',   'zh-CN': '丽江', 'ja': 'Lijiang',   'ko': '리장',   'es': 'Lijiang', 'fr': 'Lijiang', 'de': 'Lijiang', 'ru': 'Лицзян'},
}

DESCS = {
    'chongqing': {'en': 'The mountain city famous for hot pot and the merging of the Yangtze and Jialing Rivers.', 'zh-CN': '山城重庆，以火锅和两江交汇闻名。', 'ja': 'Chongqing - the mountain city famous for hot pot.', 'ko': '호탕과 양쯔강 합류점으로 유명한 산성.', 'es': 'La ciudad mountainous famosa por el hot pot y la confluencia de los rios Yangtsé y Jialing.', 'fr': 'La ville de montagne celebre pour le hot pot et la confluence du Yangtsé et de la Jialing.', 'de': 'Die Bergstadt, beruhmt fur Hot Pot und die Mundung von Yangtze und Jialing.', 'ru': 'Gorod v gorah, izvestnyj hot-pot i slijaniem Janczy i Cjalin.'},
    'guangzhou': {'en': 'The heart of Cantonese culture, cuisine, and commerce in southern China.', 'zh-CN': '岭南文化的中心，美食与商业之城。', 'ja': 'Guangzhou - the heart of Cantonese culture and cuisine.', 'ko': '광둥 문화·음식·상업의 중심지.', 'es': 'El corazon de la cultura, gastronomia y comercio cantonés.', 'fr': 'Le coeur de la culture, de la cuisine et du commerce cantonais.', 'de': 'Das Herz der kantonesischen Kultur, Kuche und Handel.', 'ru': 'Serdce kantonskoj kultury, kuhni i torgovli.'},
    'shenzhen': {'en': "China's original Special Economic Zone - a futuristic megacity built in just 40 years.", 'zh-CN': '中国首个经济特区，四十年建成的未来之城。', 'ja': "Shenzhen - China's original Special Economic Zone.", 'ko': '중국 최초의 경제특구 — 40년에 건설된 미래 도시.', 'es': 'La primera Zona Economica Especial de China - una megaciudad futurista en 40 anos.', 'fr': 'La premiere Zone Economique Speciale de Chine - une mégacité futuriste construite en 40 ans.', 'de': 'Chinas erste Sonderwirtschaftszone - eine futuristische Mega-Stadt in 40 Jahren.', 'ru': 'Pervaja osobaja jekonomicheskaja zona Kitaja - megapolis budushhego za 40 let.'},
    'kunming': {'en': 'The "Spring City" - year-round mild climate and gateway to Yunnan ethnic diversity.', 'zh-CN': '"春城"——四季如春，云南民族多元文化的门户。', 'ja': 'Kunming - the "Spring City" of China.', 'ko': '"봄의 도시" — 원난 민족 다양성의 관문.', 'es': 'La "Ciudad de la Primavera" - clima templado todo el ano y puerta a Yunnan.', 'fr': 'La "Ville du Printemps" - climat doux toute l\'annee et porte vers le Yunnan.', 'de': 'Die "Fruhlingsstadt" - ganzjahrig mildes Klima und Tor zu Yunnans Vielfalt.', 'ru': '«Gorod Vesny» - myagkij klimat kruglyj god i vrata v Junnan.'},
    'dali': {'en': 'Cangshan Mountains and Erhai Lake - the heart of Bai culture and charm.', 'zh-CN': '苍山洱海之间——白族文化的核心与魅力。', 'ja': 'Dali - Cangshan Mountains and Erhai Lake.', 'ko': '창산과얼해 호수 사이 — Bai족 문화의 핵심.', 'es': 'Montanas Cangshan y lago Erhai - el corazon de la cultura Bai.', 'fr': 'Montagnes Cangshan et lac Erhai - le coeur de la culture Bai.', 'de': 'Cangshan-Berge und Erhai-See - das Herz der Bai-Kultur.', 'ru': 'Gory Canshan i ozero Erhaj - serdce kultury baj.'},
    'lijiang': {'en': 'Ancient Naxi capital with UNESCO World Heritage status and Jade Dragon Snow Mountain backdrop.', 'zh-CN': '纳西古都，联合国世界遗产，玉龙雪山映衬下的古城。', 'ja': 'Lijiang - Ancient Naxi capital with UNESCO World Heritage status.', 'ko': '나시 고대 수도, 세계문화유산, 옥용설산 배경의 고성.', 'es': 'Antigua capital Naxi con estatus de Patrimonio de la Humanidad de la UNESCO.', 'fr': 'Ancienne capitale Naxi, site du patrimoine mondial de l\'UNESCO.', 'de': 'Alte Naxi-Hauptstadt mit UNESCO-Weltkulturerbe.', 'ru': 'Drevnjaja stolica naroda nasi, obekt Vslemirnogo nasledija JUNESKO.'},
}

LONG_DESCS = {
    'chongqing': {
        'en': '<p>Chongqing, a mountainous city in southwestern China, is famous for its fog, spicy hot pot, and dramatic nightscapes where the Yangtze and Jialing Rivers converge. Known as the "Mountain City," its terrain is unlike anywhere else in China. Buildings appear on top of buildings, and roads wind through cliffs.</p><p>Do not miss Hongya Dong, a stunning shopping complex built into a natural cave. The Ciqikou ancient street offers a glimpse into the city\'s history, while the Three Gorges Museum tells the story of the Yangtze River valley.</p>',
        'zh-CN': '<p>重庆是中国西南部的山地城市，以雾都、麻辣火锅和两江夜景闻名。重庆被称为"山城"，建筑层层叠叠，道路蜿蜒于悬崖之间，景色独特。</p><p>洪崖洞是嵌在天然洞穴中的惊人购物综合体，磁器口古镇展示了这座城市的历史，三峡博物馆讲述了长江流域的故事。</p>',
        'ja': '<p>Chongqing为中国南西部の山之城で、霧と麻辣火待、两江の夜景で有名です。洪崖洞は自然に掘られた洞穴に建てられたショッピングコンプレックスです。</p>',
        'ko': '<p>충칭은 중국 남서부의 산악 도시로 안개, 매운 훠궈, 양쯔강과 자링장강이 만나는 밤 풍경으로 유명합니다。홍야동은 자연 동굴 안에 지어진 놀라운 쇼핑콤플렉스입니다。</p>',
        'es': '<p>Chongqing, una ciudad mountainous en el southwest de China, es famosa por su niebla, hot pot picante y los dramaticos paisajes nocturnos donde confluan los rios Yangtsé y Jialing.</p>',
        'fr': '<p>Chongqing, une ville montagneuse dans le sud-ouest de la Chine, est celebre pour son brouillard, son hot pot epicé et ses paysages nocturnes spectaculaires où le Yangtsé et la Jialing confluent.</p>',
        'de': '<p>Chongqing, eine bergige Stadt im Sudwesten Chinas, ist beruhmt fur ihren Nebel, scharfen Hot Pot und dramatische Nachtlandschaften, wo sich der Yangtze und der Jialing treffen.</p>',
        'ru': '<p>Chunucin, gornyj gorod na jugozapade Kitaja, izvesten svoimi tumami, ostrym hot-pot i dramatichnymi nochnymi pejzazhami, gde Janczy i Cjalin vstrechajutsja.</p>',
    },
    'guangzhou': {
        'en': '<p>Guangzhou, the capital of Guangdong Province, is the birthplace of Cantonese culture, cuisine, and the famous "Cantonese way of life." The city blends a millennium of trading history with a hyper-modern urban core.</p><p>Visit the Canton Tower for panoramic city views, explore Shamian Island\'s colonial European architecture, or feast on dim sum in the city\'s countless teahouses.</p>',
        'zh-CN': '<p>广州是广东省省会，岭南文化、美食和"广式生活"的发源地。这座城市将千年贸易历史与现代都市核心完美融合。</p><p>登广州塔俯瞰城市全景，探索沙面岛的欧洲殖民建筑，或在众多茶楼品尝点心。</p>',
        'ja': '<p>Guangzhouは広東省の省都で、広東文化、食の発祥地です。広州塔から街の全景を眺め、汕頭島の欧州植民地建築を探検できます。</p>',
        'ko': '<p>광저우는 광둥 성의 성도로, 광둥 문화, 음식, 유명한「광둥식 삶의 방식」의 발원지입니다。광저우 타워에서 도시 전경을 감상하고, 사미엔 섬의 유럽 식민지 건축을 탐험할 수 있습니다。</p>',
        'es': '<p>Guangzhou, capital de Guangdong, es la cuna de la cultura cantonés y su famosa gastronomia。</p>',
        'fr': '<p>Guangzhou, capitale du Guangdong, est le berceau de la culture cantonaise et de sa célèbre gastronomie。</p>',
        'de': '<p>Guangzhou, die Hauptstadt der Provinz Guangdong, ist die Wiege der kantonesischen Kultur und Kuche。</p>',
        'ru': '<p>Guanchzhou, stolica provincii Guandong, javljaetsja kolybelju kantonskoj kultury i kuhni。</p>',
    },
    'shenzhen': {
        'en': '<p>Shenzhen transformed from a small fishing village in 1980 to one of China\'s largest and most prosperous cities in just four decades. As the country\'s first Special Economic Zone, it pioneered China\'s reform and opening-up policy.</p><p>Visit Window of the World for miniature landmarks from across the globe, or the Shenzhen Bay Park for waterfront promenades.</p>',
        'zh-CN': '<p>深圳从1980年的小渔村在短短四十年内崛起为中国最大、最繁荣的城市之一。作为中国第一个经济特区，它开创了中国的改革开放政策。</p><p>世界之窗汇集了全球微缩景观，深圳湾公园提供海滨漫步。</p>',
        'ja': '<p>深センは1980年の小さな漁村から40年で中国最大かつ最も繁栄した都市の一つになりました。中国最初の経済特区として、中国の改革開放政策の先触れとなりました。</p>',
        'ko': '<p>선전은 1980년 작은 어촌에서 40년 만에 중국 최대의 번영한 도시 중 하나로 발전했습니다。중국 최초의 경제특구로서 중국의 개혁개방 정책의 선구자가 되었습니다。</p>',
        'es': '<p>Shenzhen se transformó de una pequeña aldea pesquera a una de las ciudades más grandes de China en solo cuatro décadas。</p>',
        'fr': '<p>Shenzhen s\'est transformé d\'un petit village de pêcheurs à l\'une des plus grandes villes de Chine en seulement quatre décennies。</p>',
        'de': '<p>Shenzhen hat sich von einem kleinen Fischerdorf in 40 Jahren zu einer der größten Städte Chinas entwickelt。</p>',
        'ru': '<p>Shenchzhen prevratilsja iz malenkoj rybnoj derevni v 1980 godu v odin iz krupnejshih i procvetavshih gorodov Kitaja vsego za chetyre desjatiletija.</p>',
    },
    'kunming': {
        'en': '<p>Kunming, the capital of Yunnan Province, is known as the "Spring City" for its year-round spring-like climate. It is the gateway to Yunnan\'s extraordinary ethnic diversity - 24 minority groups call this province home.</p><p>The Stone Forest just outside the city features dramatic karst formations, while the Green Lake Park offers peaceful city-center relaxation.</p>',
        'zh-CN': '<p>昆明是云南省省会，因全年温和的气候被称为"春城"。它是通往云南非凡民族多元文化的门户——全省有24个少数民族。</p><p>城外的石林以壮观的喀斯特地貌著称，翠湖公园提供城市中心的宁静休闲。</p>',
        'ja': '<p>昆明は雲南省の省都で、年間を通じて春のような気候から「春之城」と呼ばれています。雲南の非凡な民族多様性への入口として、この省には24の少数民族がいます。</p>',
        'ko': '<p>쿤밍은 원난 성의 성도로 일년 내내 봄 같은 기후로「봄의 도시」로 불립니다。원난의 특별한 민족 다양성의 문으로서 이 성에는 24개의 소수민족이 있습니다。</p>',
        'es': '<p>Kunming, capital de Yunnan, es conocida como la "Ciudad de la Primavera" por su clima templado durante todo el año。</p>',
        'fr': '<p>Kunming, capitale du Yunnan, est connue comme la "Ville du Printemps" pour son climat printanier toute l\'année。</p>',
        'de': '<p>Kunming, die Hauptstadt der Provinz Yunnan, ist als "Frühlingsstadt" für ihr ganzjähriges Frühlingsklima bekannt。</p>',
        'ru': '<p>Kunmin, stolica provincii Junnan, izvestna kak "Gorod Vesny" blagodarja svoemu mjagkomu klimatu kruglyj god。</p>',
    },
    'dali': {
        'en': '<p>Dali, in northwestern Yunnan, sits between the dramatic Cangshan Mountains and the serene Erhai Lake. The ancient city of Dali was the capital of the Nanzhao Kingdom and later the Kingdom of Dali, with over 1,000 years of history.</p><p>The Three Pagodas of Dali are iconic landmarks, and cyclists flock to the Erhai Lake loop for one of China\'s most scenic rides.</p>',
        'zh-CN': '<p>大理位于云南西北部，坐落在壮丽的苍山与宁静的洱海之间。大理古城是南诏国和大理国的首都，拥有千年历史。</p><p>三塔是大理的标志性建筑，骑车环洱海是中国最风景秀丽的骑行路线之一。</p>',
        'ja': '<p>大理は雲南北西部に位置し、壮大な蒼山穏やかな洱海に囲まれています。大理古城は南詔国と大理国の首都で、千年の歴史を持っています。</p>',
        'ko': '<p>다리는 윈난 북서부에 위치하여 웅장한 창산과 평온한 얼해 호수 사이에 있습니다。고대 도시 다리는 남조국과 다리국의 수도로서 천 년 이상의 역사를 가지고 있습니다。</p>',
        'es': '<p>Dali, en el noroeste de Yunnan, se encuentra entre las dramáticas montañas Cangshan y el sereno lago Erhai。</p>',
        'fr': '<p>Dali, dans le nord-ouest du Yunnan, se situe entre les spectaculaires montagnes Cangshan et le paisible lac Erhai。</p>',
        'de': '<p>Dali liegt im Nordwesten Yunnans zwischen den dramatischen Cangshan-Bergen und dem ruhigen Erhai-See。</p>',
        'ru': '<p>Da-li raspolozhena na severo-zapade Junnani mezhdu velichestvennymi gorami Canshan i spokojnym ozerom Erhaj。</p>',
    },
    'lijiang': {
        'en': '<p>Lijiang, in northwestern Yunnan, was the capital of the Naxi Kingdom and remains one of China\'s best-preserved ancient cities. The old town\'s canal system and stone bridges create a romantic water-town atmosphere, while the Jade Dragon Snow Mountain provides a breathtaking backdrop.</p><p>The Naxi cultural show at the Impression Lijiang theater is a must-see, and the ancient Mufu (Governor\'s Office) offers a window into Naxi royal history.</p>',
        'zh-CN': '<p>丽江位于云南西北部，曾是纳西王国首都，是中国保存最完好的古城之一。老城的运河系统和石桥营造出浪漫的水镇氛围，玉龙雪山提供壮观的背景。</p><p>印象丽江剧院的纳西文化表演不容错过，古老的木府让人们一窥纳西王室历史。</p>',
        'ja': '<p>麗江は雲南北西部に位置し、ナシ王国の首都であり、中国で最も保存状態のよい古城の一つです。旧市街の運河システムと石橋はロマンチックな水郷の雰囲気を生み出し、玉龍雪山は息をのむような背景を提供します。</p>',
        'ko': '<p>리장어는 윈난 북서부에 위치한 나시 왕국의 수도로, 중국에서最も保存状态良好的古代城市 중 하나です。古い村の運河システムと石のアーチ橋がロマンチックな水辺の雰囲気を生み出します。</p>',
        'es': '<p>Lijiang, en el noroeste de Yunnan, fue la capital del Reino Naxi y sigue siendo una de las ciudades antiguas mejor conservadas de China。</p>',
        'fr': '<p>Lijiang, dans le nord-ouest du Yunnan, était la capitale du Royaume Naxi et reste l\'une des villes anciennes les mieux préservées de Chine。</p>',
        'de': '<p>Lijiang in Nordwest-Yunnan war die Hauptstadt des Naxi-Königreichs und ist eine der besterhaltenen alten Städte Chinas。</p>',
        'ru': '<p>Lichzjan na severo-zapade Junnani byl stolicej korolevstva nasi i javljaetsja odnim iz luchshe sokhranennyh drevnih gorodov Kitaja。</p>',
    },
}

def make_page(city, lang):
    tmpl = xian_template
    la = LANG_ATTRS[lang]
    city_name = CITY_NAMES[city][lang]
    city_desc = DESCS[city][lang]
    city_long_desc = LONG_DESCS[city][lang]
    lat = CITY_DATA[city]['lat']
    lon = CITY_DATA[city]['lon']
    canonical_path = (CANONICAL_BASE + '/' + la['lang_key'] + '/' + city + '.html') if lang != 'en' else (CANONICAL_BASE + '/' + city + '.html')
    page_filename = (BASE + '/' + la['lang_key'] + '/' + city + '.html') if lang != 'en' else (BASE + '/' + city + '.html')
    if lang != 'en':
        os.makedirs(BASE + '/' + la['lang_key'], exist_ok=True)
    page = tmpl
    page = re.sub(r'<html lang="en">', '<!DOCTYPE html>\n<html lang="' + la['html_lang'] + '">', page)
    page = re.sub(r'<title id="page-title">.*?</title>', '<title id="page-title">' + city_name + ' - China Tour</title>', page)
    page = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" id="meta-desc" content="' + city_desc + '">', page)
    page = page.replace('href="https://travelchinaguide.dpdns.org/xian.html"', 'href="' + canonical_path + '"')
    page = re.sub(r'<meta property="og:url"[^>]*>', '<meta property="og:url" content="' + canonical_path + '">', page)
    page = re.sub(r'<meta property="twitter:url"[^>]*>', '<meta property="twitter:url" content="' + canonical_path + '">', page)
    page = re.sub(r'<meta property="og:image"[^>]*>', '<meta property="og:image" content="' + CANONICAL_BASE + '/images/hero-' + city + '.webp">', page)
    page = re.sub(r'<meta name="twitter:image"[^>]*>', '<meta name="twitter:image" content="' + CANONICAL_BASE + '/images/hero-' + city + '.webp">', page)
    page = re.sub(r'"name": "Xi\'an",\s*"item": "https://travelchinaguide.dpdns.org/xian.html"', '"name": "' + city_name + '", "item": "' + canonical_path + '"', page)
    page = re.sub(r'"name": "Popular Cities",\s*"item": "https://travelchinaguide.dpdns.org/index.html"', '"name": "Popular Cities", "item": "' + CANONICAL_BASE + '/index.html"', page)
    hreflang_links = ''
    for lk, la2 in LANG_ATTRS.items():
        alt_path = (CANONICAL_BASE + '/' + la2['lang_key'] + '/' + city + '.html') if lk != 'en' else (CANONICAL_BASE + '/' + city + '.html')
        hreflang_links += '\n  <link rel="alternate" href="' + alt_path + '" hreflang="' + la2['hreflang'] + '">'
    page = re.sub(r'<link rel="alternate" href="https://travelchinaguide.dpddns.org/xian.html" hreflang="x-default">.*?</head>',
                  '<link rel="alternate" href="' + canonical_path + '" hreflang="x-default">' + hreflang_links + '\n  </head>', page, flags=re.DOTALL)
    page = page.replace('src="/images/hero-xian.webp"', 'src="/images/hero-' + city + '.webp"')
    page = re.sub(r'alt="Xi\'an"', 'alt="' + city_name + '"', page)
    page = re.sub(r'<h1[^>]*>Xi\'an</h1>', '<h1 id="city-name" class="text-3xl sm:text-5xl font-extrabold drop-shadow-lg leading-tight">' + city_name + '</h1>', page)
    page = page.replace('>Xi\'an</h1>', '>' + city_name + '</h1>')
    page = re.sub(r'<p id="city-sub"[^>]*>.*?</p>', '<p id="city-sub" data-lang-key="desc' + city.title() + '" class="mt-2 text-sm sm:text-base text-white/90 max-w-2xl">' + city_desc + '</p>', page, flags=re.DOTALL)
    page = re.sub(r'<div id="city-content" class="prose text-gray-700">.*?</div>', '<div id="city-content" class="prose text-gray-700">' + city_long_desc + '</div>', page, flags=re.DOTALL)
    page = page.replace('>© 2026 China Tour<', '>© 2026 China Tour — ' + city_name + '<')
    page = re.sub(r'"name": "Xi\'an"', '"name": "' + city_name + '"', page)
    page = re.sub(r'"description": "Xi\'an.*?"', '"description": "' + city_desc + '"', page)
    page = re.sub(r'"url": "https://travelchinaguide.dpdns.org/xian.html"', '"url": "' + canonical_path + '"', page)
    page = re.sub(r'"latitude": 34.3416', '"latitude": ' + str(lat), page)
    page = re.sub(r'"longitude": 108.9398', '"longitude": ' + str(lon), page)
    return page, page_filename

created = []
for city in CITIES:
    for lang in LANGS:
        page, path = make_page(city, lang)
        with open(path, 'w') as f:
            f.write(page)
        created.append(path)
print('Created', len(created), 'files')
for p in created:
    print(' ', p)