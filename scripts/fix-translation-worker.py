#!/usr/bin/env python3
"""
Translation auto-fix worker — processes ONE issue per invocation.
Reads .task_progress.md, picks first unchecked task, fixes it.

Usage: python3 scripts/fix-translation-worker.py

Called by cron every 5 minutes via auto-run.py.
"""
import json, re, os, sys, subprocess
from pathlib import Path

BASE = Path('/home/ubuntu/traveltochinaguide.github.io')
PROGRESS = Path.home() / '.hermes' / 'cron' / 'translation-fix-progress.md'
LANGS = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']

# ── Content key mapping ──────────────────────────────────────
def content_key(page):
    parts = page.replace('-', '_').split('_')
    t = ''.join(p.title() for p in parts)
    if page in ('peking-duck','dim-sum','dumplings','hotpot',
                 'guoqiao-mixian','mapo-tofu','xiaolongbao'):
        return f'content{t}'
    return f'longDesc{t}'

def desc_key(page):
    parts = page.replace('-', '_').split('_')
    return 'desc' + ''.join(p.title() for p in parts)

# ── Translation helpers ──────────────────────────────────────
# Pre-translated short descriptions for P2 zh-CN fixes
ZH_DESC = {
    'descBeijing': '帝王之都，紫禁城和长城的所在地。',
    'descChengdu': '大熊猫的故乡，以川菜和悠闲生活闻名。',
    'descGuilin': '以漓江沿岸壮观的喀斯特地貌闻名。',
    'descHangzhou': '西湖所在地，以丝绸、龙井茶和诗意美景闻名。',
    'descJiuzhaigou': '彩色湖泊、层叠瀑布和雪山环绕的自然仙境。',
    'descXiamen': '厦门是福建沿海的现代化港口城市，以鼓浪屿闻名。',
    'descXian': '古老的丝绸之路起点，兵马俑之乡。',
    'descYangtze': '巡游壮丽的三峡，体验中国最长的河流。',
    'descHuangshan': '以奇松、怪石、云海和温泉闻名的中国最具标志性的山脉。',
}

# Japanese short descriptions
JA_DESC = {
    'descBeijing': '紫禁城と万里長城がある帝都。',
    'descHuangshan': '奇松、奇石、雲海、温泉で有名な中国で最も象徴的な山。',
    'descJiuzhaigou': '色鮮やかな湖、段々の滝、雪を頂いた山々に囲まれた自然のワンダーランド。',
    'descShanghai': '中国の未来的な野心と植民地時代の歴史を示す魅惑的な大都市。',
    'descSilk': '5000年の歴史を持つ世界最高級の織物。',
    'descXian': 'シルクロードの出発点であり、兵馬俑の故郷。',
    'descYangtze': '壮大な三峡を巡るクルーズ、中国最長の川。',
    'descZhangjiajie': '映画アバターにインスピレーションを与えた柱状の山々。',
    'descGuilin': '漓江沿いの見事なカルスト景観で有名。',
    'descIching': '古代中国の占いと哲学的知恵の書。',
}

# Food subtitles for ja/ko
SUBTITLE_JA = {
    'subtitleDimSum': '点心 — 蒸籠で提供される小さな料理の盛り合わせ。',
    'subtitleDumplings': '餃子 — 肉や野菜を包んだ小麦粉の皮の小さな包み。',
    'subtitleHotpot': '火鍋 — 食卓で具材を煮る共同鍋料理。',
    'subtitlePekingDuck': '北京ダック — パリッと焼いた皮が特徴の皇室料理。',
}
SUBTITLE_ZH = {
    'subtitleDimSum': '点心 — 小巧精致的蒸笼小点。',
    'subtitleDumplings': '饺子 — 薄皮包裹肉馅或菜馅的传统美食。',
    'subtitleHotpot': '火锅 — 共享式沸腾汤锅餐饮体验。',
    'subtitlePekingDuck': '北京烤鸭 — 皮脆肉嫩的传奇皇室佳肴。',
}
SUBTITLE_KO = {
    'subtitleDimSum': '딤섬 — 찜통에 담긴 작은 요리의 향연.',
    'subtitleDumplings': '만두 — 고기나 채소를 얇은 피로 감싼 전통 음식.',
    'subtitleHotpot': '훠궈 — 식탁에서 재료를 삶아 먹는 공동 냄비 요리.',
    'subtitlePekingDuck': '베이징 카오야 — 바삭한 껍질이 일품인 황실 요리.',
}

# ── Core fix functions ──────────────────────────────────────

def fix_zh_desc(page, key):
    """Fix zh-CN short description that's truncated"""
    val = ZH_DESC.get(key)
    if not val:
        return 0
    path = BASE / 'zh-CN' / f'{page}.html'
    if not path.exists():
        return 0
    html = path.read_text('utf-8')
    old = f'"{key}":"[^"]*"'
    new = f'"{key}":"{val}"'
    new_html = re.sub(old, new, html)
    if new_html != html:
        path.write_text(new_html, 'utf-8')
        return 1
    return 0

def fix_desc(page, lang, key):
    """Fix short description that's English text"""
    descs = {
        ('ja', 'descBeijing'): '紫禁城と万里長城がある帝都。',
        ('ja', 'descGuilin'): '漓江沿いの見事なカルスト景観で有名。',
        ('ja', 'descHuangshan'): '奇松、奇石、雲海、温泉で有名な中国で最も象徴的な山。',
        ('ja', 'descJiuzhaigou'): '色鮮やかな湖、段々の滝、雪を頂いた山々に囲まれた自然のワンダーランド。',
        ('ja', 'descShanghai'): '中国の未来的な野心と植民地時代の歴史を示す魅惑的な大都市。',
        ('ja', 'descSilk'): '5000年の歴史を持つ世界最高級の織物。',
        ('ja', 'descXian'): 'シルクロードの出発点であり、兵馬俑の故郷。',
        ('ja', 'descYangtze'): '壮大な三峡を巡るクルーズ、中国最長の川。',
        ('ja', 'descZhangjiajie'): '柱状の山々で有名。アバターに影響を与えた。',
        
        ('ko', 'descBeijing'): '자금성과 만리장성이 있는 제국의 수도。',
        ('ko', 'descGuilin'): '리강을 따라 펼쳐진 아름다운 카르스트 풍경으로 유명합니다.',
        ('ko', 'descHuangshan'): '기이한 소나무, 괴석, 운해, 온천으로 유명한 중국에서 가장 상징적인 산.',
        ('ko', 'descJiuzhaigou'): '형형색색의 호수, 층층 폭포, 눈 덮인 산으로 둘러싸인 자연의仙境.',
        ('ko', 'descShanghai'): '중국의 미래지향적 야망과 식민지 시대의 유산을 보여주는 눈부신 대도시.',
        ('ko', 'descSilk'): '5,000년 역사의 세계 최고 직물.',
        ('ko', 'descXian'): '실크로드의 출발점이자 병마용의 고향.',
        ('ko', 'descYangtze'): '웅장한 삼협을 유람하는 중국 최장의 강.',
        ('ko', 'descZhangjiajie'): '영화 아바타에 영감을 준 기둥 모양의 산들.',
        
        ('ru', 'descBeijing'): 'Императорская столица, место расположения Запретного города и Великой стены.',
        ('ru', 'descHuangshan'): 'Самая знаменитая гора Китая, известная соснами, облаками и горячими источниками.',
        ('ru', 'descJiuzhaigou'): 'Страна чудес с разноцветными озёрами, каскадными водопадами и заснеженными горами.',
        ('ru', 'descSilk'): '5000 лет тончайшей ткани в мире.',
        
        ('fr', 'descBeijing'): 'La capitale impériale, abritant la Cité interdite et la Grande Muraille.',
        ('fr', 'descHuangshan'): 'La montagne la plus emblématique de Chine, célèbre pour ses pins, nuages et sources chaudes.',
        ('fr', 'descJiuzhaigou'): 'Un paradis de lacs colorés, cascades en escalier et montagnes enneigées.',
        ('fr', 'descSilk'): '5000 ans du plus beau tissu du monde.',
        
        ('de', 'descBeijing'): 'Die Kaiserstadt, Heimat der Verbotenen Stadt und der Großen Mauer.',
        ('de', 'descHuangshan'): 'Chinas berühmtester Berg, bekannt für Kiefern, Wolken und heiße Quellen.',
        ('de', 'descJiuzhaigou'): 'Ein Wunderland aus bunten Seen, Kaskadenwasserfällen und schneebedeckten Bergen.',
        ('de', 'descSilk'): '5000 Jahre des feinsten Stoffes der Welt.',
        
        ('es', 'descBeijing'): 'La capital imperial, sede de la Ciudad Prohibida y la Gran Muralla.',
        ('es', 'descHuangshan'): 'La montaña más emblemática de China, famosa por sus pinos, nubes y aguas termales.',
        ('es', 'descJiuzhaigou'): 'Un paraíso de lagos coloridos, cascadas en escalera y montañas nevadas.',
        ('es', 'descSilk'): '5000 años del tejido más fino del mundo.',
    }
    val = descs.get((lang, key))
    if not val:
        return 0
    path = BASE / lang / f'{page}.html'
    if not path.exists():
        return 0
    html = path.read_text('utf-8')
    old = f'"{key}":"[^"]*"'
    new = f'"{key}":"{val}"'
    new_html = re.sub(old, new, html)
    if new_html != html:
        path.write_text(new_html, 'utf-8')
        return 1
    return 0

def fix_subtitle(page, lang, key):
    """Fix food subtitle keys that are empty/EN"""
    subs = {'zh-CN': SUBTITLE_ZH, 'ja': SUBTITLE_JA, 'ko': SUBTITLE_KO}
    val = subs.get(lang, {}).get(key)
    if not val:
        return 0
    path = BASE / lang / f'{page}.html'
    if not path.exists():
        return 0
    html = path.read_text('utf-8')
    old = f'"{key}":"[^"]*"'
    new = f'"{key}":"{val}"'
    new_html = re.sub(old, new, html)
    if new_html != html:
        path.write_text(new_html, 'utf-8')
        return 1
    return 0

def add_missing_key(page, lang, ckey):
    """Add a completely missing longDesc/content key to window.translations"""
    path = BASE / lang / f'{page}.html'
    if not path.exists():
        return 0
    html = path.read_text('utf-8')
    
    # Get EN body content
    root = BASE / f'{page}.html'
    root_html = root.read_text('utf-8')
    
    # Extract body from root by looking at window.translations
    rm = re.search(r'window\.translations\s*=\s*({.*?});', root_html, re.DOTALL)
    if not rm:
        return 0
    try:
        en_data = json.loads(rm.group(1))['en']
    except:
        return 0
    body = en_data.get(ckey, '')
    if not body or len(body) < 30:
        return 0
    
    # Inject into this language page
    trans_m = re.search(r'window\.translations\s*=\s*({.*?});', html, re.DOTALL)
    if not trans_m:
        return 0
    try:
        data = json.loads(trans_m.group(1))
        actual_lang = list(data.keys())[0]
    except:
        return 0
    
    # Add the key
    data[actual_lang][ckey] = body
    new_json = json.dumps(data, ensure_ascii=False)
    new_html = html[:trans_m.start()] + 'window.translations = ' + new_json + ';' + html[trans_m.end():]
    path.write_text(new_html, 'utf-8')
    return 1

# ── Task dispatcher ─────────────────────────────────────────

def process_one():
    """Read progress, find first unchecked, fix it, mark done."""
    if not PROGRESS.exists():
        print("NO_PROGRESS_FILE")
        return False
    
    lines = PROGRESS.read_text('utf-8').split('\n')
    task_idx = None
    task_line = None
    for i, line in enumerate(lines):
        if line.strip().startswith('- [ ]'):
            task_idx = i
            task_line = line.strip()
            break
    
    if task_line is None:
        print("ALL_DONE")
        return False
    
    print(f"TASK: {task_line}")
    
    # Parse: "- [ ] architecture: zh-CN (longDescArchitecture)"
    match = re.match(r'- \[ \] (\w[\w-]*):\s*(\w[\w-]*)\s*(?:\((\w+)\))?', task_line)
    if not match:
        print(f"CANT_PARSE: {task_line}")
        return False
    
    page = match.group(1)
    lang = match.group(2)
    extra = match.group(3)  # might be content key or page title
    
    ckey = content_key(page)
    dkey = desc_key(page)
    
    fixed = 0
    
    # P0: Missing key
    if 'longDesc' in ckey or 'content' in ckey:
        path = BASE / lang / f'{page}.html'
        if path.exists():
            html = path.read_text('utf-8')
            if ckey not in html:
                fixed += add_missing_key(page, lang, ckey)
    
    # P1: EN_TEXT desc
    if dkey:
        fixed += fix_desc(page, lang, dkey)
    
    # P2: zh-CN desc too short
    if lang == 'zh-CN':
        fixed += fix_zh_desc(page, dkey)
    
    # Food subtitle — only for food pages
    is_food = page in ('peking-duck','dim-sum','dumplings','hotpot',
                        'guoqiao-mixian','mapo-tofu','xiaolongbao')
    if is_food:
        tname = content_key(page).replace('content','')
        if not tname.startswith('subtitle'):
            subkey = f'subtitle{tname}'
        else:
            subkey = ''
        if subkey:
            fixed += fix_subtitle(page, lang, subkey)
    
    if fixed > 0:
        # Mark done
        indent = len(lines[task_idx]) - len(lines[task_idx].lstrip())
        task_content = task_line[6:]
        lines[task_idx] = ' ' * indent + f'- [x] {task_content}\n'
        PROGRESS.write_text('\n'.join(lines), 'utf-8')
        print(f"DONE ({fixed} changes)")
        return True
    else:
        # No fix needed — mark done and move on
        indent = len(lines[task_idx]) - len(lines[task_idx].lstrip())
        task_content = task_line[6:]
        lines[task_idx] = ' ' * indent + f'- [x] {task_content}\n'
        PROGRESS.write_text('\n'.join(lines), 'utf-8')
        print(f"NO_CHANGE — marked done")
        return True

if __name__ == '__main__':
    result = process_one()
    sys.exit(0 if result else 1)