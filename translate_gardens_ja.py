#!/usr/bin/env python3
"""Translate gardens.html longDescGardens to Japanese - using robust brace matching."""
import re
import json

# Japanese translation of the longDescGardens body content
japanese_body = """<p><strong>中国の古典庭園</strong>（园林、yuánlín）は、建築、水景、植栽、詩的構想を融合させ、驚くべき美しさと哲学的意味を持つ空間を創り出すランドスケープデザインの傑作です。千年以上の歴史を持ち、中国で最も洗練された芸術形態の一つを代表しています。</p><h3>歴史と哲学</h3><p>中国の庭園の伝統は漢王朝（紀元前206年～紀元220年）に遡り、皇帝たちは道教の神話と人間と自然の調和の理想に触発された離宮を建設しました。宋王朝では文人園（文人园）が発展し、文人たちが瞑想、詩作、芸術追求のための私的な空間を創造しました。</p><p>明・清王朝では古典庭園創造の黄金時代を迎え、特に蘇州では、学者官僚たちが世界観の表現として庭園を設計し、二元性、借景、空間圧縮の原理を体現した数十の傑作が建設されました。</p><h3>ユネスコ世界遺産の庭園</h3><ul><li><strong>拙政園（Humble Administrator's Garden）</strong> — 蘇州にあり、最大かつ最も有名で、蓮池、九曲橋、蘭亭を有します。</li><li><strong>留園（Lingering Garden）</strong> — 蘇州にあり、洗練された空間利用、築山、建築的な優雅さで名高い。</li><li><strong>網師園（Master of the Nets Garden）</strong> — 蘇州にあり、コンパクトな設計と繊細な美しさの傑作。</li><li><strong>頤和園（Summer Palace）</strong> — 北京にあり、昆明湖と万寿山を中心とした最も壮大な離宮庭園。</li></ul><h3>庭園設計の原則</h3><ul><li><strong>借景（Borrowed scenery）</strong> — 周囲の景観を庭園の眺めに取り入れる技法。</li><li><strong>山水（Shan shui）</strong> — 山（shan）と水（shui）の相互作用を庭園の中核要素とする。</li><li><strong>仮山（Pseudo-randomness）</strong> — 自然な不規則性を表現するために設計された築山。</li><li><strong>フレーミング（Framing）</strong> — 詩框（诗框）として形作られた窓や出入り口で、厳選された景色を創り出す。</li></ul><h3>盆景：鉢植え景観の芸術</h3><p>古典庭園と密接に関連するのが<em>盆景</em>（penjing）です。これは容器の中にミニチュアの景観を育成する芸術です。庭園と同様に、盆景は限られた空間に自然の本質を捉え、山、水、木々を一つの芸術的構成に圧縮することを目指しています。</p>"""

# Japanese translation for descGardens
japanese_desc = "中国庭園デザインの芸術を発見 — 蘇州のユネスコ世界遺産の古典庭園から離宮庭園、盆景の古来の伝統まで。"

with open('ja/gardens.html', 'r') as f:
    content = f.read()

# 1. Update the body content
old_body_marker = '<div id="city-content" class="prose text-gray-700" data-lang-key="longDescGardens">'
start = content.find(old_body_marker)
content_start = start + len(old_body_marker)

# Find the closing </div> of city-content by looking for the pattern: </div>\n      </div>\n    </article>
end_marker = '\n      </div>\n    </article>'
end_pos = content.find(end_marker, start)
# The city-content's </div> is right before end_marker
# Actually looking at the structure, the body is: <div id="city-content"...>...(HTML body)...</div>
# Then </div> closes the p-8 div, then </article>
# The body's closing </div> is the last </div> before end_marker

# Find the last </div> before end_marker
last_div = content.rfind('</div>', content_start, end_pos)
if last_div == -1:
    print("ERROR: could not find closing div")
    exit(1)

new_content = content[:content_start] + japanese_body + content[last_div:]
content = new_content

# 2. Update descGardens in hero section
old_desc = 'data-lang-key="descGardens" class="mt-2 text-sm sm:text-base text-white/90 max-w-2xl">Discover the art of Chinese garden design — from Suzhou\'s UNESCO-listed classical gardens to imperial retreats and the ancient tradition of penjing.'
new_desc = 'data-lang-key="descGardens" class="mt-2 text-sm sm:text-base text-white/90 max-w-2xl">' + japanese_desc
if old_desc in content:
    content = content.replace(old_desc, new_desc)
else:
    print("WARNING: descGardens text not found, checking...")
    # Try to find it
    idx = content.find('data-lang-key="descGardens"')
    if idx >= 0:
        print(f"Found at position {idx}")
        print(content[idx:idx+200])

# 3. Update window.translations JSON using regex
# Find the pattern: window.translations = { ... };
pattern = r'(window\.translations\s*=\s*)(\{.*?\})(\s*;)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("ERROR: could not find translations JSON with regex")
    exit(1)

json_str = match.group(2)
try:
    translations = json.loads(json_str)
except:
    print("ERROR: JSON parse failed with regex approach")
    # Try a more robust pattern
    pattern2 = r'window\.translations\s*=\s*({.*?});\s*window\.cityDetails'
    match2 = re.search(pattern2, content, re.DOTALL)
    if match2:
        json_str2 = match2.group(1)
        translations = json.loads(json_str2)
    else:
        print("Could not parse JSON")
        exit(1)

translations['ja']['longDescGardens'] = japanese_body
translations['ja']['descGardens'] = japanese_desc

new_json_str = json.dumps(translations, ensure_ascii=False)

# Replace using the matched groups
content = content[:match.start(2)] + new_json_str + content[match.end(2):]

with open('ja/gardens.html', 'w') as f:
    f.write(content)

print("✅ ja/gardens.html updated successfully")
print(f"   - longDescGardens added ({len(japanese_body)} chars)")
print(f"   - descGardens translated: {japanese_desc}")