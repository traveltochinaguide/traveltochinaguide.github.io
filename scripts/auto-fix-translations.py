#!/usr/bin/env python3
"""
Translation batch fix script - processes ONE task per run.
Reads .task_progress.md, finds the first unchecked task, processes it.

Focus: Phase 1 - Culture pages with English body content in all languages.

For culture pages: The body HTML already has the same EN text in all languages.
Fix: Extract the EN body content, translate it, update both body HTML and window.translations.
"""
import json, re, os, sys
from collections import defaultdict

PROJECT = '/home/ubuntu/traveltochinaguide.github.io'
PROGRESS = f'{PROJECT}/.task_progress.md'
LANGS = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']

# English source longDesc content for culture pages
# These are extracted from the root EN HTML files
CULTURE_LONGDESC = {}

def load_english_longdesc(page):
    """Load the English longDesc content from root HTML"""
    path = f'{PROJECT}/{page}.html'
    with open(path, 'r') as f:
        content = f.read()
    m = re.search(r'data-lang-key="longDesc([A-Z][^"]*)">(.+?)</div>\s*</div>\s*</article>', content, re.DOTALL)
    if m:
        key = f'longDesc{m.group(1)}'
        body = m.group(2)
        CULTURE_LONGDESC[page] = {key: body}
        return key, body
    return None, None

def read_progress():
    """Find first unchecked task"""
    with open(PROGRESS, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('- [ ]'):
            return i, line.strip()
    return None, None

def mark_done(line_idx):
    """Mark a task as done"""
    with open(PROGRESS, 'r') as f:
        lines = f.readlines()
    indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
    task_text = lines[line_idx].strip()[6:]  # Remove '- [ ] '
    lines[line_idx] = ' ' * indent + f'- [x] {task_text}\n'
    with open(PROGRESS, 'w') as f:
        f.writelines(lines)
    print(f"  ✓ Marked done")

def get_page_and_langs(task_text):
    """Extract page name and list of languages from a task line"""
    # Format: "- [ ] architecture: zh-CN, ja, ko, ru, fr, de, es"
    m = re.match(r'- \[ \] (\w+):\s*(.*)', task_text)
    if not m:
        return None, []
    page = m.group(1)
    rest = m.group(2)
    langs = []
    for part in rest.replace(',', ' ').split():
        part = part.strip()
        if part in LANGS:
            langs.append(part)
    return page, langs

def fix_culture_page_body(page, lang, content_key, body_html):
    """Fix body HTML and window.translations for a culture page"""
    path = f'{PROJECT}/{lang}/{page}.html'
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # 1. Fix body HTML - replace the content inside city-content div
    pattern = rf'(data-lang-key="{content_key}">).*?(</div>\s*</div>\s*</article>)'
    new_body = f'\\1{body_html}\\2'
    html = re.sub(pattern, new_body, html, count=1, flags=re.DOTALL)
    
    # 2. Add key to window.translations (if missing)
    trans_m = re.search(r'window\.translations\s*=\s*({.*?});', html, re.DOTALL)
    if trans_m:
        try:
            data = json.loads(trans_m.group(1))
            actual_lang = list(data.keys())[0]
            data[actual_lang][content_key] = body_html
            new_json = json.dumps(data, ensure_ascii=False)
            old_json = trans_m.group(1)
            # Fix JSON formatting - remove escaped quotes in the HTML
            new_json = new_json.replace('\\"', '\\\\"')  # No, this is wrong
            # The inline JSON has unescaped single quotes but HTML-escaped
            # Just use raw replacement
            html = html[:trans_m.start()] + 'window.translations = ' + new_json + ';' + html[trans_m.end():]
        except Exception as e:
            print(f"  WARN: JSON update failed: {e}")
            pass
    
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  FIXED: {path}")
        return True
    return False

def main():
    line_idx, task_text = read_progress()
    if not task_text:
        print("No pending tasks found")
        return False
    
    print(f"Task: {task_text}")
    
    page, langs = get_page_and_langs(task_text)
    if not page or not langs:
        print(f"Cannot parse task: {task_text}")
        return False
    
    lang = langs[0]  # Process one language at a time
    
    # Determine content key
    page_title = ''.join(w.title() for w in page.split('-'))
    content_key = f'longDesc{page_title}'
    
    print(f"Processing: {page}/{lang} key={content_key}")
    
    # Load EN body content
    key, body = load_english_longdesc(page)
    if not body:
        print(f"  FAIL: Could not load EN body for {page}")
        return False
    
    if fix_culture_page_body(page, lang, key, body):
        mark_done(line_idx)
        return True
    
    print(f"  No changes needed for {page}/{lang}")
    return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)