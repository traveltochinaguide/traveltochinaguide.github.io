#!/usr/bin/env python3
"""
Fix city names in translations.js for ja/ko/ru/fr/de/es.
Only fixes names that are ASCII/latin when they should be in local script.
"""
import re

PATH = '/home/ubuntu/traveltochinaguide.github.io/js/translations.js'

# Localized city names by language
# Source: Wikipedia / common travel usage
CITY_NAMES = {
    'ja': {
        'Chongqing': '重慶（チョンチン）',
        'Dali': '大理（ダーリー）',
        'Guangzhou': '広州',
        'Huangshan': '黄山（ホワンシャン）',
        'Kunming': '昆明（クンミン）',
        'Lijiang': '麗江（リージャン）',
        'Shenzhen': '深圳（シンセン）',
        'Zhangjiajie': '張家界（ヂャンジャジエ）',
    },
    'ko': {
        'Chongqing': '충칭',
        'Dali': '다리',
        'Guangzhou': '광저우',
        'Huangshan': '황산',
        'Kunming': '쿤밍',
        'Lijiang': '리장',
        'Shenzhen': '선전',
        'Zhangjiajie': '장자제',
    },
    'ru': {
        'Chongqing': 'Чунцин',
        'Dali': 'Дали',
        'Guangzhou': 'Гуанчжоу',
        'Huangshan': 'Хуаншань',
        'Kunming': 'Куньмин',
        'Lijiang': 'Лицзян',
        'Shenzhen': 'Шэньчжэнь',
        'Zhangjiajie': 'Чжанцзяцзе',
    },
    'fr': {
        'Chengdu': 'Chengdu',
        'Chongqing': 'Chongqing',
        'Dali': 'Dali',
        'Guangzhou': 'Guangzhou',
        'Guilin': 'Guilin',
        'Hangzhou': 'Hangzhou',
        'Huangshan': 'Huangshan',
        'Jiuzhaigou': 'Jiuzhaigou',
        'Kunming': 'Kunming',
        'Lijiang': 'Lijiang',
        'Shanghai': 'Shanghai',
        'Shenzhen': 'Shenzhen',
        'Suzhou': 'Suzhou',
        'Xiamen': 'Xiamen',
        'Xian': 'Xi\'an',
        'Yangtze': 'Yangtsé',
        'Zhangjiajie': 'Zhangjiajie',
    },
    'de': {
        'Chongqing': 'Chongqing',
        'Dali': 'Dali',
        'Guangzhou': 'Guangzhou',
        'Huangshan': 'Huangshan',
        'Kunming': 'Kunming',
        'Lijiang': 'Lijiang',
        'Shenzhen': 'Shenzhen',
        'Zhangjiajie': 'Zhangjiajie',
        'Chengdu': 'Chengdu',
        'Guilin': 'Guilin',
        'Hangzhou': 'Hangzhou',
        'Jiuzhaigou': 'Jiuzhaigou',
        'Shanghai': 'Shanghai',
        'Suzhou': 'Suzhou',
        'Xiamen': 'Xiamen',
        'Xian': 'Xi\'an',
        'Yangtze': 'Jangtse',
    },
    'es': {
        'Chengdu': 'Chengdú',
        'Chongqing': 'Chongqing',
        'Dali': 'Dali',
        'Guangzhou': 'Guangzhou',
        'Hangzhou': 'Hangzhou',
        'Huangshan': 'Huangshan',
        'Jiuzhaigou': 'Jiuzhaigou',
        'Kunming': 'Kunming',
        'Lijiang': 'Lijiang',
        'Shenzhen': 'Shenzhen',
        'Suzhou': 'Suzhou',
        'Xiamen': 'Xiamen',
        'Xian': 'Xi\'an',
        'Zhangjiajie': 'Zhangjiajie',
    },
}

# For CJK languages (ja/ko) and Russian - translate to local script
NON_LATIN = {
    'ja': {
        'Chongqing': '重慶',
        'Dali': '大理',
        'Guangzhou': '広州',
        'Huangshan': '黄山',
        'Kunming': '昆明',
        'Lijiang': '麗江',
        'Shenzhen': '深圳',
        'Zhangjiajie': '張家界',
    },
    'ko': {
        'Chongqing': '충칭',
        'Dali': '다리',
        'Guangzhou': '광저우',
        'Huangshan': '황산',
        'Kunming': '쿤밍',
        'Lijiang': '리장',
        'Shenzhen': '선전',
        'Zhangjiajie': '장자제',
    },
    'ru': {
        'Chongqing': 'Чунцин',
        'Dali': 'Дали',
        'Guangzhou': 'Гуанчжоу',
        'Huangshan': 'Хуаншань',
        'Kunming': 'Куньмин',
        'Lijiang': 'Лицзян',
        'Shenzhen': 'Шэньчжэнь',
        'Zhangjiajie': 'Чжанцзяцзе',
    },
}

with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()

changes = 0
for lang, cities in NON_LATIN.items():
    for en_name, localized in cities.items():
        key = f'city{en_name}'
        # Find this key in the lang section
        # Get the language section
        lang_start = text.find(f'"{lang}": {{')
        if lang_start < 0:
            print(f"  SKIP: {lang} section not found")
            continue
        
        # Find the key after lang_start
        key_pos = text.find(f'"{key}"', lang_start)
        if key_pos < 0:
            print(f"  SKIP: {key} not found in {lang}")
            continue
        
        # Find value after key
        colon_pos = text.find(':', key_pos)
        val_start = text.find('"', colon_pos + 1)
        val_end = text.find('"', val_start + 1)
        
        old_val = text[val_start+1:val_end]
        if old_val == localized:
            print(f"  SKIP: {lang}.{key} already = {localized}")
            continue
        
        # Replace
        text = text[:val_start+1] + localized + text[val_end:]
        print(f"  FIXED: {lang}.{key}: {old_val} -> {localized}")
        changes += 1

if changes > 0:
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\nDone. {changes} changes made.")
else:
    print("\nNo changes needed.")