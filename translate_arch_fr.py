import re

page = 'architecture'
lang = 'fr'

# 1. Read the EN source longDesc
with open(f'{page}.html') as f:
    en_content = f.read()

# Extract the longDesc body HTML
match = re.search(r'data-lang-key="longDescArchitecture">(.+?)</div>\s*</div>\s*</article>', en_content, re.DOTALL)
if not match:
    print("ERROR: Could not find longDescArchitecture in EN file")
    exit(1)

en_longdesc = match.group(1)
print(f"EN longDesc length: {len(en_longdesc)} chars")

# 2. Translate to French (keep ALL HTML tags intact, translate only text nodes)
# French translation
fr_longdesc = '''<p><strong>L'architecture chinoise</strong> (建筑, jiànzhù) représente l'une des traditions de construction les plus anciennes et les plus distinctives au monde — des palais impériaux et temples sacrés aux maisons à cour et pagodes. Avec une histoire continue de plus de trois millénaires, l'architecture chinoise reflète des principes philosophiques profonds : l'harmonie avec la nature, le symbolisme cosmique et la hiérarchie sociale.</p><h3>Histoire et philosophie</h3><p>La tradition architecturale chinoise a émergé sous la dynastie Shang (vers 1600-1046 av. J.-C.), avec les premières plates-formes de palais et les bâtiments rituels établissant des modèles qui perdureraient pendant des millénaires. La dynastie Han (206 av. J.-C. – 220 apr. J.-C.) a codifié des principes architecturaux qui alignaient les bâtiments sur les directions cosmiques et les cycles saisonniers.</p><p>L'architecture chinoise se caractérise par l'accent mis sur les lignes horizontales, les avant-toits relevés, la structure en bois et les agencements basés sur des cours — un système développé à son plus haut niveau d'expression dans la Cité Interdite (紫禁城) à Pékin, le plus grand complexe impérial du monde.</p><h3>Principaux types architecturaux</h3><ul><li><strong>Palais impériaux</strong> — la Cité Interdite à Pékin, avec ses 980 bâtiments sur 72 hectares, est l'exemple suprême de l'architecture palatiale chinoise. Le Palais d'Été (颐和园) à proximité démontre comment les retraites impériales combinaient architecture et paysage.</li><li><strong>Édifices religieux</strong> — les temples bouddhistes (佛寺), les temples taoïstes (道观) et les pagodes (塔) présentent des toits incurvés distinctifs, des murs vermillon et une ornementation symbolique. Le Temple du Ciel (天坛) à Pékin est un chef-d'œuvre d'architecture circulaire et de symbolisme céleste.</li><li><strong>Maisons à cour (四合院)</strong> — habitations urbaines traditionnelles organisées autour d'une cour centrale, incarnant les principes d'intimité, de hiérarchie familiale et d'harmonie avec l'environnement. Encore visibles dans les hutongs de Pékin.</li><li><strong>Pavillons de jardin</strong> — les structures de jardin comme les pavillons (亭), les corridors (廊) et les portes de lune fusionnent l'architecture et la conception paysagère en compositions unifiées.</li></ul><h3>Principes architecturaux</h3><ul><li><strong>Alignement axial (中轴线)</strong> — les grands complexes sont organisés le long d'un axe central nord-sud, avec les bâtiments importants positionnés symétriquement.</li><li><strong>Avant-toits relevés (斗拱)</strong> — les coins de toit incurvés distinctifs qui donnent aux bâtiments chinois leur silhouette reconnaissable et servent à des fins pratiques d'ombrage et d'évacuation des eaux.</li><li><strong>Structure en bois (木结构)</strong> — construction à poteaux et poutres utilisant des assemblages de bois emboîtés, offrant flexibilité et résistance aux séismes.</li><li><strong>Symbolisme cosmologique</strong> — les nombres, les couleurs et les orientations suivent des principes cosmologiques (cinq éléments, huit trigrammes, directions cardinales).</li></ul><h3>Visiter l'architecture chinoise</h3><p>Pékin reste la meilleure destination pour découvrir le patrimoine architectural chinois : la Cité Interdite, le Temple du Ciel, le Palais d'Été et le Temple des Lamas présentent l'architecture impériale et religieuse. Pour les maisons à cour et la vie des hutongs, une promenade dans les vieux quartiers de Pékin révèle l'architecture domestique traditionnelle. Les jardins classiques de Suzhou intègrent l'architecture de manière harmonieuse avec la conception paysagère.</p>'''

# 3. Read the French file
with open(f'{lang}/{page}.html') as f:
    fr_content = f.read()

# 4. Update the body content (the city-content div)
# Find the longDesc div content in fr file and replace
pattern_body = r'(<div id="city-content" class="prose text-gray-700" data-lang-key="longDescArchitecture">).+?(</div>\s*</div>\s*</article>)'
fr_content = re.sub(pattern_body, r'\1' + fr_longdesc + r'\2', fr_content, count=1, flags=re.DOTALL)

# 5. Update the window.translations JSON
# Add longDescArchitecture and update descArchitecture (French translation)
fr_desc = "Découvrez l'architecture chinoise — des palais impériaux de la Cité Interdite à la géométrie du Temple du Ciel, en passant par les maisons à cour et les pagodes."

# Fix: descArchitecture in the HTML body (the <p id="city-sub"> element)
pattern_desc_body = r'(data-lang-key="descArchitecture"[^>]*>).*?(</p>)'
fr_content = re.sub(pattern_desc_body, r'\1' + fr_desc + r'\2', fr_content, count=1)

# Update window.translations JSON
# Find the translations object
pattern_js = r'(window\.translations\s*=\s*\{)'
match_js = re.search(pattern_js, fr_content)
if not match_js:
    print("ERROR: Could not find window.translations")
    exit(1)

# Find the fr object inside translations
# We need to add longDescArchitecture and update descArchitecture inside the fr object
# Strategy: find the "fr" object and modify it

# Find the fr translations object 
start_idx = fr_content.find('"fr":{')
if start_idx < 0:
    print("ERROR: Could not find fr translations object")
    exit(1)

# Find closing } of fr object - match depth
idx = start_idx + 5  # skip "fr":{
depth = 1
i = idx
while i < len(fr_content) and depth > 0:
    if fr_content[i] == '{':
        depth += 1
    elif fr_content[i] == '}':
        depth -= 1
    i += 1
fr_obj_end = i  # position after the closing }

fr_obj = fr_content[start_idx:fr_obj_end]
print(f"FR object found at {start_idx}-{fr_obj_end}, length: {len(fr_obj)}")

# Check if longDescArchitecture already exists in fr_obj
if '"longDescArchitecture"' in fr_obj:
    print("longDescArchitecture already exists, updating...")
    # Replace existing value
    fr_obj = re.sub(
        r'"longDescArchitecture"\s*:\s*"[^"]*"',
        '"longDescArchitecture":"' + fr_longdesc.replace('"', '\\"') + '"',
        fr_obj
    )
else:
    print("Adding longDescArchitecture...")
    # Add it before the closing }}
    # Find the last key-value pair before the final }}
    last_comma = fr_obj.rfind(',')
    if last_comma > 0:
        fr_obj = fr_obj[:last_comma] + ',' + f'\n"longDescArchitecture":"{fr_longdesc.replace(chr(34), chr(92)+chr(34))}"\n' + fr_obj[last_comma:]
    else:
        # Very small object, just append
        fr_obj = fr_obj[:-1] + f',"longDescArchitecture":"{fr_longdesc.replace(chr(34), chr(92)+chr(34))}"' + '}'

# Now update descArchitecture if it exists
if '"descArchitecture"' in fr_obj:
    print("Updating descArchitecture...")
    fr_obj = re.sub(
        r'"descArchitecture"\s*:\s*"[^"]*"',
        '"descArchitecture":"' + fr_desc.replace('"', '\\"') + '"',
        fr_obj
    )

# Replace the fr object in the full content
fr_content = fr_content[:start_idx] + fr_obj + fr_content[fr_obj_end:]

# 6. Write the file
with open(f'{lang}/{page}.html', 'w') as f:
    f.write(fr_content)

print("SUCCESS: French file updated")
print(f"Total length: {len(fr_content)}")