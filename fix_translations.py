import re, os, json

dirs = ['ja', 'ko', 'es', 'fr', 'de', 'ru']
cities = ['clothing', 'festivals', 'painting', 'pottery']

fixed_any = False
for d in dirs:
    for city in cities:
        path = f'{d}/{city}.html'
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the window.translations block
        m = re.search(r'(window\\.translations\\s*=\\s*)(\\{.*?\\})(\\s*;)', content, re.DOTALL)
        if not m:
            print(f'Skipping {path}: no window.translations block found')
            continue
        
        prefix = m.group(1)
        json_str = m.group(2)
        suffix = m.group(3)
        
        # Try to parse the JSON to see if it's valid
        try:
            json.loads(json_str)
            # If valid, no need to fix
            continue
        except json.JSONDecodeError:
            pass
        
        # The corruption pattern: </p>," (missing closing quote) should be </p>","
        # We need to fix the JSON string by replacing all occurrences of </p>, with </p>", 
        # but only inside string values? Actually the pattern is inside a string value where 
        # the string contains </p> followed by a comma but missing the closing quote before the comma.
        # Looking at the skill: Pattern appears before natureTitle separator in longDesc values
        # Replace all occurrences of the specific pattern
        fixed_json_str = re.sub(r'</p>,\"', '</p>\"\",\"', json_str)
        # Apply twice to catch any remaining instances (as per the skill)
        fixed_json_str = re.sub(r'</p>,\"', '</p>\"\",\"', fixed_json_str)
        
        # Try to parse the fixed JSON
        try:
            json.loads(fixed_json_str)
            # If valid, replace in content
            new_content = prefix + fixed_json_str + suffix
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed: {path}')
                fixed_any = True
            else:
                print(f'No change needed for {path} (already fixed?)')
        except json.JSONDecodeError as e:
            print(f'Failed to fix {path}: {e}')
            # As a fallback, let's try a more aggressive approach: replace all </p>, with </p>", 
            # but we need to be careful not to break valid JSON.
            # Let's just do the same replacement but maybe there are other patterns.
            # For now, we'll just note the failure.
            pass

if not fixed_any:
    print('No files were fixed.')
