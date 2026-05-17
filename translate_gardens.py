#!/usr/bin/env python3
"""Translate gardens.html longDescGardens from EN to zh-CN."""
import re
import json

EN_BODY = """<p><strong>Chinese classical gardens</strong> (园林, yuánlín) are masterpieces of landscape design that blend architecture, water features, vegetation, and poetic conception into spaces of extraordinary beauty and philosophical meaning. With a history spanning over a thousand years, they represent one of China's most refined art forms.</p><h3>History &amp; Philosophy</h3><p>Chinese garden tradition dates to the Han Dynasty (206 BCE – 220 CE), when emperors built imperial retreats inspired by Taoist mythology and the ideal of harmony between humans and nature. The Song Dynasty saw the development of scholar's gardens (文人园), where literati created private spaces for contemplation, poetry, and artistic pursuit.</p><p>The Ming and Qing Dynasties witnessed the golden age of classical garden creation, particularly in Suzhou, where dozens of masterpieces were built by scholar-officials who designed gardens as expressions of their worldview — embodying principles of duality, borrowed scenery, and spatial compression.</p><h3>UNESCO World Heritage Gardens</h3><ul><li><strong>Humble Administrator's Garden (拙政园)</strong> in Suzhou — the largest and most celebrated, featuring a lotus pond, Zigzag Bridge, and the Orchid Pavilion.</li><li><strong>Lingering Garden (留园)</strong> in Suzhou — renowned for its sophisticated use of space, rockeries, and architectural elegance.</li><li><strong>Master of the Nets Garden (网师园)</strong> in Suzhou — a masterpiece of compact design and subtle beauty.</li><li><strong>Summer Palace (颐和园)</strong> in Beijing — the grandest imperial garden, centered on Kunming Lake and Longevity Hill.</li></ul><h3>Garden Design Principles</h3><ul><li><strong>Borrowed scenery (借景)</strong> — incorporating surrounding landscapes into the garden's views.</li><li><strong>Shan shui (山水)</strong> — the interplay of mountains (shan) and water (shui) as the garden's core elements.</li><li><strong>Pseudo-randomness (假山)</strong> — rockeries designed to appear naturally irregular.</li><li><strong>Framing</strong> — windows and doorways shaped as poem-slides (诗框) to create curated views.</li></ul><h3>Penjing: The Art of Potted Landscapes</h3><p>Closely related to classical gardens is <em>penjing</em> (盆景) — the cultivation of miniature landscapes in containers. Like gardens, penjing seeks to capture the essence of nature in a bounded space, compressing mountains, water, and trees into a single artistic composition.</p>"""

ZH_BODY = """<p><strong>中国古典园林</strong>（yuánlín）是景观设计的杰作，将建筑、水景、植被和诗意构思融合成具有非凡美感和哲学意义的空间。拥有一千多年的历史，它们代表了中国最精致的艺术形式之一。</p><h3>历史与哲学</h3><p>中国园林传统可追溯至汉朝（公元前206年–公元220年），当时皇帝们受道家神话和人与自然和谐理念的启发，建造了皇家行宫。宋朝出现了文人园的发展，文人雅士创建了用于沉思、诗歌和艺术追求的私密空间。</p><p>明清时期见证了古典园林创作的黄金时代，尤其在苏州，数十座杰作由士大夫建造——他们将园林设计为世界观的表达，体现了阴阳平衡、借景和空间压缩的原则。</p><h3>联合国教科文组织世界遗产园林</h3><ul><li><strong>拙政园</strong>（Humble Administrator's Garden）— 苏州最大且最著名的园林，以荷花池、九曲桥和兰雪堂为特色。</li><li><strong>留园</strong>（Lingering Garden）— 苏州，以精巧的空间运用、假山和建筑优雅而闻名。</li><li><strong>网师园</strong>（Master of the Nets Garden）— 苏州，紧凑设计和含蓄之美的杰作。</li><li><strong>颐和园</strong>（Summer Palace）— 北京，最宏伟的皇家园林，以昆明湖和万寿山为中心。</li></ul><h3>园林设计原则</h3><ul><li><strong>借景</strong>（Borrowed scenery）— 将周围的景观引入园林视野中。</li><li><strong>山水</strong>（Shan shui）— 山与水作为园林核心元素的相互作用。</li><li><strong>假山</strong>（Pseudo-randomness）— 设计成自然不规则的岩石景观。</li><li><strong>框景</strong>（Framing）— 将门窗塑造成诗框，营造精心设计的景观视图。</li></ul><h3>盆景：盆栽景观的艺术</h3><p>与古典园林密切相关的是<em>盆景</em>（penjing）——在容器中培育微型景观。与园林一样，盆景力求在有限的空间中捕捉自然的精髓，将山、水和树木浓缩成单一的艺术构图。</p>"""

ZH_DESC = "探索中国园林设计的艺术——从苏州被联合国教科文组织列入名录的古典园林到皇家行宫和古老的盆景传统。"

# Read the zh-CN file
with open('zh-CN/gardens.html', 'r') as f:
    content = f.read()

# 1. Update the body content (city-content div)
old_body_pattern = r'(data-lang-key="longDescGardens">)(.*?)(</div>\s*</div>\s*</article>)'
new_content = re.sub(old_body_pattern, lambda m: m.group(1) + ZH_BODY + m.group(3), content, count=1, flags=re.DOTALL)

# 2. Update window.translations JSON
def update_json(match):
    raw = match.group(1)
    data = json.loads(raw)
    zh = data.get('zh-CN', {})
    zh['longDescGardens'] = ZH_BODY
    zh['descGardens'] = ZH_DESC
    data['zh-CN'] = zh
    return 'window.translations = ' + json.dumps(data, ensure_ascii=False) + ';'

new_content = re.sub(r'window\.translations\s*=\s*({.*?});', update_json, new_content, count=1, flags=re.DOTALL)

# Write back
with open('zh-CN/gardens.html', 'w') as f:
    f.write(new_content)

print("Done. Updated zh-CN/gardens.html")

# Verify
with open('zh-CN/gardens.html', 'r') as f:
    c = f.read()
m = re.search(r'window\.translations\s*=\s*({.*?});', c, re.DOTALL)
data = json.loads(m.group(1))
zh = data['zh-CN']
print(f'longDescGardens exists: {"longDescGardens" in zh}')
print(f'descGardens: {zh.get("descGardens", "MISSING")[:60]}')
print(f'longDescGardens length: {len(zh.get("longDescGardens", ""))}')