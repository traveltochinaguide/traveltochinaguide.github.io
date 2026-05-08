#!/usr/bin/env python3
"""
修复 hreflang 标签中的英文路径问题
将 /en/page.html 改为 /page.html
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/ubuntu/traveltochinaguide.github.io')

def fix_hreflang(file_path):
    """修复单个文件的 hreflang 标签"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复英文路径：将 /en/page.html 改为 /page.html
    # 模式 1: 完整 URL - href="https://travelchinaguide.dpdns.org/en/page.html"
    fixed = re.sub(
        r'href="https://travelchinaguide\.dpdns\.org/en/([^"]+)" hreflang="en"',
        r'href="https://travelchinaguide.dpdns.org/\1" hreflang="en"',
        content
    )
    
    # 模式 2: 相对路径 - href="/en/page.html"
    fixed = re.sub(
        r'href="/en/([^"]+)" hreflang="en"',
        r'href="/\1" hreflang="en"',
        fixed
    )
    
    # 模式 3: hreflang 在前的情况
    fixed = re.sub(
        r'hreflang="en" href="https://travelchinaguide\.dpdns\.org/en/([^"]+)"',
        r'hreflang="en" href="https://travelchinaguide.dpdns.org/\1"',
        fixed
    )
    
    fixed = re.sub(
        r'hreflang="en" href="/en/([^"]+)"',
        r'hreflang="en" href="/\1"',
        fixed
    )
    
    if content != fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        return True
    return False

def main():
    print("🔧 开始修复 hreflang 标签...")
    
    # 查找所有 HTML 文件
    html_files = list(BASE_DIR.glob('**/*.html'))
    print(f"找到 {len(html_files)} 个 HTML 文件")
    
    fixed_count = 0
    for html_file in html_files:
        if fix_hreflang(html_file):
            fixed_count += 1
            print(f"  ✓ {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n✅ 完成！修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
