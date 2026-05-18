import re
import json

# German translated body content
german_body = '<p><strong>Chinesischer Papierschnitt</strong> (\u526a\u7eb8, Ji\u01cenzh\u01d0) ist eine der beliebtesten und \u00e4ltesten Volksk\u00fcnste Chinas, deren Urspr\u00fcnge bis ins 6. Jahrhundert n. Chr. zur\u00fcckreichen. Mit nur Papier und Schere oder Messer erschaffen Kunsthandwerker kunstvolle Motive \u2014 Blumen, Drachen, Schriftzeichen und Szenen \u2014 die Geschichten von Wohlstand, Gl\u00fcck und guter Fortune erz\u00e4hlen.</p><h3>Geschichte und Urspr\u00fcnge</h3><p>Der Papierschnitt entstand kurz nach der Erfindung des Papiers w\u00e4hrend der Han-Dynastie (206 v. Chr. \u2013 220 n. Chr.). Urspr\u00fcnglich in religi\u00f6sen Ritualen und als dekorative Opfergaben verwendet, verbreitete sich diese Kunstform w\u00e4hrend der Ming- und Qing-Dynastien weit und wurde ein fester Bestandteil chinesischer Feierlichkeiten und des Alltags. Im Jahr 2009 wurde der chinesische Papierschnitt (Jianzhi) in die UNESCO-Repr\u00e4sentative Liste des immateriellen Kulturerbes der Menschheit aufgenommen.</p><h3>Symbolik und Bedeutung</h3><p>Jedes Motiv im chinesischen Papierschnitt tr\u00e4gt eine tiefe symbolische Bedeutung. <strong>Drachen</strong> (\u9f99) symbolisieren Macht, St\u00e4rke und Gl\u00fcck. <strong>Pfingstrosen</strong> (\u7261\u4e39) repr\u00e4sentieren Reichtum und Ehre. <strong>Fische</strong> (\u9c7c) stehen f\u00fcr \u00dcberfluss und Wohlstand \u2014 das Wort \u9c7c (y\u00fa) klingt wie \u4f59 (y\u00fa), was \u201e\u00dcberfluss\u201c bedeutet. <strong>Flederm\u00e4use</strong> (\u8760, f\u00fa) sind Wortspiele f\u00fcr \u798f (f\u00fa), also Gl\u00fcck und Segen. <strong>Ph\u00f6nix</strong> (\u51e4) repr\u00e4sentiert Anmut und Tugend.</p><h3>Regionale Stile</h3><p>Der chinesische Papierschnitt variiert stark je nach Region. <strong>Nordchina</strong> bevorzugt kr\u00e4ftige, \u00fcbertriebene Designs mit starken Linien \u2014 der n\u00f6rdliche Stil ist dekorativ und erz\u00e4hlerisch. <strong>S\u00fcdchina</strong>, insbesondere Fujian und Guangdong, produziert feinere, komplexere Arbeiten mit zarten Details. <strong>S\u00fcdliches Jiangsu</strong> gilt mit seiner raffinierten Pr\u00e4zision als eine der feinsten Papierschnitttraditionen der Welt.</p><h3>Papierschnitt im modernen China</h3><p>Heute ist Jianzhi eine lebendige Kunst. W\u00e4hrend des chinesischen Neujahrs (\u6625\u8282) werden rote Papierschnitte mit Gl\u00fcckssymbolen an Fenstern und T\u00fcren in ganz China angebracht. Bei Hochzeiten erscheinen Doppelgl\u00fcckssymbole (\u56cd) \u00fcberall. Papierschnitte sind auch als Geschenke, Souvenirs und in k\u00fcnstlerischen Installationen beliebt. Besucher k\u00f6nnen Papierschnitt-Workshops in Pekings Hutongs, Xi\'ans Altstadt und in Kunsthandwerksd\u00f6rfern im ganzen Land finden.</p>'

german_desc = 'Mandarin, Schriftzeichen und sinoxenische Sprachen'

# Read the German file
with open('de/language.html', 'r') as f:
    content = f.read()

# 1. Replace the city-content body
old_body_pattern = r'(data-lang-key="longDescLanguage">).*?(</div>\s*</div>\s*</article>)'
content = re.sub(old_body_pattern, lambda m: m.group(1) + german_body + m.group(2), content, count=1, flags=re.DOTALL)

# 2. Update descLanguage in the HTML subtitle
old_desc_html = r'(data-lang-key="descLanguage"[^>]*>)[^<]*(</p>)'
content = re.sub(old_desc_html, lambda m: m.group(1) + german_desc + m.group(2), content, count=1)

# 3. Update window.translations
m = re.search(r'window\.translations\s*=\s*({.*?});', content, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    de_data = data.get('de', {})
    de_data['descLanguage'] = german_desc
    de_data['longDescLanguage'] = german_body
    data['de'] = de_data
    new_json = json.dumps(data, ensure_ascii=False)
    content = content[:m.start(1)] + new_json + content[m.end(1):]

# Write back
with open('de/language.html', 'w') as f:
    f.write(content)

print("DONE - German file updated successfully")

# Verify
with open('de/language.html', 'r') as f:
    c2 = f.read()
m2 = re.search(r'window\.translations\s*=\s*({.*?});', c2, re.DOTALL)
if m2:
    data2 = json.loads(m2.group(1))
    de = data2.get('de', {})
    print(f'longDescLanguage present: {bool(de.get("longDescLanguage"))}')
    print(f'longDescLanguage length: {len(de.get("longDescLanguage",""))}')
    print(f'descLanguage: {de.get("descLanguage","NOT FOUND")}')