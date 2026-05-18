#!/usr/bin/env python3
"""Update ru/medicine.html with Russian translations for descMedicine and longDescMedicine."""

import re

with open('ru/medicine.html', 'r') as f:
    content = f.read()

# 1. Update descMedicine in the subtitle <p> tag (line with id="city-sub" data-lang-key="descMedicine")
old_subtitle = '''<p id="city-sub" data-lang-key="descMedicine" class="mt-2 text-sm sm:text-base text-white/90 max-w-2xl">Discover 中医 — acupuncture, herbal medicine, and the holistic health traditions that have shaped Chinese medicine for millennia.</p>'''
new_subtitle = '''<p id="city-sub" data-lang-key="descMedicine" class="mt-2 text-sm sm:text-base text-white/90 max-w-2xl">Откройте для себя 中医 — иглоукалывание, траволечение и холистические традиции здоровья, формировавшие китайскую медицину на протяжении тысячелетий.</p>'''
assert old_subtitle in content, "Subtitle old text NOT FOUND!"
content = content.replace(old_subtitle, new_subtitle)
print("✓ Updated descMedicine subtitle in HTML")

# 2. Update the city-content div with translated body
old_body = '''<div id="city-content" class="prose text-gray-700" data-lang-key="longDescMedicine"><p><strong>Traditional Chinese Medicine</strong> (中医, zhōngyī) is a medical system that has evolved over more than 2,000 years, including herbal medicine, acupuncture, tuina massage, dietary therapy, and Qigong.</p><h3>Core Principles</h3><ul><li><strong>Qi (气)</strong> — The vital energy that flows through the body. Health is the free flow of qi.</li><li><strong>Yin-Yang (阴阳)</strong> — The complementary opposing forces. Health is a dynamic balance.</li><li><strong>Five Elements (五行)</strong> — Wood, Fire, Earth, Metal, Water — used to classify organs and diseases.</li><li><strong>Meridians (经络)</strong> — Channels through which qi flows, with acupuncture points along them.</li></ul><h3>Key Practices</h3><p><strong>Acupuncture (针灸)</strong> — Insertion of fine needles at specific points. Recognized by WHO for treating dozens of conditions.</p><p><strong>Herbal Medicine (中药)</strong> — Over 3,000 medicinal substances, mostly plants, combined into formulas tailored to the individual.</p><p><strong>Tuina (推拿)</strong> — Therapeutic massage using pressure on meridians and acupoints.</p><h3>Modern Context</h3><p>TCM is practiced alongside Western medicine throughout China and is increasingly integrated into global healthcare.</p></div>'''

new_body = '''<div id="city-content" class="prose text-gray-700" data-lang-key="longDescMedicine"><p><strong>Traditional Chinese Medicine</strong> (中医, zhōngyī) — это медицинская система, которая развивалась на протяжении более 2000 лет и включает траволечение, иглоукалывание, массаж туйна, диетотерапию и цигун.</p><h3>Основные принципы</h3><ul><li><strong>Qi (气)</strong> — Жизненная энергия, циркулирующая по телу. Здоровье — это свободное течение ци.</li><li><strong>Yin-Yang (阴阳)</strong> — Взаимодополняющие противоположные силы. Здоровье — это динамическое равновесие.</li><li><strong>Пять Элементов (五行)</strong> — Дерево, Огонь, Земля, Металл, Вода — используются для классификации органов и болезней.</li><li><strong>Меридианы (经络)</strong> — Каналы, по которым течет ци, с акупунктурными точками вдоль них.</li></ul><h3>Основные практики</h3><p><strong>Акупунктура (针灸)</strong> — Введение тонких игл в определенные точки. Признана ВОЗ для лечения десятков заболеваний.</p><p><strong>Траволечение (中药)</strong> — Более 3000 лекарственных веществ, в основном растительных, объединенных в формулы, подобранные индивидуально.</p><p><strong>Туйна (推拿)</strong> — Лечебный массаж с воздействием на меридианы и акупунктурные точки.</p><h3>Современный контекст</h3><p>ТКМ практикуется наряду с западной медициной по всему Китаю и все активнее интегрируется в мировое здравоохранение.</p></div>'''

assert old_body in content, "Body old text NOT FOUND!"
content = content.replace(old_body, new_body)
print("✓ Updated longDescMedicine body in HTML")

# 3. Update descMedicine in translations JSON
# Find it in the JSON
old_desc_json = '"descMedicine":"Discover 中医 — acupuncture, herbal medicine, and the holistic health traditions that have shaped Chinese medicine for millennia."'
new_desc_json = '"descMedicine":"Откройте для себя 中医 — иглоукалывание, траволечение и холистические традиции здоровья, формировавшие китайскую медицину на протяжении тысячелетий."'

# Need to escape for regex
old_desc_json_escaped = old_desc_json.replace('"', '\\"')
new_desc_json_escaped = new_desc_json.replace('"', '\\"')

# Use simple string replace
assert old_desc_json in content, "Old descMedicine in JSON NOT FOUND!"
content = content.replace(old_desc_json, new_desc_json)
print("✓ Updated descMedicine in translations JSON")

# 4. Add longDescMedicine to translations JSON
# Find where to insert it - after descMedicine in the JSON
# The descMedicine is followed by something like "}," or just ","
insertion_point = new_desc_json
# longDescMedicine should go right after descMedicine
long_desc_json_entry = '"longDescMedicine":"<p><strong>Traditional Chinese Medicine</strong> (中医, zhōngyī) — это медицинская система, которая развивалась на протяжении более 2000 лет и включает траволечение, иглоукалывание, массаж туйна, диетотерапию и цигун.</p><h3>Основные принципы</h3><ul><li><strong>Qi (气)</strong> — Жизненная энергия, циркулирующая по телу. Здоровье — это свободное течение ци.</li><li><strong>Yin-Yang (阴阳)</strong> — Взаимодополняющие противоположные силы. Здоровье — это динамическое равновесие.</li><li><strong>Пять Элементов (五行)</strong> — Дерево, Огонь, Земля, Металл, Вода — используются для классификации органов и болезней.</li><li><strong>Меридианы (经络)</strong> — Каналы, по которым течет ци, с акупунктурными точками вдоль них.</li></ul><h3>Основные практики</h3><p><strong>Акупунктура (针灸)</strong> — Введение тонких игл в определенные точки. Признана ВОЗ для лечения десятков заболеваний.</p><p><strong>Траволечение (中药)</strong> — Более 3000 лекарственных веществ, в основном растительных, объединенных в формулы, подобранные индивидуально.</p><p><strong>Туйна (推拿)</strong> — Лечебный массаж с воздействием на меридианы и акупунктурные точки.</p><h3>Современный контекст</h3><p>ТКМ практикуется наряду с западной медициной по всему Китаю и все активнее интегрируется в мировое здравоохранение.</p>"'

# Insert after descMedicine value (after the closing quote of the value, before the comma)
# The pattern is: "descMedicine":"...translated..." followed by ,"nextKey":
content = content.replace(
    new_desc_json + ',',
    new_desc_json + ',' + long_desc_json_entry + ','
)
print("✓ Added longDescMedicine to translations JSON")

# 5. Verify the changes
with open('ru/medicine.html', 'w') as f:
    f.write(content)

print("\n✓ File written successfully!")

# Quick verification
for key in ['descMedicine', 'longDescMedicine']:
    pattern = rf'"{key}"\s*:\s*"([^"]+)"'
    found = re.search(pattern, content)
    if found:
        val = found.group(1)
        print(f'  {key}: {val[:80]}...')
    else:
        print(f'  {key}: MISSING!')

# Check for Cyrillic in descMedicine
if re.search(r'descMedicine.*[А-Яа-я]', content):
    print("  ✓ descMedicine has Cyrillic characters")
else:
    print("  ✗ descMedicine still has NO Cyrillic!")