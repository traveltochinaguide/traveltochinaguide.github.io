#!/usr/bin/env python3
"""Fix longDesc translations - uses js_escape approach."""

import re

FILE = 'js/translations.js'

def js_escape(s):
    """Escape a string for use as a JS double-quoted string literal."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

# Read file
with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find language section boundaries
LANG_STARTS = {}
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == "'ja': {":
        LANG_STARTS['ja'] = i
    elif stripped == "'ko': {":
        LANG_STARTS['ko'] = i
    elif stripped == "'ru': {":
        LANG_STARTS['ru'] = i
    elif stripped == "'fr': {":
        LANG_STARTS['fr'] = i
    elif stripped == "'de': {":
        LANG_STARTS['de'] = i
    elif stripped == "'es': {":
        LANG_STARTS['es'] = i

lang_order = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']
LANG_RANGES = {}
for i, lang in enumerate(lang_order):
    if lang in LANG_STARTS:
        start = LANG_STARTS[lang]
        if i + 1 < len(lang_order) and lang_order[i + 1] in LANG_STARTS:
            end = LANG_STARTS[lang_order[i + 1]]
        else:
            end = len(lines)
        LANG_RANGES[lang] = (start, end)

# JA translations - RAW text (will be JS-escaped when injected)
JA_LONGDESC = {
    'Beijing': '''<p>北京（ペキン）は中華人民共和国の首都であり、深い歴史と文化的重要性を持つ都市です。長い歴史の中で権力の中枢として機能し、その壮大な建築にもそれが表れています。</p><p>旧皇居である紫禁城の広大な複合施設を探索し、歴史的な<strong>万里の長城</strong>を歩き、天壇を見学してください。现代の北京はまた芸術、グルメ、商业の中心でもあり、古いものと新しいものの活気ある融合を提供しています。</p><h3 id="great-wall-tour" class="text-xl font-semibold mt-6 mb-2">北京市内の万里の長城へのおすすめ日帰りツアー ― 慕田峪と八達嶺</h3><p><strong>北京的万里の長城tour</strong>は，北京市街地从発の最もpopularな日帰り旅です。typicalな選択肢にはプライベート transfers、共有シャトル버스、ガイド付き excursionsがあり、<strong>慕田峪</strong>（勾配が緩やかで整備された區間）または<strong>八達嶺</strong>（アクセス容易で施設が整備されている）へ向かいます。tourは半日から一日範囲で、ケーブルカーまたはトボガンのオプションを含むことが多いです。</p><p><strong>所需時間：</strong>4–6時間（目的地と交通手段による）。<strong>予約方法：</strong>地元のtourオペレーター、信頼できる予約プラットフォーム、またはホテルのコンシェルジュ経由で見つけることができます。静かな体験には平日目に慕田峪を選び、classicな体験には朝早く八達岭を選びましょう。</p><figure class="mt-4"> <img src="/images/attr-great-wall-detail.jpg" alt="北京的万里の長城ツアー ― 慕田峪區間" width="1200" height="675" class="w-full h-auto rounded" loading="lazy"> <figcaption class="text-sm text-gray-500 mt-2">北京的万里の長城ツアー：慕田峪區間 ― 家族連れや写真家に推奨。</figcaption></figure><h3 id="798-art-zone" class="text-xl font-semibold mt-6 mb-2">798芸術区（大山子）</h3><p><strong>798芸術区</strong>（大山子芸術区）は、北京の現代アートを楽しむことができる活気あるエリアです。独特的なバウhaus建築樣式を持つ廃軍工場を活用しており、ギャラリー、アトリエ、ブティック、カフェが迷路のように広がっています。現代アート好きには在北京のクリエイティブシーンを垣間見るために must-visit です。3–4時間かけて探索することをお勧めします。</p><figure class="mt-4"> <img src="/images/attr-798-art.jpg" alt="798芸術区ギャラリー" width="1200" height="675" class="w-full h-auto rounded" loading="lazy"> <figcaption class="text-sm text-gray-500 mt-2">北京798芸術区のギャラリー。</figcaption></figure><h3 class="text-xl font-semibold mt-6 mb-2">アクセス方法</h3><p><strong>航空：</strong>北京首都国際空港（PEK）と北京大興国際空港（PKX）が国際便を運航しています。空港からは空港快線を利用するかタクシーまたは配車アプリ（ディディ）を利用。</p><p><strong>鉄道：</strong>北京には複数の駅（北京南駅、北京西駅、北京駅）があり、中国全土からの高速鉄道が接続しています。</p><h3 class="text-xl font-semibold mt-6 mb-2">最佳訪問時期</h3><p>春（4–5月）と秋（9–10月）は天候が舒适で空も澄んでいます。冬は非常に寒くなることがあり、夏は暑く湿気が多くなります。</p><h3 class="text-xl font-semibold mt-6 mb-2">市内交通</h3><ul><li><strong>地下鉄：</strong>広範囲に走るネットワークです。交通カードまたは「北京一卡通」を利用。</li><li><strong>配車アプリ/タクシー：</strong>配車アプリと路上での捕車が利用可能。</li><li><strong>歩き/自転車：</strong>故宮、天壇公園、南鑼鼓巷は歩きで探索するのに最佳です。</li></ul><h3 class="text-xl font-semibold mt-6 mb-2">おすすめコース</h3><p><strong>1日コース：</strong>故宮 → 天安門広場 → 天壇 → 夕方の胡同歩き。</p><p><strong>3日コース：</strong>D1：故宮 + 天安門 +王府井；D2：慕田峪长城日帰り；D3：颐和園 + 天壇 + 什刹海胡同。</p><h3 class="text-xl font-semibold mt-6 mb-2">实用テクニック</h3><ul><li>現金とモバイル決済：アリペイ/微信支付が広く使用されています。大きなホテルや景区ではカードが使える場合も。</li><li>ビザ：出発前に大使館の規則を確認してください。</li><li>空气质量：空気品質指数（AQI）を確認し、空気が澄んでいる日に戶外活動を計画してください。</li><li>緊急電話：警察110、救急車120、火災119。</li><li>言語：主要な景区では英語表示がありますが、簡単な中国語フレーズを學ぶか翻訳アプリを使用することをお勧めします。</li></ul>''',

    'Shanghai': '''<p>上海はグローバルな金融ハブであり、超高層ビルが立ち並ぶ未来派のスカイラインで知られています。上海タワーや東方明珠電視塔がその象徴です。</p><p>外灘沿いに歩けば植民地時代の建築様式を眺めることができ、フランス租界地区のアートギャラリーやブティック探索もおすすめです。豫園では традиционных中国文化を感じることができます。上海は中国高速成長を象徴する都市で、訪問する価値があります。</p><h3>アクセス</h3><p><strong>航空：</strong>上海虹橋国際空港（SHA）と上海浦東国際空港（PVG）の2つの国際空港があります。地下鉄、タクシー、バスで市中心部へ向かえます。</p><h3>おすすめ観光コース</h3><p><strong>1日：</strong>外灘 → 豫園 → フランス租界地区</p><p><strong>2日：</strong>上海タワー → 浦東 → 迪士尼楽園</p>''',

    'Xian': '''<p>西安は中国最古の都市の一つであり、シルクロードの東の終点です。最も有名な場所は秦皇帝陵の兵馬俑で、始皇帝の軍隊を再現した数千体の陶俑です。</p><p>街を囲む保存された城壁では、自転市で巡ると素晴らしい景色が楽しめます。回族小吃街も見逃せません。</p><h3>見どころ</h3><ul><li>兵馬俑坑</li><li>西安城壁</li><li>大雁塔</li><li>回民の小吃街</li></ul>''',

    'Guilin': '''<p>桂林の風景は中国の古典絵画そのものです。広西チワン族自治区南部に位置し、幻想的なカルスト地形は世界的に有名です。</p><p>最も良い方法は漓江を船で下りながら、石灰岩の峰と竹林、穏やかな村を眺めることです。桂林の山、水、洞物が融为一体した美景をお楽しみください。芦笛洞窟も訪れる価値があります。</p>''',

    'Zhangjiajie': '''<p>张家界は、国連教育科学文化機関から国立公園に指定された美しい石英砂岩の柱状地形ことで有名です。登山や写真愛好家に最適な幻想的な景色が広がっています。天門山のガラス張りの崖、袁汁界好此山に行く価値があります。</p><h3>見どころ</h3><ul><li>张家界国家森林公園</li><li>天門山</li><li>ガラス橋</li></ul>''',

    'Jiuzhaigou': '''<p>九寨溝は四川省に位置し、鮮やかなターコイズブルーの湖、段状の滝、穏やかな高山 Valley で知られています。摄影师の天国と言える場所です。</p><h3>見どころ</h3><ul><li>五彩池</li><li>諾日朗滝</li><li>珍珠灘</li><li>熊猫海</li></ul>''',

    'Yangtze': '''<p>長江は中国最長の川で、ドラマチックな三峡と魅力的な河 cruise が存在します。重慶から宜昌までの複数日の cruise では、沿岸のTownや歴史的な史跡を訪れることができます。三峡の美しい景色をお楽しみください。</p><h3>見どころ</h3><ul><li>三峡</li><li>張飛廟</li><li>石宝寨</li><li>宜昌</li></ul>''',

    'Iching': '''<p><strong>易経</strong>（いけきょう、易経とも書く）は中国最古の古典の一つであり、変化の書と呼ばれています。64の六爻で構成され、宇宙論、哲学、占術が融合した思想です。</p><h3>易経の特徴</h3><p>易経は数千年をかけて発展し、各六爻は壊れたまたは壊れていない6本の線から構成されます。伝統的な注解は翼と呼ばれ、学者や賢者によって使用されてきました。</p><h3>易経の使い方</h3><p>コインまたは筮竹を使用して六爻を生成し、それを解釈する方法があります。</p><h3>易経を読む理由</h3><ul><li><strong>哲学的な洞察：</strong>変化と意思決定のための枠組みを提供します。</li><li><strong>文化的文脈：</strong>中国の歴史と言語の理解を深めます。</li></ul>''',
}

# KO translations - RAW text (will be JS-escaped when injected)
KO_LONGDESC = {
    'Beijing': '''<p>베이징（北京)은 중화인민공화국의 수도로, 방대한 역사적 문화적 중요성을 가진 도시입니다. 이 도시는 국가 역사 대부분 Throughoutを通じて 권력의 중심지였으며, 그 사실은 웅장한 건축물에 드러납니다.</p><p>폐왕정(Forbidden City)의 광대한 복합시설를 탐험하고, 역사적인 <strong>만리장성</strong>을 걸으며, 태庙(Temple of Heaven)을 방문하세요. 현대 베이징은 또한 예술, 미식, 상업의 중심지이며, 오래된 것과 새로운 것의 역동적인 융합을 제공합니다.</p><h3 id="great-wall-tour" class="text-xl font-semibold mt-6 mb-2">베이징 만리장성 데이투어 ― 무톈위우(慕田峪)와 바빙링(八达岭)</h3><p><strong>베이징 만리장성 투어</strong>은 도시에서 가장 인기 있는 당일 여행입니다. 일반적인 옵션으로는 개인 차량, 공유 셔틀버스, 가이드가 동반하는 excursion이 있으며, <strong>무톈위우</strong>(완만한 경사와 보수된 구간) 또는 <strong>바빙링</strong>(손쉬운 접근과 편의시설)을 선택할 수 있습니다. 반나절에서 종일 옵션이 있고, 케이블카 또는 토보간 옵션이 포함되는 경우가 많습니다.</p><p><strong>소요 시간:</strong> 목적지와 교통 수단에 따라 4–6시간. <strong>예약 방법:</strong> 현지tour 운영자, 신뢰할 수 있는 예약 플랫폼 또는 호텔 컨시어지에서 예약할 수 있습니다. 한적한 경험을 원하면 평일에 무톈위우를, 클래식한 경험을 원하면 아침 일찍 바빙링을 선택하세요.</p><figure class="mt-4"> <img src="/images/attr-great-wall-detail.jpg" alt="베이징 만리장성 투어 – 무톈위우 구간" width="1200" height="675" class="w-full h-auto rounded" loading="lazy"> <figcaption class="text-sm text-gray-500 mt-2">베이징 만리장성 투어: 무톈위우 구간 – 가족 및 사진작가에게 추천.</figcaption></figure><h3 id="798-art-zone" class="text-xl font-semibold mt-6 mb-2">798 예술지구 (다샨즈)</h3><p><strong>798 예술지구</strong>(다샨즈 예술지구)는 베이징 현대 예술의 활기찬 허브입니다. 독특한 바우하우스 양식의 폐군 공장遗迹에 걸쳐 있으며, 갤러리, 아틀리에, 부티크, 카페가 미로처럼 펼쳐져 있습니다. 현대 미술 애호가라면 베이징의 창작 현장을 엿볼 수 있는 필수 방문지입니다. 3–4시간을 할애하여 탐험하시기 바랍니다.</p><figure class="mt-4"> <img src="/images/attr-798-art.jpg" alt="798 예술지구 갤러리" width="1200" height="675" class="w-full h-auto rounded" loading="lazy"> <figcaption class="text-sm text-gray-500 mt-2">베이징 798 예술지구의 갤러리.</figcaption></figure><h3 class="text-xl font-semibold mt-6 mb-2">到这里的方法</h3><p><strong>항공:</strong> 베이징 수도국제공항(PEK)과 베이징 다싱국제공항(PKX)이 국제편을 운항합니다. 공항에서 공항 특급열차, 택시 또는 디디(호출식 택시)를 이용하세요.</p><p><strong>기차:</strong> 베이징에는 여러 역(베이징 남역, 베이징 서역, 베이징 역)이 있어 중국 전역에서 고속철도가 연결됩니다.</p><h3 class="text-xl font-semibold mt-6 mb-2">최적の 방문 시기</h3><p>봄(4–5월)과 가을(9–10월)은天候이舒适하고 하늘이 맑습니다. 겨울은 매우 추울 수 있고, 여는 덥고 습합니다.</p><h3 class="text-xl font-semibold mt-6 mb-2">市内 교통</h3><ul><li><strong>지하철:</strong> 광범위하게走る 네트워크입니다。交通 카드 또는 «베이징 일카드»를 利用.</li><li><strong>택시/디디:</strong> 어디서나 利用可能.</li><li><strong>도보/자전거:</strong> 폐왕정, 천坛, 난뤄구샹は 도보로 탐험하기最佳.</li></ul><h3 class="text-xl font-semibold mt-6 mb-2">추천 일정</h3><p><strong>1일:</strong> 폐왕정 → 천안문 광장 → 천坛 → 저녁 후통투어.</p><p><strong>3일:</strong> D1: 폐왕정 + 천안문 + 왕푸징; D2: 무톈위우 만리장성当日tour; D3: 이화원 + 천坛 + 스샤하이용 후통.</p><h3 class="text-xl font-semibold mt-6 mb-2">실用적인 팁</h3><ul><li>현금 및 모바일 결제: 알리페이/위챗페이가 널리 사용됩니다. 대형 호텔과 명소에서는 카드가 使用 가능한 경우도 있습니다.</li><li>비자: 출발 전 대사관 규칙을 확인하세요.</li><li>대기질: 대기질 지수(AQI)를 확인하고 공기가 맑은 날 야외 활동을 계획하세요.</li><li>비상 전화: 경찰 110, 구급차 120, 화재 119.</li><li>언어: 주요 명소에는 영어 표지판이 있지만 간단한 중국어 표현을 배우거나 번역 앱을 사용하는 것이 좋습니다.</li></ul>''',

    'Shanghai': '''<p>상하이는 글로벌 금융 허브이며, 초고층 빌드가 늘어선 미래형 스카이라인으로 유명합니다. 상하이다워와 동방명주 전형타워가 그 상징입니다.</p><p>외탄을 따라 걸으면 식민지 시대 건축 양식을 감상할 수 있고, 프랑스 조계지의 아트 갤러리와 부티크를 탐방할 수도 있습니다. 이화원은 전통적인 중국 문화를 느낄 수 있는 곳입니다. 상하이는 중국의 급속한 발전을 상징하는 도시로, 모든 여행자가 반드시 방문해야 합니다.</p><h3>교통</h3><p><strong>항공:</strong> 상하이지앙（共 Shanghai Hongqiao, PVG)와 상하이푸둥(上海浦东) 두 개의 국제공항이 있습니다. 시내 중심부까지 지하철, 택시, 버스로 이동 가능합니다.</p>''',

    'Xian': '''<p>시안은 중국에서 가장 오래된 도시 중 하나이며 동서실크로드의 동쪽 종점입니다. 가장 유명한 관광지는 진시황제의 능묘를 지키는 약 8,000 개의 테라코타 병사雕像입니다.</p><p>시가를 둘러싸고 있는 보존된古城壁에서는 자전거를 타고 환상적인 전망을 감상할 수 있습니다. 회족 음식 거리도 놓치지 마세요.</p>''',

    'Guilin': '''<p>구이린의 풍경은 중국 고전화의 그|F刹那间습니다.広西チワン族自治区南部に位置し、幻想的なカルスト地形は世界的に有名です。</p><p>最佳の方法は漓江を船で下りながら、石灰岩の峰と竹林、穏やかな村を眺めることです。芦笛洞窟も訪れる価値があります。</p>''',

    'Zhangjiajie': '''<p>장가계는、国連教育科学文化機関から国立公園に指定された美しい石英砂岩の柱状地形ことで有名です。登山や写真愛好家に最適な幻想的な景色が広がっています。</p><h3>見どころ</h3><ul><li>张家界国家森林公園</li><li>天門山</li><li>ガラス橋</li></ul>''',

    'Jiuzhaigou': '''<p>구주계곡은四川省に位置し、鮮やかなターコイズブルーの湖、段状の滝、穏やかな高山 Valley で知られています。写真家の天国と言える場所です。</p><h3>見どころ</h3><ul><li>五彩池</li><li>녹일랑 폭포</li><li>진주탄</li></ul>''',

    'Yangtze': '''<p>양쯔장은 중국에서 가장 긴 강으로, 드라마틱한 삼峡と魅力的な河 cruise가 있습니다. 충칭에서夷陵까지 여러 날간 cruise를 타고 강을 내려가며 해질녘의Town과 역사적인 유적지를 방문할 수 있습니다.</p>''',

    'Iching': '''<p><strong>역경</strong>（I Ching, 易經とも書く）は中国最古の古典の一つであり、変化の書と呼ばれています。64の六爻で構成され、宇宙論、哲学、占術が融合した的思想です。</p><h3>易経の特徴</h3><p>易経は数千年をかけて發展し、各六爻は壊れたまたは壊れていない6本の線から構成されます。伝統的な注解は翼呼ばれ、学者や賢者によって使用されてきました。</p>''',
}

# Process JA and KO sections
new_lines = lines[:]
changes = 0

for lang in ['ja', 'ko']:
    if lang not in LANG_RANGES:
        print(f"WARNING: {lang} section not found!")
        continue
    
    start, end = LANG_RANGES[lang]
    translations = JA_LONGDESC if lang == 'ja' else KO_LONGDESC
    
    print(f"\nProcessing {lang} section (lines {start+1}-{end}):")
    
    for line_no in range(start, end):
        line = lines[line_no]
        stripped = line.strip()
        
        for city, raw_text in translations.items():
            key = 'longDesc' + city
            # Check if this line starts with the key
            if stripped.startswith(key + ': "') or stripped.startswith(key + ':"'):
                # This line needs to be replaced
                indent = line[:len(line) - len(line.lstrip())]
                # JS-escape the raw text and build the new line
                escaped_text = js_escape(raw_text)
                new_line = indent + key + ': "' + escaped_text + '",\n'
                new_lines[line_no] = new_line
                changes += 1
                print(f"  Replaced {city} at line {line_no + 1}")
                break

print(f"\nTotal changes: {changes}")

# Write back
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done!")

# Verify the JS file is syntactically valid
import subprocess
result = subprocess.run(['node', '-e', f'require("./{FILE}")'], 
                       capture_output=True, text=True, cwd='/home/ubuntu/traveltochinaguide.github.io')
if result.returncode == 0:
    print("JS syntax check: PASSED")
else:
    print(f"JS syntax check FAILED: {result.stderr[:300]}")
    # Don't auto-restore - let human fix
    # subprocess.run(['git', 'checkout', FILE], cwd='/home/ubuntu/traveltochinaguide.github.io')
    print("NOTE: File may be corrupted - manual check needed")