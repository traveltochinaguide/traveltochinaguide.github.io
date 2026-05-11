import re
import os

dirs = ['ja', 'ko', 'es', 'fr', 'de', 'ru']
cities = ['clothing', 'festivals', 'painting', 'pottery']

for d in dirs:
    for city in cities:
        path = f'{d}/{city}.html'
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find window.translations assignments
        # We use non-greedy dotall to capture the smallest possible block that ends with };
        pattern = r'(window\\.translations\\s*=\\s*\\{.*?\\})\\s*;'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        if not matches:
            print(f'{path}: No window.translations assignments found')
            continue
        
        # We'll build the new content by replacing each match (except possibly the first) with a fixed version.
        # But we need to know which ones are the language blocks.
        # According to the structure, the first block is for 'en', and subsequent ones are for the language.
        # However, note that the file might have more than two? We'll fix all blocks that are not the first.
        # But to be safe, we'll fix every block that contains the corruption pattern? 
        # Instead, we'll fix every block and then validate. If a block becomes invalid, we revert that block.
        # However, we know the corruption pattern is in the language blocks.
        
        # Let's just fix every block by replacing the pattern, and then validate the entire file's window.translations blocks.
        # If validation fails, we revert.
        
        # We'll do a replacement on the entire content for the pattern, but only inside the window.translations blocks?
        # Instead, we'll do the replacement on the entire content and then check if the JSON is valid.
        # But note: the pattern might appear outside the JSON? Unlikely.
        
        original = content
        # Apply the fix to the entire content
        content = re.sub(r'</p>,\"', '</p>\"\",\"', content)
        content = re.sub(r'</p>,\"', '</p>\"\",\"', content)
        
        # Now validate by extracting all window.translations blocks and trying to parse them
        matches_after = list(re.finditer(pattern, content, re.DOTALL))
        all_valid = True
        for m in matches_after:
            json_str = m.group(1)
            try:
                json.loads(json_str)
            except json.JSONDecodeError:
                all_valid = False
                break
        
        if all_valid and content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed: {path}')
        elif not all_valid:
            print(f'{path}: Still invalid after fix, reverting')
            # Revert by not writing
        else:
            print(f'{path}: No change needed')
