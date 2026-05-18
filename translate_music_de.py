#!/usr/bin/env python3
"""
Translate music page longDesc from English to German.
Updates de/music.html with translated body content and translations JSON.
"""
import re
import json

# === 1. Read the English source HTML body ===
with open('music.html') as f:
    en_content = f.read()

# Extract the body inside data-lang-key="longDescMusic">
start_body = en_content.find('data-lang-key="longDescMusic">')
start_body += len('data-lang-key="longDescMusic">')

# Find closing of city-content div using depth counting
pos = start_body
depth = 1
while depth > 0 and pos < len(en_content):
    open_tag = en_content.find('<div', pos, pos + 50)
    close_tag = en_content.find('</div>', pos)
    if close_tag == -1:
        break
    if open_tag != -1 and open_tag < close_tag:
        depth += 1
        pos = open_tag + 4
    else:
        depth -= 1
        if depth == 0:
            en_body = en_content[start_body:close_tag]
            break
    pos = close_tag + 6

print(f"EN body length: {len(en_body)} chars")

# === 2. German translation ===
# I'll write the translated HTML content directly
de_body = """<p><strong>Chinesische traditionelle Musik</strong> (音乐, yīnyuè) erstreckt sich über mehr als dreitausend Jahre – von ritueller Hofmusik und der meditativen Guqin bis zur lebendigen Peking-Oper und regionalen Volksliedern. Anders als die auf Harmonie aufgebaute westliche Musik betont die chinesische Musik Melodie, Atmosphäre und die Verbindung zwischen Musik und Natur, Philosophie und emotionalem Ausdruck.</p><h3>Geschichte und Philosophie</h3><p>Die chinesische Musik entstand in rituellen Zeremonien während der Zhou-Dynastie (ca. 1046–256 v. Chr.), als Hofmusik (雅乐) zur Ehrung der Vorfahren und Gottheiten aufgeführt wurde. Die Guqin (古琴), eine siebensaitige Zither, wurde zum Instrument der Gelehrten und Weisen – ihr leiser, meditativer Klang galt als Weg zur Selbstkultivierung. Die Musik wurde durch das System der 五音 (fünf Elemente) mit der Kosmologie verbunden, wobei jede Note einer Himmelsrichtung, einer Jahreszeit und einer emotionalen Qualität zugeordnet war.</p><h3>Wichtige Instrumente</h3><ul><li><strong>Guqin (古琴)</strong> – eine siebensaitige Zither mit 3.000-jähriger Geschichte, geschätzt von konfuzianischen Gelehrten und daoistischen Praktizierenden. Ihr intimer, meditativer Klang wird als „der Klang des Kosmos" beschrieben. Die UNESCO erkannte die Guqin 2003 als immaterielles Kulturerbe an.</li><li><strong>Guzheng (古筝)</strong> – eine 21-saitige horizontale Zither mit einem helleren, resonanteren Ton als die Guqin. Seit der Qin-Dynastie beliebt, wird sie sowohl in der klassischen als auch in der zeitgenössischen Musik eingesetzt.</li><li><strong>Pipa (琵琶)</strong> – eine viersaitige Laute mit einem eindringlichen, perkussiven Klang. Entlang der Seidenstraße eingeführt, entfaltet sie eine unverwechselbare Tremolo-Technik in Solo- und Ensemble-Aufführungen.</li><li><strong>Erhu (二胡)</strong> – ein zweisaitiges Streichinstrument mit einem gesangähnlichen Klang. Oft als „chinesische Violine" bezeichnet, drückt sie tiefe Trauer und Freude mit bemerkenswerter emotionaler Bandbreite aus.</li></ul><h3>Traditionelle Formen</h3><ul><li><strong>Peking-Oper (京剧)</strong> – Chinas berühmteste Operntradition, die Gesang, Schauspiel, Kampfkunst und Akrobatik vereint. Sie zeichnet sich durch aufwändige Kostüme, stilisierte Bewegungen und einen einzigartigen Gesangsstil aus.</li><li><strong>Kunqu (昆曲)</strong> – Chinas älteste Opernform (ca. 14. Jahrhundert), bekannt für ihre eleganten Melodien, kunstvollen Texte und anmutige Choreografie. Ebenfalls UNESCO-Weltkulturerbe.</li><li><strong>Regionale Volksmusik</strong> – dramatische Unterschiede zwischen den Provinzen, von den ergreifenden Melodien des Nordens (信天游) bis zu den beschwingten Liedern Yunnans und den pentatonischen Tonleitern Guangdongs.</li></ul><h3>Chinesische Musik erleben</h3><p>Das Nationale Zentrum für Darstellende Künste und die Konzerthalle in Peking bieten traditionelle Musikaufführungen. Für ein intimes Erlebnis besuchen Sie den Lama-Tempel an Sonntagmorgen, wenn sich Guqin-Spieler versammeln. Das Shanghai-Konservatorium und das Jiangnan-Teehaus in Suzhou bieten regelmäßige Guzheng- und Pipa-Aufführungen.</p>
        <h3>Lernen und Praxis</h3><p>Wer chinesische traditionelle Musik erlernen möchte, findet Lehrer und Schulen in den großen Städten. Die Guqin wird oft in einer Meister-Schüler-Tradition unterrichtet, die nicht nur Technik, sondern auch die Philosophie und Denkweise des Spielers betont. Viele Universitäten bieten mittlerweile Kurse in chinesischer Musikwissenschaft und Aufführungspraxis an.</p><h3>Zeitgenössische Fusion</h3><p>Moderne Künstler verbinden traditionelle chinesische Instrumente mit Jazz, elektronischer und westlicher klassischer Musik. Gruppen wie die Twelve Girls Band und Künstler wie Wu Man (Pipa) haben chinesische Musik einem globalen Publikum nähergebracht, ohne ihr Wesen zu verlieren.</p>"""

print(f"DE body length: {len(de_body)} chars")

# === 3. Read German file ===
with open('de/music.html') as f:
    de_content = f.read()

# === 4. Update the body content in HTML ===
# Find the current body in the German file
start_de = de_content.find('data-lang-key="longDescMusic">')
start_de += len('data-lang-key="longDescMusic">')

pos = start_de
depth = 1
while depth > 0 and pos < len(de_content):
    open_tag = de_content.find('<div', pos, pos + 50)
    close_tag = de_content.find('</div>', pos)
    if close_tag == -1:
        break
    if open_tag != -1 and open_tag < close_tag:
        depth += 1
        pos = open_tag + 4
    else:
        depth -= 1
        if depth == 0:
            old_body = de_content[start_de:close_tag]
            break
    pos = close_tag + 6

# Replace old body with new body
de_content = de_content[:start_de] + de_body + de_content[start_de + len(old_body):]

# === 5. Update translations JSON ===
# Find the window.translations JSON
m = re.search(r'window\.translations\s*=\s*({.*?});', de_content, re.DOTALL)
if not m:
    print("ERROR: Could not find window.translations")
    exit(1)

json_str = m.group(1)
data = json.loads(json_str)

# Add longDescMusic
data['de']['longDescMusic'] = de_body

# Update descMusic to German
data['de']['descMusic'] = "Entdecken Sie die chinesische traditionelle Musik – von der antiken Guqin und Guzheng über die Peking-Oper, Volksmelodien bis hin zur zeremoniellen Hofmusik."

# Serialize back
new_json_str = json.dumps(data, ensure_ascii=False)

# Replace in content
de_content = de_content[:m.start(1)] + new_json_str + de_content[m.end(1):]

# === 6. Write file ===
with open('de/music.html', 'w') as f:
    f.write(de_content)

print("✓ Updated de/music.html successfully!")
print(f"  - Added longDescMusic ({len(de_body)} chars)")
print(f"  - Updated descMusic to German")