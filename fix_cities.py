#!/usr/bin/env python3
import re
import os

CITY_ENTRIES = {
    'chongqing': '{"imgQuery":"chongqing cityscape,china,yangtze river","localImg":"/images/hero-chongqing.webp","nameKey":"cityChongqing","descKey":"descChongqing","longDescKey":"longDescChongqing"}',
    'dali': '{"imgQuery":"dali,erhai lake,yunnan,china","localImg":"/images/hero-dali.webp","nameKey":"cityDali","descKey":"descDali","longDescKey":"longDescDali"}',
    'guangzhou': '{"imgQuery":"cantonese,guangzhou,china","localImg":"/images/hero-guangzhou.webp","nameKey":"cityGuangzhou","descKey":"descGuangzhou","longDescKey":"longDescGuangzhou"}',
    'kunming': '{"imgQuery":"kunming,stone forest,china","localImg":"/images/hero-kunming.webp","nameKey":"cityKunming","descKey":"descKunming","longDescKey":"longDescKunming"}',
    'lijiang': '{"imgQuery":"lijiang old town,naxi,yunnan,china","localImg":"/images/hero-lijiang.webp","nameKey":"cityLijiang","descKey":"descLijiang","longDescKey":"longDescLijiang"}',
    'shenzhen': '{"imgQuery":"shenzhen skyline,china","localImg":"/images/hero-shenzhen.webp","nameKey":"cityShenzhen","descKey":"descShenzhen","longDescKey":"longDescShenzhen"}',
}

# Additional cities needed for the new city pages (chengdu, hangzhou, huangshan, suzhou, xiamen)
ADDITIONAL_ENTRIES = {
    'chengdu': '{"imgQuery":"chengdu,panda,china","localImg":"/images/hero-chengdu.webp","nameKey":"cityChengdu","descKey":"descChengdu","longDescKey":"longDescChengdu"}',
    'hangzhou': '{"imgQuery":"west lake,hangzhou,china","localImg":"/images/hero-hangzhou.webp","nameKey":"cityHangzhou","descKey":"descHangzhou","longDescKey":"longDescHangzhou"}',
    'huangshan': '{"imgQuery":"yellow mountain,huangshan,china","localImg":"/images/hero-huangshan.webp","nameKey":"cityHuangshan","descKey":"descHuangshan","longDescKey":"longDescHuangshan"}',
    'suzhou': '{"imgQuery":"garden,suzhou,china","localImg":"/images/hero-suzhou.webp","nameKey":"citySuzhou","descKey":"descSuzhou","longDescKey":"longDescSuzhou"}',
    'xiamen': '{"imgQuery":"xiamen,gulangyu,china","localImg":"/images/hero-xiamen.webp","nameKey":"cityXiamen","descKey":"descXiamen","longDescKey":"longDescXiamen"}',
}

ALL_ENTRIES = {**CITY_ENTRIES, **ADDITIONAL_ENTRIES}

# City pages that need all 18 cities
CITY_PAGES = ['beijing', 'shanghai', 'xian', 'chengdu', 'guilin', 'hangzhou', 'huangshan', 'suzhou', 'xiamen', 'zhangjiajie', 'jiuzhaigou', 'yangtze', 'chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang']

LANG_DIRS = ['', 'en', 'zh-CN', 'ja', 'ko', 'es', 'fr', 'de', 'ru']

def get_city_order():
    """Return the desired alphabetical order for new city entries."""
    return ['chongqing', 'dali', 'guangzhou', 'kunming', 'lijiang', 'shenzhen',
            'chengdu', 'hangzhou', 'huangshan', 'suzhou', 'xiamen']

def fix_file(filepath):
    """Fix missing cities in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find window.cityDetails block
    pattern = r'(window\.cityDetails\s*=\s*\{)(.*?)(\};)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"  No cityDetails found in {filepath}")
        return False
    
    full_match = match.group(0)
    inner = match.group(2)
    
    # Find existing city entries
    existing_entries = re.findall(r'"(\w+)":\s*\{[^}]*\}', inner)
    
    # Determine which cities are missing
    all_needed = list(ALL_ENTRIES.keys())
    missing = [c for c in all_needed if c not in existing_entries]
    
    if not missing:
        print(f"  No missing cities in {filepath}")
        return False
    
    # Sort missing cities in desired order
    ordered = get_city_order()
    missing_sorted = sorted(missing, key=lambda x: ordered.index(x) if x in ordered else 999)
    
    # Build the new entries to insert (alphabetically sorted within city type)
    new_entries = []
    city_missing = [c for c in missing_sorted if c in CITY_ENTRIES]
    additional_missing = [c for c in missing_sorted if c in ADDITIONAL_ENTRIES]
    
    # Find insertion point - before iching (which starts the cultural section)
    # The entries appear to be in order: cities then cultural entries
    # We need to find where to insert new city entries
    
    # Find insertion point - after the last city entry (before iching or similar)
    # Look for the pattern: city entries followed by cultural entries
    city_order = ['beijing', 'shanghai', 'xian', 'guilin', 'zhangjiajie', 'jiuzhaigou', 'yangtze', 
                  'chengdu', 'hangzhou', 'huangshan', 'suzhou', 'xiamen', 'chongqing', 'guangzhou', 
                  'shenzhen', 'kunming', 'dali', 'lijiang']
    
    # Find the last existing city entry
    last_city_pos = -1
    for city in reversed(city_order):
        if city in existing_entries:
            # Find the position of this city entry
            city_pattern = rf'"{city}":\{{[^}}]*\}}'
            m = re.search(city_pattern, inner)
            if m:
                last_city_pos = max(last_city_pos, m.end())
    
    if last_city_pos == -1:
        # No city found, try to find insertion before iching or first cultural entry
        cultural = ['iching', 'clothing', 'music', 'paper', 'language', 'greatwall']
        for cult in cultural:
            if cult in existing_entries:
                cult_pattern = rf'"{cult}"'
                m = re.search(cult_pattern, inner)
                if m:
                    last_city_pos = m.start() - 1
                    break
    
    # Build the string to insert
    new_entries_str = ','.join([f'"{c}":{ALL_ENTRIES[c]}' for c in missing_sorted])
    
    # Insert the new entries
    if last_city_pos >= 0:
        new_content = content[:match.start(1) + len(match.group(1)) + last_city_pos] + ',' + new_entries_str + content[match.start(1) + len(match.group(1)) + last_city_pos:]
    else:
        # Fallback: append at the end before the closing };
        new_content = content[:match.end(1)] + new_entries_str + content[match.end(1):]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Fixed {filepath}: added {missing_sorted}")
    return True

def main():
    fixed_count = 0
    for lang in LANG_DIRS:
        for city in CITY_PAGES:
            fname = f'{lang}/{city}.html' if lang else f'{city}.html'
            if not os.path.exists(fname):
                continue
            if fix_file(fname):
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} files.")

if __name__ == '__main__':
    main()