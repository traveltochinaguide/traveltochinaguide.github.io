import re

# Read the file
with open('ko/paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the body content in city-content div for longDescPaper
old_body = '''<div id="city-content" class="prose text-gray-700" data-lang-key="longDescPaper"><p><strong>Chinese paper cutting</strong> (剪纸, Jiǎnzhǐ) is one of China's most beloved and oldest folk arts, with origins dating back to the 6th century CE. Using only paper and scissors or knives, artisans create intricate designs — flowers, dragons, characters, and scenes — that tell stories of prosperity, happiness, and good fortune.</p><h3>History & Origins</h3><p>Paper cutting emerged shortly after the invention of paper during the Han Dynasty (206 BCE – 220 CE). Initially used in religious rituals and as decorative offerings, the art form spread widely during the Ming and Qing dynasties, becoming an integral part of Chinese celebrations and daily life. In 2009, Chinese paper cutting (Jianzhi) was inscribed on the UNESCO Representative List of the Intangible Cultural Heritage of Humanity.</p><h3>Symbolism & Meanings</h3><p>Each motif in Chinese paper cutting carries deep symbolic meaning. <strong>Dragons</strong> (龙) symbolize power, strength, and good fortune. <strong>Peonies</strong> (牡丹) represent wealth and honor. <strong>Fish</strong> (鱼) signifies surplus and abundance — the word 鱼 (yú) sounds like 余 (yú), meaning "surplus." <strong>Bats</strong> (蝠, fú) are puns for 福 (fú), or happiness and blessings. <strong>Phoenix</strong> (凤) represents grace and virtue.</p><h3>Regional Styles</h3><p>Chinese paper cutting varies dramatically by region. <strong>Northern China</strong> favors bold, exaggerated designs with strong lines — the northern style is decorative and narrative. <strong>Southern China</strong>, especially Fujian and Guangdong, produces finer, more intricate work with delicate details. <strong>Southern Jiangsu</strong> paper cutting is considered among the finest in the world, known for its refined precision.</p><h3>Paper Cutting in Modern China</h3><p>Today, Jianzhi remains a vibrant living art. During Chinese New Year (春节), red paper cuttings with lucky symbols are pasted on windows and doors across China. At weddings, double-happiness (囍) symbols appear everywhere. Paper cuttings are also popular as gifts, souvenirs, and in artistic installations. Visitors can find paper cutting workshops in Beijing's hutongs, Xian's old city, and in craft villages throughout the country.</p></div>'''

new_body = '''<div id="city-content" class="prose text-gray-700" data-lang-key="longDescPaper"><p><strong>중국 종이 découpage</strong> (剪纸, Jiǎnzhǐ)은 6세기 CE까지 그 기원을 추적할 수 있는 중국에서 가장 사랑받고 오래된 민속 예술 중 하나입니다. 종이와 가위나 칼만 사용하여 장인들이 꽃, 용, 문자, 장면으로 번영, 행복, 행운의 이야기를 담은 정교한 디자인을 만들어냅니다.</p><h3>역사와 기원</h3><p>종이 découpage은 한나라(기원전 206년–220년) 시대에 종이가 발명된 직후 등장했습니다. 처음에는 종교 의식과 장식용 공물로 사용되었으며, 명청 시대에 널리 퍼져 중국 축하 행사 와 일상 생활에 없어서는 안 될 부분이 되었습니다. 2009년 중국 종이 découpage(Jianzhi)은 유네스코 인간무형문화유산 대표 목록에 등재되었습니다.</p><h3>상징과 의미</h3><p>중국 종이 découpage의 각 모티프는 깊은 상징적 의미를 담고 있습니다. <strong>용</strong>(龙)은 권력, 힘, 행운을 상징합니다. <strong>모란</strong>(牡丹)은 부와 명예를 대표합니다. <strong>물고기</strong>(鱼)는 풍요와 번영을 나타냅니다— 물고기(鱼, yú)는 잉여(余, yú)와 발음이 같아 "잉여"를 의미합니다. <strong>박쥐</strong>(蝠, fú)는 福(복, fú)의 말장난으로 행복과 축복을 뜻합니다. <strong>봉황</strong>(凤)은 우아함과 덕을 상징합니다.</p><h3>지역 양식</h3><p>중국 종이 découpage은 지역에 따라 현저하게 다릅니다. <strong>중국 북부</strong>는 강하고 장식적인 내러티브 양식의 강렬한 선이 있는 과장된 디자인을 선호합니다. <strong>중국 남부</strong>, 특히 푸젠과 광둥은 섬세한 디테일의 더 섬세고 정교한 작품을 생산합니다. <strong>남부 장쑤</strong> 종이 découpage은 정제된 정밀도로 인해 세계에서 가장 섬세한 것으로 간주됩니다.</p><h3>현대 중국의 종이 découpage</h3><p>오늘날 Jianzhi는 여전히 활기찬 생생한 예술입니다. 중국 신춘절(春节)에는 행운의 상징이 담긴 빨간 종이 découpage이 중국 전역의 창문과 문에 붙여집니다. 결혼식에서는 双喜(囍) 기호가 어디든 나타납니다. 종이 découpage은 선물, 기념품, 예술적 설치물로도 인기가 있습니다. 방문객은 베이징의 후통, 시안의 오래된 도시, 그리고 전국의 공예 마을에서 종이 découpage 워크숍을 찾을 수 있습니다.</p></div>'''

if old_body in content:
    content = content.replace(old_body, new_body)
    print("Body replaced successfully")
else:
    print("Body pattern not found")

# 2. Update descPaper in window.translations (currently English)
old_desc = '"descPaper":"The ancient Chinese folk art of Jianzhi paper cutting — from festival decorations to UNESCO heritage."'
new_desc = '"descPaper":"축제 장식에서 유네스코 문화유산까지, jianzhi 종이 découpage에 관한 중국 고대 민속 예술."'
content = content.replace(old_desc, new_desc)
print("descPaper translation updated")

# 3. Add longDescPaper to window.translations
if '"longDescPaper":' not in content:
    desc_match = re.search(r'"descPaper":"[^"]*",', content)
    if desc_match:
        insert_pos = desc_match.end()
        long_desc_ko = '"longDescPaper":"<p><strong>중국 종이 découpage</strong> (剪纸, Jiǎnzhǐ)은 6세기 CE까지 그 기원을 추적할 수 있는 중국에서 가장 사랑받고 오래된 민속 예술 중 하나입니다. 종이와 가위나 칼만 사용하여 장인들이 꽃, 용, 문자, 장면으로 번영, 행복, 행운의 이야기를 담은 정교한 디자인을 만들어냅니다.</p><h3>역사와 기원</h3><p>종이 découpage은 한나라(기원전 206년–220년) 시대에 종이가 발명된 직후 등장했습니다. 처음에는 종교 의식과 장식용 공물로 사용되었으며, 명청 시대에 널리 퍼져 중국 축하 행사 와 일상 생활에 없어서는 안 될 부분이 되었습니다. 2009년 중국 종이 découpage(Jianzhi)은 유네스코 인간무형문화유산 대표 목록에 등재되었습니다.</p><h3>상징과 의미</h3><p>중국 종이 découpage의 각 모티프는 깊은 상징적 의미를 담고 있습니다. <strong>용</strong>(龙)은 권력, 힘, 행운을 상징합니다. <strong>모란</strong>(牡丹)은 부와 명예를 대표합니다. <strong>물고기</strong>(鱼)는 풍요와 번영을 나타냅니다— 물고기(鱼, yú)는 잉여(余, yú)와 발음이 같아 \\"잉여\\"를 의미합니다. <strong>박쥐</strong>(蝠, fú)는 福(복, fú)의 말장난으로 행복과 축복을 뜻합니다. <strong>봉황</strong>(凤)은 우아함과 덕을 상징합니다.</p><h3>지역 양식</h3><p>중국 종이 découpage은 지역에 따라 현저하게 다릅니다. <strong>중국 북부</strong>는 강하고 장식적인 내러티브 양식의 강렬한 선이 있는 과장된 디자인을 선호합니다. <strong>중국 남부</strong>, 특히 푸젠과 광둥은 섬세한 디테일의 더 섬세고 정교한 작품을 생산합니다. <strong>남부 장쑤</strong> 종이 découpage은 정제된 정밀도로 인해 세계에서 가장 섬세한 것으로 간주됩니다.</p><h3>현대 중국의 종이 découpage</h3><p>오늘날 Jianzhi는 여전히 활기찬 생생한 예술입니다. 중국 신춘절(春节)에는 행운의 상징이 담긴 빨간 종이 découpage이 중국 전역의 창문과 문에 붙여집니다. 결혼식에서는 双喜(囍) 기호가 어디든 나타납니다. 종이 découpage은 선물, 기념품, 예술적 설치물로도 인기가 있습니다. 방문객은 베이징의 후통, 시안의 오래된 도시, 그리고 전국의 공예 마을에서 종이 découpage 워크숍을 찾을 수 있습니다.</p>"'
        content = content[:insert_pos] + long_desc_ko + ',' + content[insert_pos:]
        print("longDescPaper added to translations")
    else:
        print("Could not find descPaper position")
else:
    print("longDescPaper already exists in translations")

with open('ko/paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File written")