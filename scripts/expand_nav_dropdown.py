#!/usr/bin/env python3
"""Expand city navigation dropdown on ALL city pages to include all 17 cities."""
import os, re

BASE = '/home/ubuntu/traveltochinaguide.github.io'

# All 17 cities for the nav dropdown
CITIES_17 = [
    'beijing', 'shanghai', 'xian', 'chengdu', 'guilin',
    'hangzhou', 'suzhou', 'xiamen', 'zhangjiajie', 'jiuzhaigou', 'yangtze',
    'chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'
]

# Root-level city HTML pages (have the city dropdown)
CITY_PAGES_ROOT = [
    'beijing.html', 'shanghai.html', 'xian.html', 'chengdu.html', 'guilin.html',
    'hangzhou.html', 'suzhou.html', 'xiamen.html', 'jiuzhaigou.html', 'yangtze.html',
    'zhangjiajie.html', 'chongqing.html', 'guangzhou.html', 'shenzhen.html',
    'kunming.html', 'dali.html', 'lijiang.html'
]

LANGS = ['zh-CN', 'ja', 'ko', 'es', 'fr', 'de', 'ru']

def build_city_links(prefix=''):
    """Build nav dropdown links for all 17 cities."""
    links = []
    for city in CITIES_17:
        href = f'/{prefix}{city}.html' if prefix else f'/{city}.html'
        links.append(f'  <a href="{href}" class="block px-3 py-2 text-sm font-medium text-gray-800 hover:bg-gray-100 whitespace-nowrap" data-lang-key="city{city.title()}" role="menuitem">{city.capitalize()}</a>')
    return '\n'.join(links)

def expand_dropdown_root(path):
    """Expand dropdown on a root-level HTML file (links like /city.html)."""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    old_dropdown = '<div class="dropdown-panel hidden absolute left-0 top-full mt-0 min-w-max w-56 bg-white rounded-md shadow-md p-2 z-50" role="menu">'
    if old_dropdown not in html:
        return False
    
    # Find navCities button and then the dropdown after it
    nav_cities_matches = list(re.finditer(r'data-lang-key="navCities"', html))
    updated = 0
    for m in nav_cities_matches:
        search_start = m.end()
        panel_start = html.find(old_dropdown, search_start)
        if panel_start == -1:
            continue
        panel_end = html.find('</div>', panel_start) + 6
        panel_content = html[panel_start:panel_end]
        
        # Check if this is the city dropdown (has beijing.html)
        if 'href="/beijing.html"' not in panel_content and 'href="/xian.html"' not in panel_content:
            continue
        
        # Count current cities
        current_cities = re.findall(r'href="/(\w+)\.html"', panel_content)
        if len(current_cities) >= 14:
            continue  # Already expanded
        
        new_dropdown = f'''
  <div class="dropdown-panel hidden absolute left-0 top-full mt-0 min-w-max w-56 bg-white rounded-md shadow-md p-2 z-50" role="menu">
{build_city_links()}
</div>'''
        html = html[:panel_start] + new_dropdown + html[panel_end:]
        updated += 1
    
    if updated > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return updated > 0

def expand_dropdown_lang(path, lang):
    """Expand dropdown on a language-version HTML file (links like /zh-CN/city.html)."""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # For lang pages, the dropdown links include the lang prefix
    old_dropdown = '<div class="dropdown-panel hidden absolute left-0 top-full mt-0 min-w-max w-56 bg-white rounded-md shadow-md p-2 z-50" role="menu">'
    if old_dropdown not in html:
        return False
    
    nav_cities_matches = list(re.finditer(r'data-lang-key="navCities"', html))
    updated = 0
    for m in nav_cities_matches:
        search_start = m.end()
        panel_start = html.find(old_dropdown, search_start)
        if panel_start == -1:
            continue
        panel_end = html.find('</div>', panel_start) + 6
        panel_content = html[panel_start:panel_end]
        
        # Check if this is city dropdown - zh-CN uses /zh-CN/beijing.html, etc.
        if f'href="/{lang}/beijing.html"' not in panel_content and f'href="/{lang}/xian.html"' not in panel_content:
            continue
        
        current_cities = re.findall(r'href="/\w+/(\w+)\.html"', panel_content)
        if len(current_cities) >= 14:
            continue
        
        new_dropdown = f'''
  <div class="dropdown-panel hidden absolute left-0 top-full mt-0 min-w-max w-56 bg-white rounded-md shadow-md p-2 z-50" role="menu">
{build_city_links(lang + '/')}
</div>'''
        html = html[:panel_start] + new_dropdown + html[panel_end:]
        updated += 1
    
    if updated > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return updated > 0

# Process root pages
updated_root = []
for page in CITY_PAGES_ROOT:
    path = f'{BASE}/{page}'
    if os.path.exists(path):
        changed = expand_dropdown_root(path)
        if changed:
            updated_root.append(page)

print(f'Updated {len(updated_root)} root pages')

# Process language versions
total_lang = 0
for lang in LANGS:
    lang_dir = f'{BASE}/{lang}'
    if not os.path.exists(lang_dir):
        continue
    count = 0
    for page in CITY_PAGES_ROOT:
        path = f'{lang_dir}/{page}'
        if os.path.exists(path):
            changed = expand_dropdown_lang(path, lang)
            if changed:
                count += 1
    print(f'  {lang}: {count} pages updated')
    total_lang += count

print(f'Total: {len(updated_root)} root + {total_lang} lang = {len(updated_root) + total_lang} files')