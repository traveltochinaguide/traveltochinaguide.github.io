#!/usr/bin/env python3
"""Translate language.html longDesc and desc from EN to ES for es/language.html"""

import re

# Read the ES file
with open('es/language.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The Spanish translation of the longDesc content about Chinese paper cutting
spanish_longdesc = (
    '<p><strong>El recorte de papel chino</strong> (剪纸, Jiǎnzhǐ) es uno de los '
    'arte populares más queridos y antiguos de China, con orígenes que se remontan '
    'al siglo VI d.C. Usando solo papel y tijeras o cuchillos, los artesanos crean '
    'diseños intrincados — flores, dragones, personajes y escenas — que cuentan '
    'historias de prosperidad, felicidad y buena fortuna.</p>'
    '<h3>Historia y orígenes</h3>'
    '<p>El recorte de papel surgió poco después de la invención del papel durante '
    'la dinastía Han (206 a.C. – 220 d.C.). Inicialmente utilizado en rituales '
    'religiosos y como ofrendas decorativas, esta forma de arte se extendió '
    'ampliamente durante las dinastías Ming y Qing, convirtiéndose en una parte '
    'integral de las celebraciones chinas y la vida cotidiana. En 2009, el recorte '
    'de papel chino (Jianzhi) fue inscrito en la Lista Representativa del '
    'Patrimonio Cultural Inmaterial de la Humanidad de la UNESCO.</p>'
    '<h3>Simbolismo y significados</h3>'
    '<p>Cada motivo en el recorte de papel chino tiene un profundo significado '
    'simbólico. <strong>Los dragones</strong> (龙) simbolizan poder, fuerza y '
    'buena fortuna. <strong>Las peonías</strong> (牡丹) representan riqueza y '
    'honor. <strong>Los peces</strong> (鱼) significan excedente y abundancia — '
    'la palabra 鱼 (yú) suena como 余 (yú), que significa "excedente." '
    '<strong>Los murciélagos</strong> (蝠, fú) son juegos de palabras con '
    '福 (fú), que significa felicidad y bendiciones. <strong>El fénix</strong> '
    '(凤) representa gracia y virtud.</p>'
    '<h3>Estilos regionales</h3>'
    '<p>El recorte de papel chino varía drásticamente según la región. '
    '<strong>El norte de China</strong> prefiere diseños audaces y exagerados '
    'con líneas fuertes — el estilo norteño es decorativo y narrativo. '
    '<strong>El sur de China</strong>, especialmente Fujian y Guangdong, produce '
    'trabajos más finos e intrincados con detalles delicados. El recorte de papel '
    'del <strong>sur de Jiangsu</strong> se considera entre los mejores del mundo, '
    'conocido por su refinada precisión.</p>'
    '<h3>Recorte de papel en la China moderna</h3>'
    '<p>Hoy en día, el Jianzhi sigue siendo un arte vivo y vibrante. Durante el '
    'Año Nuevo chino (春节), se pegan recortes de papel rojo con símbolos de '
    'buena suerte en ventanas y puertas de toda China. En las bodas, los símbolos '
    'de doble felicidad (囍) aparecen por todas partes. Los recortes de papel '
    'también son populares como regalos, souvenirs y en instalaciones artísticas. '
    'Los visitantes pueden encontrar talleres de recorte de papel en los hutongs '
    'de Beijing, la ciudad antigua de Xi\'an y en pueblos artesanales de todo '
    'el país.</p>'
)

# 1. Replace the body content (the longDescLanguage div content)
# The old body content is the English one
old_body_pattern = (
    r'(<div id="city-content" class="prose text-gray-700" data-lang-key="longDescLanguage">)'
    r'.*?(</div>\s*\n\s*</div>\s*\n\s*</article>)'
)

def replace_body(match):
    return match.group(1) + spanish_longdesc + match.group(2)

new_content = re.sub(old_body_pattern, replace_body, content, flags=re.DOTALL)

if new_content == content:
    print("WARNING: No body content replaced!")
else:
    print("Body content replaced successfully.")

# 2. Add longDescLanguage to the window.translations JSON
# Find the descLanguage entry and add longDescLanguage after it
# First, escape the spanish_longdesc for JSON
escaped_longdesc = spanish_longdesc.replace('\\', '\\\\').replace('"', '\\"')

# Find descLanguage in the translations JSON and add longDescLanguage after it
# Pattern: "descLanguage":"value",
pattern_desc = r'("descLanguage":"[^"]*")'
replacement_desc = r'\1,\n"longDescLanguage":"' + escaped_longdesc + '"'

new_content = re.sub(pattern_desc, replacement_desc, new_content, count=1)

if pattern_desc in content and new_content == content:
    print("WARNING: descLanguage not replaced!")
else:
    print("descLanguage replacement attempted.")

# 3. Also update descLanguage from English to Spanish
old_desc = '"descLanguage":"Mandarin, Characters & Sinoxenic Languages"'
new_desc = '"descLanguage":"Mandarín, caracteres e idiomas sinoxénicos"'
new_content = new_content.replace(old_desc, new_desc)

if old_desc not in content:
    # Try without the ampersand encoding
    old_desc_alt = '"descLanguage":"Mandarin, Characters & Sinoxenic Languages"'
    new_content = new_content.replace(old_desc_alt, new_desc)

# Write the file
with open('es/language.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("File written successfully.")