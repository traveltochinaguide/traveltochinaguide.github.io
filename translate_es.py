#!/usr/bin/env python3
"""Replace longDescBeijing in es/beijing.html with Spanish translation."""
import re, json

with open('es/beijing.html') as f:
    content = f.read()

# Spanish translation of longDescBeijing (all HTML tags and English proper nouns preserved)
es_long_desc = (
    '<p>Pekín, la capital de la República Popular China, es una ciudad de inmensa '
    'importancia histórica y cultural. Ha sido el centro del poder durante gran '
    'parte de la historia del país, lo que se refleja en su grandiosa arquitectura.</p>'
    '<p>Explore el vasto complejo de la Ciudad Prohibida, el antiguo palacio imperial, '
    'recorra la histórica <strong>Gran Muralla</strong> (consulte la '
    '<a href="#great-wall-tour">sección de la Gran Muralla</a> más abajo) y visite '
    'el sereno Templo del Cielo. El Pekín moderno es también un centro de arte, '
    'gastronomía y comercio, que ofrece una combinación dinámica de lo antiguo y lo nuevo.</p>'
    '<h3 id="great-wall-tour" class="text-xl font-semibold mt-6 mb-2">'
    'Tour de la Gran Muralla desde Pekín – Mutianyu y Badaling</h3>'
    '<p>El <strong>tour de la Gran Muralla desde Pekín</strong> es la excursión '
    'de un día más popular desde la ciudad. Las opciones típicas incluyen traslados '
    'privados, autobuses lanzadera compartidos y excursiones guiadas a '
    '<strong>Mutianyu</strong> (pendientes suaves y secciones restauradas) o '
    '<strong>Badaling</strong> (acceso más fácil e instalaciones para visitantes). '
    'Los tours van desde medio día hasta un día completo y a menudo incluyen '
    'opciones de teleférico o tobogán.</p>'
    '<p><strong>Duración:</strong> 4–6 horas según el destino y el transporte. '
    '<strong>Cómo reservar:</strong> Reserve a través de operadores turísticos '
    'locales, plataformas de reserva de confianza o la conserjería de su hotel. '
    'Para una experiencia más tranquila, elija Mutianyu entre semana; para la '
    'experiencia clásica, elija Badaling temprano por la mañana.</p>'
    '<figure class="mt-4"> <img src="/images/attr-great-wall-detail.jpg" '
    'alt="Tour de la Gran Muralla desde Pekín – sección Mutianyu" width="1200" '
    'height="675" class="w-full h-auto rounded" loading="lazy"> '
    '<figcaption class="text-sm text-gray-500 mt-2">Tour de la Gran Muralla '
    'desde Pekín: sección Mutianyu – recomendado para familias y fotógrafos.</figcaption></figure>'
    '<h3 id="798-art-zone" class="text-xl font-semibold mt-6 mb-2">'
    'Zona de Arte 798 (Dashanzi)</h3>'
    '<p>La <strong>Zona de Arte 798</strong>, o Distrito de Arte Dashanzi, '
    'es un vibrante centro de arte contemporáneo chino. Ubicado en antiguas '
    'fábricas militares desmanteladas construidas con un estilo único de '
    'influencia Bauhaus, es un laberinto de galerías, estudios, boutiques y '
    'cafeterías. Es una visita obligada para los amantes del arte moderno, '
    'ofreciendo una mirada a la escena creativa de Pekín. Dedique de 3 a 4 '
    'horas para explorarlo.</p>'
    '<figure class="mt-4"> <img src="/images/attr-798-art.jpg" '
    'alt="Galería de la Zona de Arte 798" width="1200" height="675" '
    'class="w-full h-auto rounded" loading="lazy"> '
    '<figcaption class="text-sm text-gray-500 mt-2">Una galería en la Zona '
    'de Arte 798 de Pekín.</figcaption></figure>'
    '<h3 class="text-xl font-semibold mt-6 mb-2">Cómo llegar</h3>'
    '<p><strong>En avión:</strong> Pekín Capital (PEK) y Pekín Daxing (PKX) '
    'atienden vuelos internacionales. Desde los aeropuertos use el tren expreso '
    'del aeropuerto, taxis o Didi (servicio de transporte).</p>'
    '<p><strong>En tren:</strong> Pekín tiene múltiples estaciones (Pekín Sur, '
    'Pekín Oeste, Estación de Pekín) que conectan servicios de alta velocidad '
    'desde toda China.</p>'
    '<h3 class="text-xl font-semibold mt-6 mb-2">Mejor época para visitar</h3>'
    '<p>La primavera (abril–mayo) y el otoño (septiembre–octubre) ofrecen un '
    'clima agradable y cielos más despejados. Los inviernos pueden ser muy '
    'fríos; los veranos son calurosos y húmedos.</p>'
    '<h3 class="text-xl font-semibold mt-6 mb-2">Cómo moverse</h3>'
    '<ul><li><strong>Metro:</strong> Extenso, económico y eficiente. Obtenga '
    'una tarjeta de transporte (Yikatong) o use pagos móviles.</li>'
    '<li><strong>Taxi / Didi:</strong> Ampliamente disponibles. Tenga su '
    'destino escrito en chino para los conductores.</li>'
    '<li><strong>A pie / bicicleta:</strong> Los Hutongs y algunas zonas de '
    'parques se exploran mejor a pie.</li></ul>'
    '<h3 class="text-xl font-semibold mt-6 mb-2">Itinerarios sugeridos</h3>'
    '<p><strong>1 día:</strong> Ciudad Prohibida – Plaza de Tiananmen – '
    'Templo del Cielo – Paseo por los Hutongs por la noche.</p>'
    '<p><strong>3 días:</strong> Día 1: Ciudad Prohibida + Tiananmen + '
    'Wangfujing; Día 2: Excursión de un día a la Gran Muralla (Mutianyu); '
    'Día 3: Palacio de Verano + Templo del Cielo + Hutongs.</p>'
    '<h3 class="text-xl font-semibold mt-6 mb-2">Consejos prácticos</h3>'
    '<ul><li>Efectivo y pago móvil: Alipay/WeChat Pay son ampliamente '
    'utilizados; muchos lugares aceptan tarjetas en grandes hoteles y '
    'atracciones.</li>'
    '<li>Visa: Verifique las reglas de la embajada antes de viajar.</li>'
    '<li>Calidad del aire: Consulte el AQI y planifique actividades al aire '
    'libre cuando el aire esté más limpio.</li>'
    '<li>Emergencias: Marque <strong>110</strong> para la policía, '
    '<strong>120</strong> para ambulancia, <strong>119</strong> para bomberos '
    'en China.</li>'
    '<li>Idioma: La señalización en inglés es común en las principales '
    'atracciones, pero aprenda algunas frases en chino o use aplicaciones de '
    'traducción.</li></ul>'
)

# Extract the JSON
m = re.search(r'window\.translations\s*=\s*({.*?});', content, re.DOTALL)
if not m:
    print("ERROR: Could not find window.translations")
    exit(1)

data = json.loads(m.group(1))

# Update the Spanish longDesc
data['es']['longDescBeijing'] = es_long_desc

# Re-serialize the JSON
new_json = json.dumps(data, ensure_ascii=False, indent=2)

# Replace in the file - but we need to be careful with the old content
old_raw = m.group(1)
# Replace the old JSON with new one in the content
new_content = content.replace(old_raw, new_json)

with open('es/beijing.html', 'w') as f:
    f.write(new_content)

print("DONE: es/beijing.html updated")

# Verify
with open('es/beijing.html') as f:
    content2 = f.read()
m2 = re.search(r'window\.translations\s*=\s*({.*?});', content2, re.DOTALL)
if m2:
    data2 = json.loads(m2.group(1))
    val = data2['es']['longDescBeijing']
    print(f"New ES longDesc length: {len(val)} chars")
    print(f"Starts with: {val[:80]}...")
    print(f"Contains Spanish? {'Pekín' in val}")