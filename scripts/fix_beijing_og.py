with open('/home/ubuntu/traveltochinaguide.github.io/beijing.html', 'r') as f:
    content = f.read()

# Read the exact og:title and twitter:title lines from the file to use as search strings
# Extract the exact lines
lines = content.split('\n')
og_title_old = None
tw_title_old = None
for line in lines:
    if '<meta property="og:title"' in line and 'data-lang-key' not in line:
        og_title_old = line
    if '<meta property="twitter:title"' in line and 'data-lang-key' not in line:
        tw_title_old = line

print("og:title line found:", og_title_old is not None)
print("twitter:title line found:", tw_title_old is not None)
if og_title_old:
    print("OG:", repr(og_title_old))
if tw_title_old:
    print("TW:", repr(tw_title_old))

# Now create new versions with data-lang-key
if og_title_old:
    og_title_new = og_title_old.replace('content="', 'data-lang-key="ogTitleBeijing" content="')
    content = content.replace(og_title_old, og_title_new)
    print("OG replaced:", og_title_new)
if tw_title_old:
    tw_title_new = tw_title_old.replace('content="', 'data-lang-key="ogTitleBeijing" content="')
    content = content.replace(tw_title_old, tw_title_new)
    print("TW replaced:", tw_title_new)

with open('/home/ubuntu/traveltochinaguide.github.io/beijing.html', 'w') as f:
    f.write(content)

# Verify
with open('/home/ubuntu/traveltochinaguide.github.io/beijing.html', 'r') as f:
    lines2 = f.readlines()
for i, line in enumerate(lines2[13:28], start=14):
    if 'og:title' in line or 'og:description' in line or 'twitter:title' in line or 'twitter:description' in line:
        print(f"Line {i}: {line.rstrip()}")