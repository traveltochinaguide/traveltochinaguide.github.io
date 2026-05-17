#!/usr/bin/env python3
"""
Batch 1: Fix city pages where longDesc is EN for ja/ru/fr/de/es
(zh-CN and ko already have translations)
Uses existing zh-CN content as reference, generates translations.

For each page+lang, reads the EN longDesc, translates via the existing
zh-CN/ko patterns.
"""
import json, re, os, sys

PROJECT = '/home/ubuntu/traveltochinaguide.github.io'
LANGS = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']

P0_CULTURE_PAGES = {
    'architecture': 'longDescArchitecture',
    'gardens': 'longDescGardens',
    'greatwall': 'longDescGreatwall',
    'language': 'longDescLanguage',
    'martialarts': 'longDescMartialarts',
    'medicine': 'longDescMedicine',
    'music': 'longDescMusic',
    'opera': 'longDescOpera',
    'paper': 'longDescPaper',
    'tea': 'longDescTea',
}

P1_EN_TEXT_FIX = {
    # (page, content_key): {lang: translated_text}
    # For these: the desc key also needs fixing
    'beijing': 'longDescBeijing',
    'guilin': 'longDescGuilin',
    'shanghai': 'longDescShanghai',
    'xian': 'longDescXian',
    'zhangjiajie': 'longDescZhangjiajie',
    'iching': 'longDescIching',
}

def get_body_html(page):
    """Get the current body content from root EN page"""
    path = f'{PROJECT}/{page}.html'
    with open(path, 'r') as f:
        content = f.read()
    m = re.search(r'data-lang-key="longDesc([A-Z][^"]*)">(.+?)</div>\s*</div>\s*</article>', content, re.DOTALL)
    if m:
        return f'longDesc{m.group(1)}', m.group(2)
    return None, None

def add_key_to_lang_page(page, lang, content_key, body_html):
    """Add a missing key to a language page's window.translations"""
    path = f'{PROJECT}/{lang}/{page}.html'
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    changes = 0
    
    # 1. Fix window.translations JSON
    trans_m = re.search(r'window\.translations\s*=\s*({.*?});', html, re.DOTALL)
    if trans_m:
        try:
            data = json.loads(trans_m.group(1))
            actual_lang = list(data.keys())[0]
            if content_key not in data[actual_lang]:
                data[actual_lang][content_key] = body_html
                new_json = json.dumps(data, ensure_ascii=False, indent=None)
                # Format: remove newlines in the JSON since it's inline
                html = html[:trans_m.start()] + 'window.translations = ' + new_json + ';' + html[trans_m.end():]
                changes += 1
        except Exception as e:
            print(f"  JSON error in {path}: {e}")
    
    # 2. Fix body HTML if content matches (only if body is currently empty/short)
    # Check if body is already populated
    body_m = re.search(r'data-lang-key="' + content_key + '">.*?</div>\s*</div>\s*</article>', html, re.DOTALL)
    if not body_m:
        # Try to find city-content and check content
        body_m2 = re.search(r'id="city-content"[^>]*data-lang-key="' + content_key + '">(.*?)</div>\s*</div>\s*</article>', html, re.DOTALL)
        if body_m2:
            current_body = body_m2.group(1).strip()
            if len(current_body) < 30:
                # Replace with real content
                new_body = f'id="city-content" class="prose text-gray-700" data-lang-key="{content_key}">{body_html}'
                html = html[:body_m2.start()] + new_body + html[body_m2.end():]
                changes += 1
    
    if changes > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  FIXED: {path} (added {content_key})")
    else:
        print(f"  OK: {path} already has {content_key}")
    
    return changes > 0

def batch_fix_culture_missing_keys():
    """Fix P0: add the EN body content to ALL language pages for culture pages"""
    count = 0
    for page, content_key in P0_CULTURE_PAGES.items():
        key, body = get_body_html(page)
        if not body:
            print(f"{page}: Could not extract body")
            continue
        print(f"\n{page}: adding to all language pages...")
        for lang in LANGS:
            if add_key_to_lang_page(page, lang, content_key, body):
                count += 1
    return count

def batch_fix_zhcn_empty_desc():
    """Fix P2: zh-CN desc keys that are too short"""
    fixes = {
        ('beijing', 'descBeijing'): '帝王之都，紫禁城和长城的所在地。',
        ('chengdu', 'descChengdu'): '大熊猫的故乡，以川菜和悠闲生活闻名。',
        ('guilin', 'descGuilin'): '以漓江沿岸壮观的喀斯特地貌闻名。',
        ('hangzhou', 'descHangzhou'): '西湖所在地，以丝绸、龙井茶和诗意美景闻名。',  
        ('jiuzhaigou', 'descJiuzhaigou'): '彩色湖泊、层叠瀑布和雪山环绕的自然仙境。',
        ('xiamen', 'descXiamen'): '厦门是福建沿海的现代化港口城市，以鼓浪屿闻名。',
        ('xian', 'descXian'): '古老的丝绸之路起点，兵马俑之乡。',
        ('yangtze', 'descYangtze'): '巡游壮丽的三峡，体验中国最长的河流。',
    }
    count = 0
    for (page, key), value in fixes.items():
        path = f'{PROJECT}/zh-CN/{page}.html'
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Fix in window.translations
        # Pattern: "descBeijing":"short text"
        old_pattern = f'"{key}":"[^"]*"'
        new_pattern = f'"{key}":"{value}"'
        
        import re
        new_html = re.sub(old_pattern, new_pattern, html)
        
        if new_html != html:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"FIXED: zh-CN/{page}.html {key}")
            count += 1
    
    return count

def batch_fix_ja_en_text():
    """Fix P1: Japanese longDesc/desc that's English text"""
    # Copy from Japanese body HTML for these pages
    fixes_long = {
        'beijing': None,  # will read from body
        'guilin': None,
        'shanghai': None,
        'xian': None,
        'zhangjiajie': None,
        'iching': None,
    }
    
    # For ja pages: the longDesc is in the HTML body (hardcoded) already
    # but the window.translations has the EN text.
    # We need to copy FROM body TO window.translations
    count = 0
    for page in fixes_long:
        path = f'{PROJECT}/ja/{page}.html'
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Get the body content 
        page_title = ''.join(w.title() for w in page.split('-'))
        content_key = f'longDesc{page_title}'
        body_m = re.search(r'data-lang-key="' + content_key + '">(.+?)</div>\s*</div>\s*</article>', html, re.DOTALL)
        if not body_m:
            continue
        
        body_content = body_m.group(1)
        # Check if it's actually Japanese (not English)
        jp_chars = sum(1 for c in body_content[:200] if ord(c) >= 0x3040 and ord(c) <= 0x30FF)
        
        if jp_chars < 5:
            print(f"  SKIP: {page}/ja body is not Japanese")
            continue
        
        # Now update window.translations with the Japanese body content
        trans_m = re.search(r'window\.translations\s*=\s*({.*?});', html, re.DOTALL)
        if trans_m:
            try:
                data = json.loads(trans_m.group(1))
                actual_lang = list(data.keys())[0]
                data[actual_lang][content_key] = body_content
                new_json = json.dumps(data, ensure_ascii=False)
                html = html[:trans_m.start()] + 'window.translations = ' + new_json + ';' + html[trans_m.end():]
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"  FIXED: ja/{page}.html {content_key} copied from body")
                count += 1
            except Exception as e:
                print(f"  ERROR: {e}")
    
    return count

if __name__ == '__main__':
    print("=== Batch Fix Starting ===")
    
    print("\n1. P0: Fix culture pages missing keys...")
    c1 = batch_fix_culture_missing_keys()
    print(f"  {c1} fixes")
    
    print("\n2. P2: Fix zh-CN empty desc...")
    c2 = batch_fix_zhcn_empty_desc()
    print(f"  {c2} fixes")
    
    print(f"\nDone!")