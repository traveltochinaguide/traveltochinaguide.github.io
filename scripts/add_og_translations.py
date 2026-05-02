import re

with open('/home/ubuntu/traveltochinaguide.github.io/js/translations.js', 'r') as f:
    content = f.read()

# Translation entries for ogTitleBeijing and ogDescBeijing
# These go after each descBeijing line in each language section
entries = [
    # EN city page descBeijing (line ~43)
    ('ogTitleBeijing: "Beijing Travel Guide - Imperial Palace, Great Wall & Tours",',
     'ogDescBeijing: "Explore Beijing with guides to the Forbidden City, Great Wall, Temple of Heaven, and authentic Peking Duck. Plan your Beijing tour with insider tips.",'),
    # ZH city page descBeijing (line ~239)
    ('ogTitleBeijing: "北京旅游指南 - 故宫、天坛寺、八达岭长城",',
     'ogDescBeijing: "北京旅游完全指南：故宫、天坛、八达岭长城、颐和园实用信息。北京烤鸭、胡同文化、夜生活全涵盖。",'),
    # JA city page descBeijing (line ~480)
    ('ogTitleBeijing: "北京旅行ガイド - 故宮、天壇寺、八達嶺长城",',
     'ogDescBeijing: "北京旅行 完全ガイド: 故宮、天壇寺、八達嶺の長城を解説。胡同歩き、北京ダック、北京の穴場情報を徹底紹介。",'),
    # KO city page descBeijing (line ~667)
    ('ogTitleBeijing: "베이징 여행 가이드 - 자금성, 만리장성, 천단사",',
     'ogDescBeijing: "베이징 여행의 모든 것: 자금성, 천단사, 만리장지(바다링) 가이드. 베이징덕훙통&야경을 한눈에!",'),
    # RU city page descBeijing (line ~855)
    ('ogTitleBeijing: "Путеводитель по Пекину - Запретный город, Великая стена",',
     'ogDescBeijing: "Всё о Пекине: Запретный город, Храм Неба, Великая стена (Бадалин и Мутяньюй). Советы по пекинской утке и хутонам.",'),
    # FR city page descBeijing (line ~1043)
    ("ogTitleBeijing: \"Guide de voyage à Beijing - Cité interdite, Grande Muraille & Palais d'Été\",",
     'ogDescBeijing: "Tout sur Beijing: Cité interdite, Temple du Ciel, Grande Muraille (Mutianyu & Badaling). Conseils sur le canard pékinois et les hutongs.",'),
    # DE city page descBeijing (line ~1231)
    ('ogTitleBeijing: "Peking Reiseführer - Verbotene Stadt, Große Mauer & Sommerpalast",',
     'ogDescBeijing: "Peking komplett: Verbotene Stadt, Tempel des Himmels, Große Mauer (Mutianyu & Badaling). Peking Ente & Hutongs Insider-Tipps.",'),
    # ES city page descBeijing (line ~1419)
    ('ogTitleBeijing: "Guía de viaje a Peking - Ciudad Prohibida, Gran Muralla & Palacio de Verano",',
     'ogDescBeijing: "Todo sobre Pekin: Ciudad Prohibida, Templo del Cielo, Gran Muralla (Mutianyu & Badaling). Consejos sobre Pato Pekines y Hutongs.",'),
]

# Find all descBeijing: lines (8 total: EN, ZH, JA, KO, RU, FR, DE, ES city pages)
# Skip the cityDetails descKey reference
matches = []
for m in re.finditer(r'descBeijing:', content):
    # Check if this is the cityDetails reference (has quote after, not colon)
    start = m.start()
    # Get the line containing this match
    line_start = content.rfind('\n', 0, start) + 1
    line_end = content.find('\n', m.end())
    line = content[line_start:line_end]
    if 'descKey' not in line:  # Skip cityDetails descKey reference
        matches.append((line_start, line_end, line.strip()))

print(f"Found {len(matches)} descBeijing (city page) occurrences:")
for i, (ls, le, line) in enumerate(matches):
    print(f"  {i}: pos={ls}, line: {line[:60]}...")

# Insert after each descBeijing line, in reverse order to preserve positions
for i in range(len(matches)-1, -1, -1):
    line_start, line_end, line = matches[i]
    if i >= len(entries):
        print(f"Warning: no entry for index {i}")
        continue
    
    og_title, og_desc = entries[i]
    insert_pos = line_end
    insert_text = '\n  ' + og_title + '\n  ' + og_desc
    
    content = content[:insert_pos] + insert_text + content[insert_pos:]
    print(f"Inserted entry {i} after pos {insert_pos}")

# Verify
og_count = content.count('ogTitleBeijing:')
print(f"\nogTitleBeijing count: {og_count} (expected: 8)")

with open('/home/ubuntu/traveltochinaguide.github.io/js/translations.js', 'w') as f:
    f.write(content)

print("Done!")