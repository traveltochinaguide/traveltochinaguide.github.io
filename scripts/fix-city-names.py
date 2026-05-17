#!/usr/bin/env python3
"""Fix city names in translations.js for zh-CN"""
import re

TARGET = '/home/ubuntu/traveltochinaguide.github.io/js/translations.js'

FIXES = {
    'Chongqing': '重庆',
    'Dali': '大理',
    'Guangzhou': '广州',
    'Huangshan': '黄山',
    'Kunming': '昆明',
    'Lijiang': '丽江',
    'Shenzhen': '深圳',
}

with open(TARGET, 'r', encoding='utf-8') as f:
    text = f.read()

# Find zh-CN section
start = text.find('\"zh-CN\": {')
end = text.find('\"ja\": {', start)
zh_section = text[start:end]

for en, cn in FIXES.items():
    # Pattern: "city<EnglishName>": "<EN>"
    # Find the value for city{en}
    key_pattern = f'\"city{en}\"'
    idx = zh_section.find(key_pattern)
    if idx == -1:
        print(f'  NOT FOUND: city{en}')
        continue
    # Find the value after ": "
    val_start = zh_section.find('"', idx + len(key_pattern) + 2)
    val_end = zh_section.find('"', val_start + 1)
    old_val = zh_section[val_start+1:val_end]
    
    if old_val == cn:
        print(f'  SKIP: city{en} already = {cn}')
        continue
    
    # Replace in the full text
    # Need to find the exact position in the full text
    full_idx = text.find(f'\"city{en}\"', start)
    if full_idx >= 0:
        # Find the ":" pattern and extract value
        after_key = text.find(':', full_idx)
        v_start = text.find('"', after_key + 1)
        v_end = text.find('"', v_start + 1)
        actual_old = text[v_start+1:v_end]
        old_str = f'\"{actual_old}\"'
        new_str = f'\"{cn}\"'
        text = text[:v_start+1] + cn + text[v_end:]
        print(f'  FIXED: city{en}: {actual_old} -> {cn}')
    else:
        print(f'  NOT FOUND in full text: city{en}')

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(text)

print('\nDone. Now run generate-multilang.js to regenerate pages.')