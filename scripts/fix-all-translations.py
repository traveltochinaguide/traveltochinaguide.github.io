#!/usr/bin/env python3
"""Fix broken translations in translations.js - Kunming, Guangzhou, Shenzhen, Suzhou, Opera"""
import re, subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/traveltochinaguide.github.io')
JS = ROOT / 'js' / 'translations.js'

# Translations: key -> new value (all properly escaped for JS strings)
TRANSLATIONS = {
    # Kunming -> 6 languages
    'ja.longDescKunming': '<p>昆明は雲南省の省都で、年間を通じて温和な気候（平均気温16〜18°C）から<strong>「春城」</strong>と呼ばれています。山と湖に囲まれ、雲南省の非凡な民族的多様性への文化的玄関口となっています—雲南省には中国の56民族中26民族が居住しています。</p><p>昆明は、石林の石柱から大理・麗江の古鎮まで、雲南省の自然と文化の驚異を探るための理想的な拠点です。</p><h3>見所</h3><ul><li><strong>石林（Shilin）</strong> — そびえ立つカルスト地形の世界遺産。</li><li><strong>海埂公園</strong> — 大きな湖と中国庭園がある昆明の中心緑地。</li><li><strong>雲南民族村</strong> — 文化公演を行う26の少数民族集落。</li><li><strong>官渡古鎮</strong> — 古代雲南の首都跡地にある歴史的な町。</li></ul><h3>観光情報</h3><p>昆明はLCCの利用が便利です。市内に地下鉄網が拡大中。最適な訪問時期は春と秋。昆明を基地に石林へ、または大理・麗江・シャングリラへの直通ハブとして活用できます。</p>',

    'ko.longDescKunming': '<p>쿤밍(昆明)은 윈난성(雲南省)의 성도로서 연간を通じて 온화한 기후(평균 기온 16~18도)로 인해 <strong>\"봄의 도시\"</strong>로 불립니다. 산과 호수로 둘러싸여 있으며 윈난성의 뛰어난 민족적 다양성의 문화적 관문 역할을 합니다—윈난성에는 중국 56개 민족 중 26개 민족이 거주합니다.</p><p>쿤밍은 윈난의 자연과 문화의驚異를 탐험하기에的理想적인 거점입니다. 스톤 포레스트(석임)와 대리, 리장 고대 마을까지探索할 수 있습니다.</p><h3>주요 명소</h3><ul><li><strong>스톤 포레스트(石林/Shilin)</strong> — 유네스코 세계문화유산의 카르스트 지형.</li><li><strong>하이뎅 공원(海埂公园)</strong> — 큰 호수와 중국 정원이 있는 쿤밍の中心緑地.</li><li><strong>윈난 민족촌(雲南民族村)</strong> — 문화 공연을 제공하는 26개 소수민족 마을.</li><li><strong>관두 고대 마을(官渡古鎮)</strong> — 고대 윈난 수도 터의 역사적인 마을.</li></ul><h3>실용 정보</h3><p>쿤밍은 저가 항공편利用이 편리합니다. 시내 지하철이 확대中입니다. 최적의 방문 시기는 봄과 가을입니다.</p>',

    'ru.longDescKunming': '<p>Куньмин (昆明), столица провинции Юньнань, известен как <strong>«Весенний город»</strong> благодаря мягкому климату в течение всего года (средняя температура 16–18°C). Окружённый горами и озёрами, он служит культурными воротами к исключительному этническому разнообразию Юньнани — в провинции представлено 26 из 56 этнических групп Китая.</p><p>Город является идеальной базой для изучения природных и культурных чудес Юньнани — от каменных столбов Шилинь до древних городов Дали и Лицзян.</p><h3>Достопримечательности</h3><ul><li><strong>Каменный лес (石林/Shilin)</strong> — объект Всемирного наследия ЮНЕСКО.</li><li><strong>Парк Хайгэн (海埂公园)</strong> — центральный парк Куньмина с озером.</li><li><strong>Деревня народов Юньнани</strong> — воссозданные деревни 26 этнических меньшинств.</li><li><strong>Древний город Гуаньду (官渡古鎮)</strong> — исторический город на месте древней столицы.</li></ul><h3>Полезная информация</h3><p>Куньмин хорошо обслуживается бюджетными авиакомпаниями. В городе развивается метро. Лучшее время для посещения — весна или осень.</p>',

    'fr.longDescKunming': '<p>Kunming, la capitale de la province du Yunnan, est connue comme la <strong>Ville du Printemps</strong> pour son climat doux toute l\'annee (moyenne de 16-18°C). Entouree de montagnes et de lacs, elle sert de porte d\'acces culturelle a la diversite ethnique exceptionnelle du Yunnan — 26 des 56 groupes ethniques de Chine sont representes dans la province.</p><p>La ville constitue une base ideale pour explorer les merveilles naturelles et culturelles du Yunnan, des colonnes de pierre de Shilin aux anciennes villes de Dali et Lijiang.</p><h3>Points forts</h3><ul><li><strong>Foret de Pierre (Shilin/石林)</strong> — site du patrimoine mondial de l\'UNESCO.</li><li><strong>Parc Haidian (海埂公园)</strong> — espace vert central avec un grand lac.</li><li><strong>Village des ethnies du Yunnan</strong> — reconstitutions de 26 villages minoritaires.</li><li><strong>Ville ancienne de Guandu (官渡古鎮)</strong> — ville historique au site de l\'ancienne capitale.</li></ul><h3>Informations pratiques</h3><p>Kunming est bien desservie par les compagnies low-cost. La ville dispose d\'un metro en expansion. Idealement a visiter au printemps ou en automne.</p>',

    'de.longDescKunming': '<p>Kunming, die Hauptstadt der Provinz Yunnan, ist wegen ihres ganzjahrig milden Klimas (Durchschnitt 16-18°C) als <strong>Stadt des Fruhling</strong> bekannt. Umgeben von Bergen und Seen dient sie als kulturelles Tor zur aussergewohnlichen ethnischen Vielfalt Yunnans — 26 der 56 ethnischen Gruppen Chinas sind in der Provinz vertreten.</p><p>Die Stadt ist ein idealer Ausgangspunkt für die Erkundung der natur- und Kulturwunder Yunnans — von den Steinsaulen des Steinwaldes (Shilin) bis zu den alten Städten Dali und Lijiang.</p><h3>Highlights</h3><ul><li><strong>Steinwald (Shilin/石林)</strong> — UNESCO-Weltkulturerbe mit imposanten Karstformationen.</li><li><strong>Haidian-Park (海埂公园)</strong> — zentrale Grunflache mit grossem See.</li><li><strong>Dorfer der Yunnan-Volker</strong> — Nachbildungen von 26 Minderheitendorfern.</li><li><strong>Guandu Ancient Town (官渡古鎮)</strong> — historische Stadt an der alten Hauptstadt.</li></ul><h3>Praktische Informationen</h3><p>Kunming wird von Billigfliegern gut angeflogen. Die Stadt verfugt uber ein wachsendes U-Bahn-Netz. Am besten im Fruhjahr oder Herbst besuchen.</p>',

    'es.longDescKunming': '<p>Kunming, la capital de la provincia de Yunnan, es conocida como la <strong>Ciudad de la Primavera</strong> por su clima templado durante todo el ano (promedio de 16-18°C). Rodeada de montañas y lagos, sirve como puerta de acceso cultural a la extraordinaria diversidad etnica del Yunnan — 26 de los 56 grupos etnicos de China estan representados en la provincia.</p><p>La ciudad es una base ideal para explorar las maravillas naturales y culturales del Yunnan, desde las columnas de piedra de Shilin hasta las antiguas ciudades de Dali y Lijiang.</p><h3>Destacados</h3><ul><li><strong>Bosque de Piedra (Shilin/石林)</strong> — sitio del Patrimonio Mundial de la UNESCO.</li><li><strong>Parque Haidian (海埂公园)</strong> — espacio verde central con un gran lago.</li><li><strong>Pueblo de las Etnias de Yunnan</strong> — recreaciones de 26 aldeas minoritarias.</li><li><strong>Pueblo Antiguo de Guandu (官渡古鎮)</strong> — pueblo historico en el sitio de la antigua capital.</li></ul><h3>Informacion practica</h3><p>Kunming cuenta con buenas conexiones de aerolineas de bajo costo. La ciudad tiene un sistema de metro en expansion. Mejor visitarla en primavera u otoo.</p>',

    # Guangzhou -> 6 languages
    'ja.longDescGuangzhou': '<p>広州は広東省の省都であり、古い伝統と尖端的な現代性の迷人な融合です。広東語文化の発祥地として、世界クラスのグルメ、歴史的な寺院、活気ある現代アートシーンを提供します。</p><p>広州は<strong>広東料理</strong>で国際的に有名で、アジア中で称賛されています。伝統的な茶楼で点心を楽しみ、qinghai市場で珍しい食材を探索してください。</p><h3>見所</h3><ul><li><strong>広州塔（CTFタワー）</strong> — 600mのアイコン的な電波塔。</li><li><strong>上下九步行街</strong> — 歴史的な植民地・伝統建築が並ぶ通りです。</li><li><strong>陳家祠</strong> — 美しい木彫りを備えた19世紀の壮大な氏族ホール。</li><li><strong>北京路</strong> — ガラス張りの床から古代都市の壁の層を眺められる歴史的な大通りです。</li></ul><h3>観光情報</h3><p>広州は優れた地下鉄網があります。ほとんどの観光地に英語表示があります。亜熱帯気候で一年中美湿です。春（3-5月）と秋（10-12月）が最も快適です。</p>',

    'ko.longDescGuangzhou': '<p>광저우(广州)는 광둥성의 성도로서 고대와 현대가迷人的하게 융합한 도시입니다. 광둥 문화의 발상지로서 세계적 수준의 미식, 역사적인 사원, 활기찬 현대 미술계를 제공합니다.</p><p>광저우는 <strong>광둥 요리</strong>로 국제적으로 유명하며 아시아 전역에서 칭찬받고 있습니다. 전통 찻집에서 딤섬을 맛보고칭하이 시장에서 exotic 재료를 구경하세요.</p><h3>주요 명소</h3><ul><li><strong>광저우 타워(CTF 타워)</strong> — 600m의 상징적인 전파타워.</li><li><strong>샹샤샤 보행 거리(上下九步行街)</strong> — 역사적인 식민지 및 전통 건축물.</li><li><strong>천가 사당(陈家祠)</strong> — 아름다운 목조 조각이 돋보이는 19세기氏族 홀.</li><li><strong>베이징 로드(北京路)</strong> — 유리 바닥을 통해 고대 도시 벽의 층이 보이는 역사적인 대로.</li></ul><h3>실용 정보</h3><p>광저우는 우수한 지하철 시스템이 있습니다. 대부분의 관광 명소에 영어 표지판이 있습니다. 아열대 기후로了一年중 뜨겁고 습합니다. 봄(3~5월)과 가을(10~12월)이 가장 쾌적합니다.</p>',

    'ru.longDescGuangzhou': '<p>Гуанчжоу (广州), столица провинции Гуандун, — это увлекательное сочетание древних традиций и новейшей современности. Будучи родиной гуандунской культуры, он предлагает лучшую в мире кухню, исторические храмы и яркую современную художественную сцену.</p><p>Гуанчжоу международно известен <strong>гуандунской кухней</strong> — еда города прославлена по всей Азии. Обязательно попробуйте димсам в традиционном чайном доме или прогуляйтесь по рынку Цинхай за экзотическими ингредиентами.</p><h3>Достопримечательности</h3><ul><li><strong>Гуанчжоу Тауэр (CTF Тауэр)</strong> — культовая 600-метровая телебашня.</li><li><strong>Пешеходная улица Шансяся (上下九步行街)</strong> — историческая улица с колониальной и традиционной архитектурой.</li><li><strong>Храм клана Чэнь (陈家祠)</strong> — великолепный XIX века зал клана с прекрасной деревянной резьбой.</li><li><strong>Пекинская дорога (北京路)</strong> — исторический проспект со слоями древних городских стен под стеклом.</li></ul><h3>Полезная информация</h3><p>В Гуанчжоу отличная система метро. Большинство достопримечательностей имеют английские указатели. Город субтропический — жаркий и влажный круглый год. Наиболее комфортно весной и осенью.</p>',

    'fr.longDescGuangzhou': '<p>Guangzhou (广州), la capitale de la province du Guangdong, est un fascinant melange de tradition ancienne et de modernite de pointe. Berceau de la culture cantonaise, elle offre une cuisine de classe mondiale, des temples historiques et une scene artistique contemporaine dynamique.</p><p>Guangzhou est internationalement fameuse pour la <strong>cuisine cantonaise</strong> — sa gastronomie est celebree a travers l\'Asie. Ne manquez pas de gouitter aux dim sum dans une maison de the traditionnelle.</p><h3>Points forts</h3><ul><li><strong>Canton Tower (CTF Tower)</strong> — l\'iconique tour de television de 600m.</li><li><strong>Ruepietonne Shangxiaxia (上下九步行街)</strong> — rue historique a l\'architecture coloniale et traditionnelle.</li><li><strong>Temple ancestral du clan Chen (陈家祠)</strong> — magnifique salle clanique du XIXe siecle.</li><li><strong>Rue Beijing (北京路)</strong> — avenue historique avec les couches de murs anciens visibles sous le verre.</li></ul><h3>Informations pratiques</h3><p>Guangzhou dispose d\'un excellent metro. La plupart des attractions ont une signaletique en anglais. La ville est subtropicale. Le printemps et l\'automne sont les periodes les plus confortables.</p>',

    'de.longDescGuangzhou': '<p>Guangzhou (广州), die Hauptstadt der Provinz Guangdong, ist eine faszinierende Mischung aus alter Tradition und modernster Gegenwart. Als Wiege der kantonesischen Kultur bietet sie erstklassige Kueche, historische Tempel und eine lebendige zeitgenossische Kunstszene.</p><p>Guangzhou ist international bekannt fuer die <strong>kantonesische Kueche</strong> — das Essen der Stadt wird in ganz Asien gefeiert. Verpassen Sie nicht, Dim Sum in einem traditionellen Teehaus zu probieren.</p><h3>Highlights</h3><ul><li><strong>Canton Tower (CTF Tower)</strong> — das 600m hohe Wahrzeichen mit spektakulaerer Aussichtsplattform.</li><li><strong>Shangxiaxia Fussgaengerstrasse (上下九步行街)</strong> — historische Strasse mit kolonialer und traditioneller Architektur.</li><li><strong>Chen-Clan-Ahnentempel (陈家祠)</strong> — praechtige Clan-Halle aus dem 19. Jahrhundert.</li><li><strong>Peking-Strasse (北京路)</strong> — historische Allee mit sichtbaren Schichten antiker Stadtmauern unter Glas.</li></ul><h3>Praktische Informationen</h3><p>Guangzhou hat ein ausgezeichnetes U-Bahn-System. Die meisten Sehenswuerdigkeiten haben englische Beschilderung. Am angenehmsten im Fruhjahr und Herbst.</p>',

    'es.longDescGuangzhou': '<p>Guangzhou (广州), la capital de la provincia de Guangdong, es una fascinante mezcla de tradicion antigua y modernidad de vanguardia. Como cuna de la cultura cantonesa, ofrece cocina de clase mundial, templos historicos y una vibrante escena de arte contemporáneo.</p><p>Guangzhou es internacionalmente famosa por la <strong>cocina cantonesa</strong> — la gastronomia de la ciudad es celebrada en toda Asia. No te pierdas probar dim sum en una casa de te tradicional.</p><h3>Destacados</h3><ul><li><strong>Canton Tower (CTF Tower)</strong> — la iconica torre de television de 600m.</li><li><strong>Calle Peatonal Shangxiaxia (上下九步行街)</strong> — calle historica con arquitectura colonial y tradicional.</li><li><strong>Sala Ancestral del Clan Chen (陈家祠)</strong> — magnifica sala clanica del siglo XIX.</li><li><strong>Avenida Beijing (北京路)</strong> — avenida historica con capas de murallas antiguas visibles a traves del suelo de vidrio.</li></ul><h3>Informacion practica</h3><p>Guangzhou tiene un excelente sistema de metro. La mayoria de las atracciones tienen senalizacion en ingles. La primavera y el otono son mas comodos.</p>',

    # Shenzhen -> 6 languages
    'ja.longDescShenzhen': '<p>深センは世界で最も著しい都市変容の一つです—1980年に3万人だった漁村から今天的1700万人都市へと発展しました。中国初の経済特区として改革開放の先頭に立ち、今日では地球上で最も未来的なスカイライン夸っています。</p><p>深センはテック愛好家の天国で、Huawei、Tencent、BYDなどの大手企業が拠点を置いています。ビジネス地区以外にも、美しい公園、文化博物館、優れた水族館があります。</p><h3>見所</h3><ul><li><strong>ワールドウィンドウ（世界之窗）</strong> — 世界の名所miniature再現。</li><li><strong>深セン博物館</strong> — 市の非凡な変容に関する優れた展示。</li><li><strong>大芬油画村</strong> — 世界最大の油彩複製生産地。</li><li><strong>テンセント本社（Mango Valley）</strong> — ザー・ハディドが設計した stunning キャンパス。</li></ul><h3>観光情報</h3><p>深センの地下鉄は非常に発達しています。英語の表示は他の中国都市より優れています。香港との組み合わせでの週末旅行に最佳です。</p>',

    'ko.longDescShenzhen': '<p>선전(深圳)은 세계에서最も눈부신 도시 변신입니다—1980년에 3만 명의 어촌이었다 곳이 오늘날 1,700만 명의 대도시로発展했습니다. 중국 최초의 경제특구로서 개혁개방을 선도했으며 오늘날 지구상에서最も미래적인 스카이라인을誇っています.</p><p>선전은 테크愛好자의 천국으로 화웨이, 텐센트, BYD 등의 주요 기업이 본부를 두고 있습니다.</p><h3>주요 명소</h3><ul><li><strong>월드 윈도우(世界之窗)</strong> — 세계 명소의 미니어처.</li><li><strong>선전 박물관(深圳博物馆)</strong> — 도시의 extraordinary한 변신 전시.</li><li><strong>다펜 유화촌(大芬油画村)</strong> — 세계 최대의 유화 복제 생산지.</li><li><strong>텐센트 본사(Mango Valley)</strong> — 자하 하디드가設計한 stunning한 캠퍼스.</li></ul><h3>실용 정보</h3><p>선전은 지하철이 매우 잘 되어 있습니다. 홍콩과 함께하는 주말 여행에 최적입니다.</p>',

    'ru.longDescShenzhen': '<p>Шэньчжэнь (深圳) — одна из самых remarkableых городских трансформаций в мире: из рыбацкой деревни с 30 000 жителей в 1980 году до мегаполиса с 17 миллионами сегодня. Будучи первой в Китае специальной экономической зоной, он стал пионером реформ и открытости, и сегодня может похвастаться одним из самых футуристических силуэтов на Земле.</p><p>Шэньчжэнь — рай для любителей технологий, здесь расположены Huawei, Tencent и BYD.</p><h3>Достопримечательности</h3><ul><li><strong>Окно в мир (世界之窗)</strong> — миниатюрные воссоздания мировых достопримечательностей.</li><li><strong>Музей Шэньчжэня (深圳博物馆)</strong> — отличные экспозиции о трансформации города.</li><li><strong>Деревня масляной живописи Дафэнь (大芬油画村)</strong> — крупнейший производитель репродукций.</li><li><strong>Штаб-квартира Tencent (Mango Valley)</strong> — потрясающий кампус Захи Хадид.</li></ul><h3>Полезная информация</h3><p>Метро в Шэньчжэне очень развито. Лучше всего посетить как комбинированную поездку с Гонконгом на выходные.</p>',

    'fr.longDescShenzhen': '<p>Shenzhen (深圳) est l\'une des transformations urbaines les plus remarquables au monde — d\'un village de pecheurs de 30 000 habitants en 1980 a une megalopole de 17 millions d\'habitants aujourd\'hui. Zone economique speciale pionniere de la Chine, elle a ouvert la voie aux reformes et a l\'ouverture.</p><p>Shenzhen est le paradis des amateurs de tech, abritant Huawei, Tencent et BYD.</p><h3>Points forts</h3><ul><li><strong>Fenetre sur le monde (世界之窗)</strong> — reproductions miniatures de monuments mondiaux.</li><li><strong>Musee de Shenzhen (深圳博物馆)</strong> — excellentes expositions sur la transformation de la ville.</li><li><strong>Village de peinture a l\'huile de Dafen (大芬油画村)</strong> — le plus grand producteur de reproductions.</li><li><strong>QG Tencent (Mango Valley)</strong> — un campus epoustouflant conçu par Zaha Hadid.</li></ul><h3>Informations pratiques</h3><p>Shenzhen est extremely bien desservie par le metro. Ideal pour un week-end combine avec Hong Kong.</p>',

    'de.longDescShenzhen': '<p>Shenzhen (深圳) ist eine der bemerkenswertesten städtischen Verwandlungen der Welt — von einem Fischerdorf mit 30.000 Einwohnern im Jahr 1980 zu einer Metropole mit 17 Millionen heute. Als Chinas erste Sonderwirtschaftszone ebnete sie den Weg für Reformen und Öffnung.</p><p>Shenzhen ist ein Paradies für Technikliebhaber, Heimat von Huawei, Tencent und BYD.</p><h3>Highlights</h3><ul><li><strong>Fenster zur Welt (世界之窗)</strong> — maßstabsgetreue Nachbildungen weltberühmter Wahrzeichen.</li><li><strong>Museum Shenzhen (深圳博物馆)</strong> — hervorragende Ausstellungen zur Transformation der Stadt.</li><li><strong>Dafen Ölgemälde-Dorf (大芬油画村)</strong> — der größte Produzent von Ölgemälde-Nachbildungen.</li><li><strong>Tencent-Hauptsitz (Mango Valley)</strong> — ein atemberaubender Campus von Zaha Hadid.</li></ul><h3>Praktische Informationen</h3><p>Shenzhen ist extrem gut an das U-Bahn-Netz angebunden. Am besten als Wochenendausflug in Kombination mit Hongkong.</p>',

    'es.longDescShenzhen': '<p>Shenzhen (深圳) es una de las transformaciones urbanas mas extraordinarias del mundo — de una aldea de pescadores con 30.000 habitantes en 1980 a una metropoli de 17 millones hoy. Como la primera Zona Economica Especial de China, pionera en reformas y apertura.</p><p>Shenzhen es el paraiso de los amantes de la tecnologia, hogar de Huawei, Tencent y BYD.</p><h3>Destacados</h3><ul><li><strong>Ventana al Mundo (世界之窗)</strong> — miniaturas de monumentos mundiales.</li><li><strong>Museo de Shenzhen (深圳博物馆)</strong> — excelentes exposiciones sobre la transformacion de la ciudad.</li><li><strong>Pueblo de Pintura al Oleo de Dafen (大芬油画村)</strong> — el mayor productor de reproducciones.</li><li><strong>Sede de Tencent (Mango Valley)</strong> — un campus impresionante disenado por Zaha Hadid.</li></ul><h3>Informacion practica</h3><p>Shenzhen esta extremadamente bien comunicada por metro. Lo mejor como viaje de fin de semana combinado con Hong Kong.</p>',

    # Suzhou Korean
    'ko.longDescSuzhou': '<p>쑤저우(蘇州)은 장쑤성에 위치한 유네스코 세계문화유산 도시로 고전 정원, 견직물 생산, 운하 네트워크로 유명합니다. 종종 <strong>동방의 베네치아</strong>로 불리며 중국의 현대적 대도시와는 달리 평화로운 대비를 제공합니다.</p><p>겸허한 관리의 정원을 탐방하고, 역사적인 평장로 운하를 따라 걸으며, 쑤저우 견직물 박물관을 방문하세요. 쑤저우의 고전 정원—겸허한 관리의 정원과 영구정원을 포함—은 중국에서 가장 유명한 정원들입니다.</p><p>호랑이 언덕 파고, 고대 영구정원, 활기찬 평장로 역사 지구를 놓치지 마세요.</p>',

    # Opera Korean/Russian/German/Spanish
    'ko.longDescOpera': '<p><strong>중국 오페라</strong> (戏曲, xìqǔ)는 음악, 성악, 묘사, 춤, 곡예를 결합한 종합 공연 예술입니다. <strong>경극</strong> (京剧, jīngjù)이 가장 유명한 형식입니다.</p><h3>경극 (京剧)</h3><p>경극은 18세기 후반에 앙후이 오페라(徽剧)와 후베이 오페라(汉剧)의 결합으로誕生했습니다. 주요 특징:</p><ul><li><strong>노래</strong> — 소규모 앙상블 반주를 동반한 다양한 패턴의 선율적 아리아.</li><li><strong>대화와 낭송</strong> — 베이징 방언으로 전달.</li><li><strong>무술</strong> — 곡예적 싸움과 동작.</li><li><strong>춤</strong> — 상징적 제스처와 동작 시퀀스.</li></ul><h3>의상과 분장</h3><p>중국 오페라 의상(戏服)은 매우 정교합니다. 분장(脸谱)은 상징적입니다 — 각 색상은 등장인물의 성격을 나타냅니다: 빨간색은 충성, 검은색은 정의, 흰색은 배신, 금색은 신성한 존재.</p><h3>지역 양식</h3><p>경극 외에 주요 지역 양식으로는 광둥 오페라(粤剧), Kunqu(昆曲) — 원나라 시대遡る最古の公演形式の一つ — 등이 있습니다.</p>',

    'ru.longDescOpera': '<p><strong>Китайская опера</strong> (戏曲, xìqǔ) — это синтетический вид сценического искусства, объединяющий музыку, вокальное исполнение, пантомиму, танец и акробатику. Наиболее известной формой является <strong>Пекинская опера</strong> (京剧, jīngjù).</p><h3>Пекинская опера (京剧)</h3><p>Пекинская опера возникла в конце XVIII века, объединив элементы Аньхойской оперы (徽剧) и Хубэйской оперы (汉剧). Её особенности:</p><ul><li><strong>Пение</strong> — мелодичные арии в различных ритмических рисунках в сопровождении небольшого ансамбля.</li><li><strong>Диалог и декламация</strong> — исполняемые на пекинском диалекте.</li><li><strong>Боевые искусства</strong> — акробатические бои и движения.</li><li><strong>Танец</strong> — символические жесты и последовательности движений.</li></ul><h3>Костюмы и грим</h3><p>Костюмы китайской оперы (戏服) отличаются необычайной elaboration. Грим (脸谱) является символом — каждый цвет передаёт характер персонажа: красный — верность, чёрный — праведность, белый — коварство, золотой — божественные существа.</p><h3>Региональные стили</h3><p>Помимо Пекинской оперы, существуют крупные regionalные формы, включая Кантонскую оперу (粤剧), Куньцюй (昆曲) — одну из старейших сохранившихся форм, датируемую династией Юань, и многие другие.</p>',

    'de.longDescOpera': '<p><strong>Die chinesische Oper</strong> (戏曲, xìqǔ) ist eine umfassende darstellende Kunstform, die Musik, Gesang, Pantomime, Tanz und Akrobatik vereint. Die Peking-Oper (京剧, jīngjù) ist die bekannteste Form.</p><h3>Peking-Oper (京剧)</h3><p>Die Peking-Oper entstand im späten 18. Jahrhundert aus einer Verbindung der Anhui-Oper (徽剧) und der Hubei-Oper (汉剧). Ihre Merkmale sind:</p><ul><li><strong>Gesang</strong> — melodische Arien in verschiedenen Mustern, begleitet von einem kleinen Ensemble.</li><li><strong>Dialog und Rezitation</strong> — vorgetragen im Peking-Dialekt.</li><li><strong>Kampfkunst</strong> — akrobatische Kämpfe und Bewegungen.</li><li><strong>Tanz</strong> — symbolische Gesten und Bewegungabläufe.</li></ul><h3>Kostüme und Masken</h3><p>Die Kostüme der chinesischen Oper (戏服) sind äußerst aufwendig. Die Gesichtsbemalung (脸谱) ist ikonisch — jede Farbe vermittelt den Charakter der Figur: Rot für Loyalität, Schwarz für Rechtschaffenheit, Weiß für Verrat, Gold für göttliche Wesen.</p><h3>Regionale Stile</h3><p>Neben der Peking-Oper gibt es weitere bedeutende regionale Formen wie die Kanton-Oper (粤剧), Kunqu (昆曲) — eine der ältesten erhaltenen Formen aus der Yuan-Dynastie — und viele andere.</p>',

    'es.longDescOpera': '<p><strong>La opera china</strong> (戏曲, xìqǔ) es una forma de arte scenico integral que combina musica, interpretacion vocal, mimo, danza y acrobacia. La <strong>Opera de Pekin</strong> (京剧, jingju) es la forma mas celebre.</p><h3>Opera de Pekin (京剧)</h3><p>La Opera de Pekin surgio a finales del siglo XVIII, combinando la opera de Anhui (徽剧) y la opera de Hubei (汉剧). Sus caracteristicas incluyen:</p><ul><li><strong>Canto</strong> — Arias melodicas en varios patrones, acompanadas por un pequeno conjunto.</li><li><strong>Dialogo y recitacion</strong> — entregados en dialecto de Pekin.</li><li><strong>Artes marciales</strong> — luchas acrobaticas y movimiento.</li><li><strong>Danza</strong> — gestos simbolicos y secuencias de movimiento.</li></ul><h3>Vestuario y maquillaje</h3><p>Los disfraces de la opera china (戏服) son muy elaborados. La <strong>pintura facial</strong> (脸谱) es iconica — cada color transmite la personalidad del personaje: rojo para la lealtad, negro para la rectitud, blanco para la traicion, oro para figuras divinas.</p><h3>Estilos regionales</h3><p>Mas alla de la Opera de Pekin, las principales formas regionales incluyen la <strong>Opera Cantonesa</strong> (粤剧), el <strong>Kunqu</strong> (昆曲) — una de las formas mas antiguas que se conservan, que data de la dinastia Yuan — y muchas otras.</p>',
}

print(f"Total translations to apply: {len(TRANSLATIONS)}")

# Read translations.js
js = JS.read_text(encoding='utf-8')

applied = 0
for key, new_val in TRANSLATIONS.items():
    lang, js_key = key.split('.', 1)
    
    # Find the language section
    lang_pat = rf'"{lang}": \{{'
    m_lang = re.search(lang_pat, js)
    if not m_lang:
        print(f"WARNING: no {lang} section found")
        continue
    
    # Find the key within that section
    # Key pattern: "js_key": "value"
    # The value may contain HTML and escaped quotes
    key_pat = rf'("{re.escape(js_key)}": ")'
    m_key = re.search(key_pat, js)
    if not m_key:
        print(f"WARNING: {key} not found")
        continue
    
    # Find where the value starts
    val_start = m_key.end()
    
    # Parse the JS string to find its end
    i = val_start
    string_char = '"'
    escaped = False
    while i < len(js):
        c = js[i]
        if escaped:
            escaped = False
        elif c == '\\':
            escaped = True
        elif c == '"':
            # Check if this is the end of the string (followed by comma or end of section)
            next_chars = js[i+1:i+3].lstrip()
            if next_chars.startswith(',') or next_chars.startswith('}') or next_chars == '':
                break
        i += 1
    val_end = i  # position of closing quote
    
    old_val = js[val_start:val_end]
    
    # Replace
    js = js[:val_start] + new_val + js[val_end:]
    applied += 1

print(f"Applied {applied} patches")

# Write
JS.write_text(js, encoding='utf-8')
print(f"Wrote {JS}")

# Syntax check
r = subprocess.run(['node', '--check', str(JS)], capture_output=True, text=True)
if r.returncode == 0:
    print("Syntax check: PASSED")
else:
    print(f"Syntax check FAILED: {r.stderr[:200]}")
    exit(1)

print("DONE")