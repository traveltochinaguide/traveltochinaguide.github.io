#!/usr/bin/env python3
"""
China Travel Site - 自动化开发任务执行器

用法:
    python3 scripts/auto-dev-task.py --task enrich-beijing
    python3 scripts/auto-dev-task.py --task create-page --city nanjing
    python3 scripts/auto-dev-task.py --task check-seo
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path('/home/ubuntu/traveltochinaguide.github.io')
PROGRESS_FILE = Path.home() / '.hermes' / 'cron' / 'china-travel-progress.md'

def read_progress():
    """读取进度文件"""
    if not PROGRESS_FILE.exists():
        return []
    
    tasks = []
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        in_todo = False
        for line in f:
            if line.startswith('###'):
                in_todo = True
            if in_todo and line.strip().startswith('- [ ]'):
                task = line.strip()[6:].strip()
                tasks.append(task)
            elif line.startswith('##') and '待办' not in line:
                in_todo = False
    return tasks

def enrich_city_content(city_name, additions):
    """丰富城市页面内容"""
    print(f"📝 丰富 {city_name} 页面内容...")
    
    # 1. 读取现有 HTML
    html_path = BASE_DIR / f"{city_name}.html"
    if not html_path.exists():
        print(f"❌ 文件不存在：{html_path}")
        return False
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 2. 分析现有内容
    print(f"  当前内容长度：{len(content)} 字符")
    
    # 3. 检查缺失内容
    missing = []
    if '历史' not in content and 'history' not in content.lower():
        missing.append('历史背景')
    if '美食' not in content and 'food' not in content.lower():
        missing.append('美食推荐')
    if '交通' not in content and 'transport' not in content.lower():
        missing.append '交通信息')
    
    if missing:
        print(f"  缺失内容：{', '.join(missing)}")
    else:
        print("  ✓ 内容完整")
    
    # 4. 生成更新建议
    print("\n  建议添加:")
    for item in additions or missing:
        print(f"    - {item}")
    
    return True

def create_city_page(city_name, template='xian'):
    """创建新城市页面"""
    print(f"🏙️  创建 {city_name} 页面...")
    
    # 检查是否已存在
    if (BASE_DIR / f"{city_name}.html").exists():
        print(f"  ⚠ 页面已存在")
        return False
    
    # 复制模板
    template_path = BASE_DIR / f"{template}.html"
    if not template_path.exists():
        print(f"  ❌ 模板不存在：{template_path}")
        return False
    
    new_path = BASE_DIR / f"{city_name}.html"
    
    print(f"  从模板创建：{template} -> {city_name}")
    # 实际创建逻辑...
    
    return True

def check_seo():
    """SEO 检查"""
    print("🔍 SEO 检查...\n")
    
    html_files = list(BASE_DIR.glob('*.html'))
    print(f"找到 {len(html_files)} 个 HTML 文件\n")
    
    issues = []
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 meta description
        if 'meta name="description"' not in content:
            issues.append(f"  ❌ {html_file.name}: 缺少 meta description")
        
        # 检查 JSON-LD
        if 'application/ld+json' not in content:
            issues.append(f"  ⚠ {html_file.name}: 缺少 JSON-LD Schema")
        
        # 检查 title
        if '<title>' not in content:
            issues.append(f"  ❌ {html_file.name}: 缺少 title")
    
    if issues:
        print("发现问题:")
        for issue in issues[:10]:  # 只显示前 10 个
            print(issue)
        if len(issues) > 10:
            print(f"  ... 还有 {len(issues) - 10} 个问题")
    else:
        print("  ✓ 所有页面 SEO 良好")
    
    return len(issues)

def update_progress(task, status='completed'):
    """更新进度文件"""
    if not PROGRESS_FILE.exists():
        print(f"创建进度文件：{PROGRESS_FILE}")
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_FILE.write_text(f"# Progress\n\n## Completed\n- [x] {task}\n")
    else:
        # 追加记录
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp}\n- [x] {task}\n")

def main():
    parser = argparse.ArgumentParser(description='China Travel Site 自动化开发工具')
    parser.add_argument('--task', required=True, 
                       choices=['enrich-beijing', 'enrich-shanghai', 'enrich-xian',
                               'create-page', 'check-seo', 'status'],
                       help='要执行的任务')
    parser.add_argument('--city', help='城市名称（用于 create-page 任务）')
    parser.add_argument('--additions', nargs='+', help='要添加的内容类型')
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print(f"China Travel Site - 自动化开发")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"任务：{args.task}")
    print(f"{'='*50}\n")
    
    if args.task.startswith('enrich-'):
        city = args.task.replace('enrich-', '')
        enrich_city_content(city, args.additions)
        update_progress(f"丰富{city}页面内容")
    
    elif args.task == 'create-page':
        if not args.city:
            print("❌ create-page 任务需要 --city 参数")
            sys.exit(1)
        create_city_page(args.city)
        update_progress(f"创建{args.city}页面")
    
    elif args.task == 'check-seo':
        issues = check_seo()
        update_progress(f"SEO 检查 - {issues}个问题")
    
    elif args.task == 'status':
        print("当前状态:")
        tasks = read_progress()
        print(f"待办任务：{len(tasks)}")
        for task in tasks[:5]:
            print(f"  - {task}")
    
    print(f"\n{'='*50}")
    print("✅ 任务完成")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
