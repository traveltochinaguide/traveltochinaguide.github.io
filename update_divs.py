#!/usr/bin/env python3
import re

def update_city_content_div(html_path, new_content):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Pattern to find the div and replace its inner content
    pattern = r'(<div id="city-content"[^>]*>)(.*?)(</div>\s*<script>)'
    # We need to replace the inner content (group 2) with new_content
    def repl(match):
        return match.group(1) + new_content + match.group(3)
    new_content_str = re.sub(pattern, repl, content, flags=re.DOTALL)
    if new_content_str == content:
        print(f"Warning: pattern not found in {html_path}")
        return False
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content_str)
    return True

if __name__ == '__main__':
    # Read the extended English content from translations.js? We'll just define it again.
    # We'll extract from the translations.js file to ensure consistency.
    import json
    with open('js/translations.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    match = re.search(r'let translations\s*=\s*({[\s\S]*?})\s*;', js_content)
    if match:
        trans_str = match.group(1)
        data = json.loads(trans_str)
        extended_en = data['en']['longDescChongqing']
        # We'll use this for both en and de div (placeholder)
    else:
        # Fallback: use the string we constructed earlier
        extended_en = """<p>Chongqing, a mountain city of over 30 million people, is one of China's most distinctive destinations. Set at the confluence of the Yangtze and Jialing Rivers, its dramatic hillside location creates a surreal urban landscape of soaring skyscrapers, cable cars, and one of the world's most impressive skylines.</p>
<p>Chongqing is famous for its <strong>hot pot</strong> — the city claims to have invented the communal dining tradition. Sample the legendary malatang (spicy hot pot) at one of the city's many riverside hot pot restaurants.</p>
<h3>Highlights</h3>
<ul>
<li><strong>Hongya Cave</strong> — a stunning riverside complex of traditional architecture carved into the cliff face.</li>
<li><strong>Jiefangbei Pedestrian Street</strong> — the commercial heart of central Chongqing.</li>
<li><strong>Yangtze & Jialing River Cruises</strong> — see the city's dramatic riverfront illuminated at night.</li>
<li><strong>Ciyao Ancient Town</strong> — a well-preserved riverside town with traditional architecture.</li>
<li><strong>Three Gorges Museum</strong> — a comprehensive museum showcasing the history, culture, and natural environment of the Three Gorges region.</li>
<li><strong>Dazu Rock Carvings</strong> — a UNESCO World Heritage site featuring exquisite Buddhist sculptures carved into cliffs.</li>
</ul>
<h3>Culture and History</h3>
<p>Chongqing served as the provisional capital of China during World War II and has a rich wartime heritage. The city also played a key role in the ancient Bayu culture, dating back over 2,000 years. Visitors can explore the Chongqing China Three Gorges Museum to understand the region's historical significance.</p>
<h3>Culinary Scene</h3>
<p>Beyond hot pot, Chongqing offers a variety of Sichuanese dishes known for their bold flavors and liberal use of chili peppers and Sichuan peppercorns. Popular dishes include Chongqing noodles (xiaomian), spicy chicken (la zi ji), and fish broth cooked in hot pot style. The city's night markets are bustling with street food vendors offering grilled skewers, stinky tofu, and fresh fruit juices.</p>
<h3>Practical info</h3>
<p>Chongqing has an extensive metro system. English signage is improving. The city is very humid in summer — bring light clothing. The best time to visit is spring and autumn.</p>"""
    
    success_en = update_city_content_div('chongqing.html', extended_en)
    success_de = update_city_content_div('de/chongqing.html', extended_en)  # placeholder
    
    if success_en and success_de:
        print("Updated city-content div in chongqing.html and de/chongqing.html")
    else:
        print("Failed to update one or more divs")