#!/usr/bin/env python3
"""Inject longDesc translations for 7 cities across 6 non-EN languages."""

import re
import json

# Load translations data
with open('/home/ubuntu/traveltochinaguide.github.io/scripts/translations_data.json', 'r', encoding='utf-8') as f:
    translations_data = json.load(f)

# Read the main translations file
trans_path = '/home/ubuntu/traveltochinaguide.github.io/js/translations.js'
with open(trans_path, 'r', encoding='utf-8') as f:
    content = f.read()

def js_escape(s):
    """Escape a string for use as a JS double-quoted string literal."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

cities = ['Beijing', 'Shanghai', 'Xian', 'Guilin', 'Zhangjiajie', 'Jiuzhaigou', 'Yangtze', 'Iching']

# Target languages and their section markers
target_langs = {
    'ja': "'ja': {",
    'ko': "'ko': {",
    'ru': "'ru': {",
    'fr': "'fr': {",
    'de': "'de': {",
    'es': "'es': {",
}

total_injected = 0
total_skipped = 0

for lang, section_marker in target_langs.items():
    if lang not in translations_data:
        print(f"WARNING: {lang} not in translations data")
        continue

    # Find the section boundaries
    section_start = content.find(section_marker)
    if section_start < 0:
        print(f"WARNING: {lang} section not found!")
        continue

    # Find the end of this section (next lang's start or end of file)
    # Look for next section marker
    remaining = content[section_start + len(section_marker):]
    next_section_patterns = ["'ru': {", "'fr': {", "'de': {", "'es': {", "\n};\n\nif (typeof"]
    section_end_offset = len(remaining)  # default: to end
    for pat in next_section_patterns:
        idx = remaining.find(pat)
        if idx > 0 and idx < section_end_offset:
            section_end_offset = idx

    section = remaining[:section_end_offset]
    modified_section = section

    for city in cities:
        key = f'longDesc{city}'
        translation = translations_data[lang].get(key)
        if not translation:
            print(f"  WARNING: {lang}/{key} not in translation data")
            continue

        # Check if the entry already has proper translated content (not English)
        if key in modified_section:
            idx = modified_section.find(key)
            # Find the end of this entry (next comma or end of section)
            after_key = modified_section[idx + len(key) + 2:]  # skip "key: "
            # Check if it's English text (starts with <p>Beijing, or similar)
            if after_key.startswith('"<p>Beijing') or after_key.startswith('"<p>Shanghai') or after_key.startswith('"<p>Xi\'an') or after_key.startswith('"<p>Guilin') or after_key.startswith('"<p>Zhangjiajie') or after_key.startswith('"<p>Jiuzhaigou') or after_key.startswith('"<p>The Yangtze') or after_key.startswith('"<p>The <strong>I Ching'):
                # It's English - needs replacement
                # Find the entire string value
                str_start = after_key.index('"') + 1
                # Find matching end quote
                pos = str_start
                depth_html = 0
                in_tag = False
                while pos < len(after_key):
                    c = after_key[pos]
                    pc = after_key[pos-1] if pos > 0 else ''
                    if pc != '\\':
                        if c == '<':
                            in_tag = True
                        elif c == '>' and in_tag:
                            in_tag = False
                        elif c == '"' and not in_tag:
                            break
                    pos += 1
                str_end = pos + 1  # include the closing quote

                old_value = after_key[str_start-1:str_end]
                new_value = '"' + js_escape(translation) + '"'

                if old_value == new_value:
                    total_skipped += 1
                else:
                    # Replace
                    old_block = key + ': ' + old_value
                    new_block = key + ': ' + new_value
                    modified_section = modified_section.replace(old_block, new_block, 1)
                    total_injected += 1
                    print(f"  {lang}/{key}: injected ({len(translation)} chars)")

    # Replace section in content
    content = content[:section_start] + section_marker + modified_section + content[section_start + len(section_marker) + section_end_offset:]

print(f"\nTotal injected: {total_injected}, skipped (already correct): {total_skipped}")

# Write back
with open(trans_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Written to {trans_path}")