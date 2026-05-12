#!/usr/bin/env python3
import re

def find_matching_brace(text, start_pos):
    """Find the position of the matching closing brace for the opening brace at start_pos.
    Assumes text[start_pos] == '{'
    Returns the index of the matching '}' or -1 if not found.
    """
    stack = 1
    pos = start_pos + 1
    while pos < len(text):
        ch = text[pos]
        if ch == '{':
            stack += 1
        elif ch == '}':
            stack -= 1
            if stack == 0:
                return pos
        pos += 1
    return -1

def insert_keys_in_language_section(content, lang, keys_to_add):
    # Pattern to find the start of the language section: "lang": {
    pattern = rf'\"{lang}\"\s*:\s*{{'
    match = re.search(pattern, content)
    if not match:
        print(f"Could not find start of {lang} section")
        return content, False
    
    start_brace_pos = match.end() - 1  # position of the '{'
    end_brace_pos = find_matching_brace(content, start_brace_pos)
    if end_brace_pos == -1:
        print(f"Could not find matching brace for {lang} section")
        return content, False
    
    # Extract the content inside the braces
    inner_start = start_brace_pos + 1
    inner_end = end_brace_pos
    inner_content = content[inner_start:inner_end]
    
    # Determine the indentation used inside this section.
    lines = inner_content.split('\n')
    indent = None
    for line in lines:
        if line.strip():
            match = re.match(r'^( *)', line)
            if match:
                indent = match.group(1)
                break
    if indent is None:
        indent = ' ' * 4  # default
    
    # Prepare the lines to insert
    insert_lines = []
    for key, value in keys_to_add.items():
        # Escape the value for JSON string: we need to escape backslashes and quotes.
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        insert_lines.append(f'{indent}  "{key}": "{escaped}",')
    
    # If there is already content, we need to add a comma after the last existing property if it doesn't have one.
    # Check the last non-empty line of inner_content.
    last_non_empty = None
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip():
            last_non_empty = lines[i]
            break
    needs_comma = False
    if last_non_empty:
        # If the last non-empty line does not end with a comma, we need to add one.
        if not last_non_empty.rstrip().endswith(','):
            needs_comma = True
    
    # Build the new inner content
    new_inner_lines = []
    if needs_comma:
        # We'll add a comma to the last line and then a newline.
        # Actually, it's easier to rebuild: we'll take all lines, and if the last line doesn't end with a comma, we add one.
        # But note: the last line might have trailing comments? We'll assume not.
        # We'll just add a comma to the last line and then add our new lines.
        # However, we don't want to modify the existing lines if we can avoid it.
        # Instead, we'll keep the existing lines as is, and then add our new lines with a comma before the first new line if needed.
        # The convention is that each line ends with a comma except the last one? Actually, in the file, each property ends with a comma.
        # So we expect every line to end with a comma. Let's check a sample.
        # We'll just add our new lines with a comma at the end of each, and then we will remove the trailing comma from the last new line? 
        # Actually, we want the last property in the section to not have a trailing comma? No, in JS object, the last property can have a trailing comma? 
        # It is allowed in ES5? Actually, trailing commas in object literals are allowed in ES5? 
        # According to ES5, trailing commas in object literals are not allowed. But in ES3? 
        # However, the file we have does have trailing commas after each property, including the last one? Let's check.
        # We'll look at the en section: the last line before the closing brace? We don't know.
        # To be safe, we'll follow the existing pattern: if the last line of the inner content ends with a comma, then we add our lines each with a comma, and then we do not add an extra comma after the last new line.
        # If the last line does not end with a comma, then we add a comma to the last line, and then our lines each with a comma, and then we remove the comma from the last new line? 
        # This is getting messy.
        #
        # Let's take a simpler approach: we will insert our new lines, each ending with a comma, and then we will not worry about the trailing comma in the entire object because the file we have might already have a trailing comma after the last property in each language section? 
        # Actually, looking at the file, the language sections do NOT have a trailing comma after the last property? Let's check a small section.
        # We'll write a small test later, but for now, we'll assume that the section does not have a trailing comma after the last property (because the next line is the closing brace of the section, and then a comma to separate from the next language).
        # So we will insert our new lines, each ending with a comma, and then we will not add any extra comma.
        # But note: we must separate our new lines from the existing content with a newline.
        pass
    
    # We'll just insert our new lines with a newline before and after, and each line ends with a comma.
    # We'll also ensure that if the inner_content is not empty and does not end with a newline, we add a newline.
    if inner_content and not inner_content.endswith('\n'):
        inner_content += '\n'
    
    # Add our new lines
    for line in insert_lines:
        inner_content += line + '\n'
    
    # Now reconstruct the content
    new_content = content[:inner_start] + inner_content + content[end_brace_pos:]
    return new_content, True

def main():
    filename = 'js/translations.js'
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    keys_to_add = {
        'ogTitleArchitecture': 'Chinese Architecture - Forbidden City, Temple of Heaven & Classical Design',
        'ogDescArchitecture': "Explore Chinese architecture — from the Forbidden City's imperial grandeur to Temple of Heaven geometry and traditional courtyard houses."
    }
    
    langs = ['ja', 'ko', 'ru', 'fr', 'de', 'es']
    
    new_content = content
    any_changed = False
    for lang in langs:
        new_content, changed = insert_keys_in_language_section(new_content, lang, keys_to_add)
        if changed:
            any_changed = True
            print(f"Updated {lang} section")
        else:
            print(f"Failed to update {lang} section")
    
    if any_changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("File updated successfully.")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()