#!/usr/bin/env python3
"""
Translate architecture.html longDescArchitecture + descArchitecture to Japanese.
Updates ja/architecture.html inline window.translations JSON + body content.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path('/home/ubuntu/traveltochinaguide.github.io')
EN_FILE = ROOT / 'architecture.html'
JA_FILE = ROOT / 'ja' / 'architecture.html'

# === STEP 1: Extract English longDesc body ===
en_html = EN_FILE.read_text(encoding='utf-8')
m = re.search(
    r'data-lang-key="longDescArchitecture">(.*?)</div>\s*</div>\s*</article>',
    en_html, re.DOTALL
)
if not m:
    print("ERROR: Could not find longDescArchitecture in EN file")
    sys.exit(1)
en_long_desc = m.group(1)

# === STEP 2: Japanese translations ===
# DescArchitecture (short)
ja_desc = "中国建築―故宮の壮麗な宮殿から天壇の幾何学美、四合院、そして塔のデザインまで、中国建築の世界をご紹介します。"

# LongDescArchitecture (full HTML body) - Japanese translation
ja_long_desc = (
    '<p><strong>中国建築</strong>（建筑、jiànzhù）は、世界最古かつ最も特徴的な建築伝統のひとつであり、'
    '皇室の宮殿や神聖な寺院から四合院や塔に至るまで多岐にわたります。'
    '3000年以上にわたる連続した歴史を持ち、中国建築は自然界との調和、宇宙的象徴性、'
    '社会的階層といった深い哲学的 principles を反映しています。</p>'
    '<h3>歴史と哲学</h3>'
    '<p>中国建築の伝統は殷（商）王朝（紀元前1600～1046年頃）に始まり、'
    '初期の宮殿基壇や儀礼建築がその後数千年にわたって受け継がれる様式を確立しました。'
    '漢王朝（紀元前206年～紀元220年）では建築 principles が体系化され、'
    '建物を宇宙の方角や季節の循環に合わせて配置することが定められました。</p>'
    '<p>中国建築の特徴は、水平線の強調、反り返った軒先、木造構造、'
    'そして中庭を中心とした配置にあります。これらの様式は北京の故宮（紫禁城）で最高潮に達し、'
    '世界最大の皇室建築群を形成しています。</p>'
    '<h3>主な建築様式</h3>'
    '<ul>'
    '<li><strong>皇室宮殿</strong> ― 北京の故宮は72ヘクタールに980棟の建物を擁し、'
    '中国宮殿建築の最高傑作です。近隣の頤和園（いわえん）は、'
    '皇室の離宮が建築と景観を融合させた好例です。</li>'
    '<li><strong>宗教建築</strong> ― 仏教寺院（佛寺）、道教寺院（道觀）、塔（塔）は、'
    '特徴的な曲線の屋根、朱色の壁、象徴的な装飾が施されています。'
    '北京の天壇（天壇）は円形建築と天体象徴の傑作です。</li>'
    '<li><strong>四合院</strong> ― 中心となる中庭の周りに配置された伝統的な都市住宅で、'
    'プライバシー、家族の階層、環境との調和の principles を体現しています。'
    '北京の胡同（フートン）で今も見ることができます。</li>'
    '<li><strong>庭園亭閣</strong> ― 亭（パビリオン）、廊（回廊）、月門（満月門）などの庭園構造物は、'
    '建築とランドスケープデザインを一体化させています。</li>'
    '</ul>'
    '<h3>建築 principles</h3>'
    '<ul>'
    '<li><strong>中軸線</strong> ― 壮大な建築群は中央の南北軸に沿って配置され、'
    '重要な建物は左右対称に位置します。</li>'
    '<li><strong>斗拱（ときょう）</strong> ― 独特の反り返った軒先で、'
    '中国建築の特徴的なシルエットを生み出すとともに、日除けや排水の実用的機能も果たします。</li>'
    '<li><strong>木構造</strong> ― 組み合わせ式の木製継手を用いた柱と梁の構造で、'
    '柔軟性と耐震性を備えています。</li>'
    '<li><strong>宇宙的象徴性</strong> ― 数字、色、方角は宇宙論的 principles'
'（五行、八卦、方位）に従います。</li>'
    '</ul>'
    '<h3>中国建築の見学</h3>'
    '<p>中国建築遺産を体験するには北京が最適な目的地です。'
    '故宮、天壇、頤和園、雍和宮（ラマ寺院）では皇室建築と宗教建築を鑑賞できます。'
    '四合院や胡同の生活を知るには、北京の旧市街を散策すると伝統的な住宅建築に出会えます。'
    '蘇州の古典庭園では、建築が景観デザインと見事に融合しています。</p>'
)

print("--- Translation prepared ---")
print(f"  ja_desc: {ja_desc[:60]}...")
print(f"  ja_long_desc length: {len(ja_long_desc)} chars")

# === STEP 3: Read ja file and update ===
ja_html = JA_FILE.read_text(encoding='utf-8')
orig_ja = ja_html

# --- 3a. Update inline window.translations JSON ---
json_m = re.search(r'window\.translations\s*=\s*({.*?});', ja_html, re.DOTALL)
if not json_m:
    print("ERROR: Could not find window.translations in ja file")
    sys.exit(1)

trans_data = json.loads(json_m.group(1))
lang_key = list(trans_data.keys())[0]

# Add/update longDescArchitecture
trans_data[lang_key]['longDescArchitecture'] = ja_long_desc

# Update descArchitecture (already exists, but value is English)
trans_data[lang_key]['descArchitecture'] = ja_desc

# Serialize back (compact, then re-indent)
new_json_str = json.dumps(trans_data, ensure_ascii=False, indent=2)
# But we need to keep it on one line since it's inline JS...
# Let's check original format
orig_json_str = json_m.group(1)
if '\n' in orig_json_str:
    # Multi-line
    new_json_oneline = json.dumps(trans_data, ensure_ascii=False, indent=2)
else:
    new_json_oneline = json.dumps(trans_data, ensure_ascii=False)

ja_html = ja_html[:json_m.start(1)] + new_json_oneline + ja_html[json_m.end(1):]

# --- 3b. Update body content for longDescArchitecture ---
long_m = re.search(
    r'(data-lang-key="longDescArchitecture">).*?(</div>\s*</div>\s*</article>)',
    ja_html, re.DOTALL
)
if long_m:
    ja_html = ja_html[:long_m.start(1)] + long_m.group(1) + ja_long_desc + long_m.group(2) + ja_html[long_m.end(2):]
    print("  Body longDescArchitecture updated")
else:
    print("WARNING: Could not find body longDescArchitecture marker")

# --- 3c. Update descArchitecture display text ---
desc_m = re.search(
    r'(data-lang-key="descArchitecture"[^>]*>)([^<]+)(<)',
    ja_html
)
if desc_m:
    ja_html = ja_html[:desc_m.start(2)] + ja_desc + ja_html[desc_m.end(2):]
    print("  descArchitecture display text updated")
else:
    print("WARNING: Could not find descArchitecture display text")

if ja_html == orig_ja:
    print("ERROR: No changes made to ja file!")
    sys.exit(1)

# === STEP 4: Write file ===
JA_FILE.write_text(ja_html, encoding='utf-8')
print(f"  Wrote {JA_FILE}")

# === STEP 5: Verify ===
verify = JA_FILE.read_text(encoding='utf-8')
if 'longDescArchitecture' in verify and ja_desc in verify:
    print("  VERIFICATION PASSED")
else:
    print("  VERIFICATION FAILED!")
    sys.exit(1)

print("DONE")