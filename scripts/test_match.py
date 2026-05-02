with open('/home/ubuntu/traveltochinaguide.github.io/beijing.html', 'r') as f:
    content = f.read()

# Find exact og:title line
idx = content.find('<meta property="og:title"')
segment = content[idx:idx+100]
print('Exact:', repr(segment))
print()

# Test if our search string matches
test1 = '<meta property="og:title" content="Beijing Travel Guide - Imperial Palace, Great Wall & Tours">'
test2 = '<meta property="og:title" content="Beijing Travel Guide - Imperial Palace, Great Wall & Tours">'
print('test1 in content:', test1 in content)
print('test2 in content:', test2 in content)
print()
print('test1 repr:', repr(test1))
print('test2 repr:', repr(test2))