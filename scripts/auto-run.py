#!/usr/bin/env python3
"""China Travel Site - 页面质量检查修复执行器
每5分钟执行，逐个检查页面。
特征: 锁文件防并发, 自愈模式, 自动git commit+push
"""

import os, sys, subprocess, json, re, time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path('/home/ubuntu/traveltochinaguide.github.io')
LOCK_FILE = Path('/tmp/hermes_china_travel.lock')
PROGRESS_FILE = Path.home() / '.hermes' / 'cron' / 'china-travel-progress.md'
LOG_FILE = Path.home() / '.hermes' / 'cron' / 'china-travel-log.md'

LANGS = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']

# 按领域分类的页面
PAGE_GROUPS = {
    'hot_cities': [
        'beijing', 'shanghai', 'xian', 'chengdu', 'guilin', 'hangzhou',
        'suzhou', 'xiamen', 'chongqing', 'guangzhou', 'shenzhen', 'kunming',
        'dali', 'lijiang', 'zhangjiajie', 'jiuzhaigou', 'huangshan',
        'nanjing', 'yangtze', 'nanjiang'
    ],
    'culture': [
        'iching', 'calligraphy', 'gardens', 'tea', 'opera', 'martialarts',
        'medicine', 'festivals', 'painting', 'pottery', 'clothing',
        'architecture', 'music', 'silk', 'language', 'paper'
    ],
    'food': [
        'food', 'peking-duck', 'dim-sum', 'hotpot', 'dumplings',
        'guoqiao-mixian', 'mapo-tofu', 'xiaolongbao'
    ],
    'utility': ['index', 'visa', 'transport', 'greatwall']
}

ALL_PAGES = []
for group in PAGE_GROUPS.values():
    ALL_PAGES.extend(group)

def check_lock():
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            if subprocess.run(['ps', '-p', str(pid)], capture_output=True).returncode == 0:
                log(f"[SKIP] 前一个任务仍在运行 (PID: {pid})")
                return True
        except (ValueError, FileNotFoundError):
            pass
        LOCK_FILE.unlink(missing_ok=True)
    return False

def set_lock():
    LOCK_FILE.write_text(str(os.getpid()))

def release_lock():
    LOCK_FILE.unlink(missing_ok=True)

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def get_todo_list():
    """从进度文件读取待办页面"""
    if not PROGRESS_FILE.exists():
        return None
    content = PROGRESS_FILE.read_text(encoding='utf-8')
    todos = []
    done = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- [ ]'):
            todos.append(line[6:].strip())
        elif line.startswith('- [x]'):
            done.append(line[6:].strip())
    return todos, done

def check_page_quality(page_name):
    """检查单个页面的多语言质量"""
    issues = []
    
    # 检查根页面
    root_path = BASE_DIR / f'{page_name}.html'
    if not root_path.exists():
        return [f'{page_name}.html: 根页面缺失']
    
    content = root_path.read_text(encoding='utf-8')
    
    # 1. language-switcher div
    if 'id="language-switcher"' not in content:
        issues.append(f'{page_name}.html: 缺少 language-switcher div')
    
    # 2. lang-switcher.js
    if '/js/lang-switcher.js' not in content:
        issues.append(f'{page_name}.html: 缺少 lang-switcher.js 引用')
    
    # 3. persist-lang.js
    if '/js/persist-lang.js' not in content:
        issues.append(f'{page_name}.html: 缺少 persist-lang.js 引用')
    
    # 4. hreflang 标签数量
    hreflangs = set(re.findall(r'hreflang="([^"]*)"', content))
    if len(hreflangs) < 8:
        issues.append(f'{page_name}.html: 只有 {len(hreflangs)}/8 hreflang 标签')
    
    # 5. 检查所有语言目录页面都存在
    for lang in LANGS:
        lang_path = BASE_DIR / lang / f'{page_name}.html'
        if not lang_path.exists():
            issues.append(f'{page_name}.html: {lang} 版本缺失')
    
    # 6. 检查语言目录页面的 language-switcher
    for lang in LANGS:
        lang_path = BASE_DIR / lang / f'{page_name}.html'
        if lang_path.exists():
            lang_content = lang_path.read_text(encoding='utf-8')
            if 'id="language-switcher"' not in lang_content:
                issues.append(f'{lang}/{page_name}.html: 缺少 language-switcher div')
    
    return issues

def auto_fix_page(page_name):
    """自动修复常见的页面问题"""
    base_url = 'https://travelchinaguide.dpdns.org'
    issues = check_page_quality(page_name)
    
    if not issues:
        return True, "无需修复"
    
    # 运行 generate-multilang.js 重新生成所有语言版本
    result = subprocess.run(
        ['node', 'scripts/generate-multilang.js'],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        return False, f"generate-multilang.js 失败: {result.stderr[:200]}"
    
    # 验证修复
    remaining = check_page_quality(page_name)
    if remaining:
        return False, f"修复后仍有问题: {'; '.join(remaining[:3])}"
    
    return True, "generate-multilang.js 重生成完成"

def run():
    log("="*50)
    log("China Travel Site - 页面质量检查")
    
    if check_lock():
        return
    
    set_lock()
    log("锁已获取")
    
    try:
        # 读取待办列表
        todo_data = get_todo_list()
        
        if todo_data is None:
            # 首次运行：创建进度文件
            create_initial_progress()
            log("待办列表已创建")
            return
        
        todos, done = todo_data
        
        if not todos:
            log("✅ 全部页面已完成，无需更多任务")
            return
        
        # 取第一个待办页面
        task = todos[0]
        log(f"📋 执行: {task}")
        
        # 解析任务（格式如 "beijing.html - 修复多语言问题"）
        page_name = task.split('.html')[0].strip()
        if not page_name:
            log(f"⚠️ 无法解析页面名: {task}")
            mark_done(task)
            return
        
        log(f"🔍 检查 {page_name}.html...")
        
        # 执行修复
        success, msg = auto_fix_page(page_name)
        
        if success:
            log(f"✅ {page_name}.html 修复完成")
        else:
            log(f"❌ {page_name}.html 修复失败: {msg}")
        
        # 标记完成（无论成功失败，避免卡死）
        mark_done(task)
        
        # Git 提交
        subprocess.run(['git', 'add', '-A'], cwd=BASE_DIR, capture_output=True)
        result = subprocess.run(
            ['git', 'commit', '-m', f'Auto: {page_name}.html 多语言检查修复'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=BASE_DIR, capture_output=True)
            log("📤 已提交并推送")
        else:
            log("ℹ️  无变更或提交失败")
        
# 清理 Cloudflare 缓存
        cf_token = os.environ.get('CF_API_TOKEN', '')
        if cf_token:
            subprocess.run([
                'curl', '-s', '-X', 'POST',
                'https://api.cloudflare.com/client/v4/zones/5020faaea9c504e81ba4943c527d2858/purge_cache',
                '-H', f'Authorization: Bearer {cf_token}',
                '-H', 'Content-Type: application/json',
                '--data', '{"purge_everything":true}'
            ], capture_output=True)
            log("🧹 Cloudflare 缓存已清理")
        else:
            log("⚠️ CF_API_TOKEN 未设置，跳过缓存清理")
        
    except Exception as e:
        log(f"❌ 异常: {e}")
    finally:
        release_lock()
        log("锁已释放")
        log(f"{'='*50}\n")

def create_initial_progress():
    """创建初始待办进度文件"""
    content = "# China Travel Site - 页面多语言修复进度\n\n"
    content += "## 按页面逐一修复\n\n"
    
    from datetime import datetime
    content += f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    content += "### 热门城市页面 (20)\n"
    for p in PAGE_GROUPS['hot_cities']:
        content += f"- [ ] {p}.html - 多语言检查修复\n"
    content += "\n"
    
    content += "### 文化页面 (16)\n"
    for p in PAGE_GROUPS['culture']:
        content += f"- [ ] {p}.html - 多语言检查修复\n"
    content += "\n"
    
    content += "### 美食页面 (8)\n"
    for p in PAGE_GROUPS['food']:
        content += f"- [ ] {p}.html - 多语言检查修复\n"
    content += "\n"
    
    content += "### 其他页面 (4)\n"
    for p in PAGE_GROUPS['utility']:
        content += f"- [ ] {p}.html - 多语言检查修复\n"
    content += "\n"
    
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(content, encoding='utf-8')
    log(f"待办列表已创建: {len(ALL_PAGES)} 个页面")

def mark_done(task):
    """标记任务为已完成"""
    if not PROGRESS_FILE.exists():
        return
    content = PROGRESS_FILE.read_text(encoding='utf-8')
    new_content = content.replace(f'- [ ] {task}', f'- [x] {task}')
    PROGRESS_FILE.write_text(new_content, encoding='utf-8')

if __name__ == '__main__':
    run()