#!/usr/bin/env python3
"""
Scan all pages for translation issues and produce a categorized task list.
Run: python3 scripts/scan-all-translation-issues.py
Output: Writes .task_progress.md with categorized tasks
"""
import json, re, os
from collections import defaultdict

LANGS = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']

# Pages and their body content keys
PAGES = {
    # City pages: use longDescCityName
    'beijing': 'longDescBeijing', 'shanghai': 'longDescShanghai', 'xian': 'longDescXian',
    'guilin': 'longDescGuilin', 'chengdu': 'longDescChengdu', 'hangzhou': 'longDescHangzhou',
    'suzhou': 'longDescSuzhou', 'xiamen': 'longDescXiamen', 'huangshan': 'longDescHuangshan',
    'chongqing': 'longDescChongqing', 'guangzhou': 'longDescGuangzhou', 'shenzhen': 'longDescShenzhen',
    'kunming': 'longDescKunming', 'dali': 'longDescDali', 'lijiang': 'longDescLijiang',
    'zhangjiajie': 'longDescZhangjiajie', 'jiuzhaigou': 'longDescJiuzhaigou', 'yangtze': 'longDescYangtze',
    'nanjing': 'longDescNanjing', 'nanjiang': 'longDescNanjiang',
    # Culture pages
    'iching': 'longDescIching', 'calligraphy': 'longDescCalligraphy', 'architecture': 'longDescArchitecture',
    'gardens': 'longDescGardens', 'greatwall': 'longDescGreatwall', 'tea': 'longDescTea',
    'opera': 'longDescOpera', 'martialarts': 'longDescMartialarts', 'medicine': 'longDescMedicine',
    'music': 'longDescMusic', 'painting': 'longDescPainting', 'pottery': 'longDescPottery',
    'clothing': 'longDescClothing', 'silk': 'longDescSilk', 'paper': 'longDescPaper',
    'festivals': 'longDescFestivals', 'language': 'longDescLanguage',
    # Food pages: use contentDishName
    'peking-duck': 'contentPekingDuck', 'dim-sum': 'contentDimSum',
    'hotpot': 'contentHotpot', 'dumplings': 'contentDumplings',
    'guoqiao-mixian': 'contentGuoqiaomixian',
    'mapo-tofu': 'contentMapotofu', 'xiaolongbao': 'contentXiaolongbao',
    'nanjing': 'longDescNanjing',  # nanjiang is a food page too
}

def get_page_title(page):
    """Convert page name to title case for key naming"""
    return ''.join(w.title() for w in page.split('-'))

def check_page(page, content_key, is_food=False):
    """Check a page for issues"""
    path = f'{page}.html'
    if not os.path.exists(path):
        return []
    
    with open(path, 'r') as f:
        content = f.read()
    
    m = re.search(r'window\.translations\s*=\s*({.*?});', content, re.DOTALL)
    if not m:
        return []
    try:
        en_data = json.loads(m.group(1))['en']
    except:
        return []
    
    page_title = get_page_title(page)
    
    # Determine which keys to check
    check_keys = []
    
    if is_food:
        # Food pages: check content and subtitle keys
        check_keys = [content_key, f'subtitle{page_title}']
    else:
        # City/culture pages: check longDesc and desc keys
        check_keys = [content_key, f'desc{page_title}']
    
    issues = []
    
    for lang in LANGS:
        fname = f'{lang}/{page}.html'
        if not os.path.exists(fname):
            continue
        
        with open(fname, 'r') as f:
            lang_content = f.read()
        
        m2 = re.search(r'window\.translations\s*=\s*({.*?});', lang_content, re.DOTALL)
        if not m2:
            continue
        
        try:
            lang_data = json.loads(m2.group(1))
            actual_lang = list(lang_data.keys())[0]
            lang_trans = lang_data[actual_lang]
        except:
            continue
        
        for key in check_keys:
            en_val = en_data.get(key, '')
            lang_val = lang_trans.get(key, '')
            
            if key not in lang_trans:
                issues.append((page, lang, f'MISSING_KEY:{key}'))
                continue
            
            if not lang_val or len(lang_val.strip()) < 20:
                issues.append((page, lang, f'EMPTY:{key} ({len(lang_val)} chars)'))
                continue
            
            en_clean = re.sub(r'<[^>]+>', '', en_val).strip()[:60] if en_val else ''
            lang_clean = re.sub(r'<[^>]+>', '', lang_val).strip()[:60] if lang_val else ''
            
            if en_clean and en_clean == lang_clean:
                issues.append((page, lang, f'EN_TEXT:{key}'))
    
    return issues

# Scan all pages
all_issues = defaultdict(list)

for page, content_key in sorted(PAGES.items()):
    is_food = page in ['peking-duck', 'dim-sum', 'dumplings', 'hotpot', 'guoqiao-mixian', 'mapo-tofu', 'xiaolongbao']
    issues = check_page(page, content_key, is_food)
    for issue in issues:
        all_issues[issue[0]].append(issue)

# Output summary
print("=" * 80)
print("TRANSLATION ISSUES SCAN REPORT")
print("=" * 80)

# Group by issue type
by_type = defaultdict(lambda: defaultdict(list))
for page, page_issues in sorted(all_issues.items()):
    for pi in page_issues:
        page_name, lang, issue_type = pi
        issue_type_name = issue_type.split(':')[0]
        issue_detail = issue_type.split(':')[1] if ':' in issue_type else ''
        by_type[issue_type_name][page_name].append((lang, issue_detail))

for issue_type, pages_dict in sorted(by_type.items()):
    print(f"\n{'=' * 60}")
    print(f"TYPE: {issue_type} ({sum(len(v) for v in pages_dict.values())} occurrences)")
    print(f"{'=' * 60}")
    for page, details in sorted(pages_dict.items()):
        langs_str = ', '.join(f"{l}({d.split(':')[0] if ':' in d else d})" for l, d in details)
        print(f"  {page}: {langs_str}")

print(f"\n{'=' * 80}")
print(f"TOTAL: {sum(len(v) for v in all_issues.values())} issues across {len(all_issues)} pages")
print(f"{'=' * 80}")