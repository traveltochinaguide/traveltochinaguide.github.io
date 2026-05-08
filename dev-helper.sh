#!/bin/bash
# China Travel Site - 开发助手快捷脚本
# 用法：./dev-helper.sh [task]

set -e

WORKDIR="/home/ubuntu/traveltochinaguide.github.io"
PROGRESS_FILE="$HOME/.hermes/cron/china-travel-progress.md"
LOCKFILE="/tmp/hermes_china_travel.lock"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  China Travel Site - 开发助手${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

check_lock() {
    if [ -f "$LOCKFILE" ]; then
        local pid=$(cat "$LOCKFILE")
        if ps -p $pid > /dev/null; then
            echo -e "${YELLOW}⚠ 检测到运行中的任务 (PID: $pid)${NC}"
            echo "是否继续？(y/N)"
            read -r response
            if [[ "$response" != "y" ]]; then
                exit 0
            fi
        fi
        rm -f "$LOCKFILE"
    fi
}

set_lock() {
    echo $$ > "$LOCKFILE"
    trap "rm -f $LOCKFILE" EXIT
}

show_status() {
    echo -e "${GREEN}📊 当前状态:${NC}"
    echo ""
    
    # Git 状态
    cd "$WORKDIR"
    echo "Git 状态:"
    git status --short | head -10 || echo "  工作区干净"
    echo ""
    
    # 最近提交
    echo "最近提交:"
    git log --oneline -3 | sed 's/^/  /'
    echo ""
    
    # 进度文件
    if [ -f "$PROGRESS_FILE" ]; then
        echo "进度跟踪:"
        grep -E "^\- \[ |^\- \[x\]" "$PROGRESS_FILE" | head -10 | sed 's/^/  /'
    fi
    echo ""
}

run_task() {
    local task="$1"
    echo -e "${YELLOW}🚀 执行任务：$task${NC}"
    echo ""
    
    case "$task" in
        "analyze")
            # 分析项目结构
            echo "分析项目结构..."
            cd "$WORKDIR"
            echo "文件统计:"
            find . -name "*.html" | wc -l | xargs echo "  HTML 文件:"
            find . -name "*.js" | wc -l | xargs echo "  JS 文件:"
            find . -name "*.css" | wc -l | xargs echo "  CSS 文件:"
            echo ""
            echo "语言目录:"
            ls -d */ 2>/dev/null | grep -E "^(en|zh|ja|ko|ru|fr|de|es)/" | sed 's/^/  /'
            ;;
        
        "generate-languages")
            # 生成多语言页面
            echo "生成多语言页面..."
            cd "$WORKDIR"
            node scripts/generate-multilang.js
            echo -e "${GREEN}✓ 多语言生成完成${NC}"
            ;;
        
        "check-seo")
            # SEO 检查
            echo "SEO 检查..."
            cd "$WORKDIR"
            echo ""
            echo "Meta Description 检查:"
            grep -r "meta name=\"description\"" --include="*.html" . | wc -l | xargs echo "  找到的页面数:"
            echo ""
            echo "JSON-LD Schema 检查:"
            grep -r "application/ld+json" --include="*.html" . | wc -l | xargs echo "  包含 Schema 的页面数:"
            ;;
        
        "build")
            # 构建项目
            echo "构建项目..."
            cd "$WORKDIR"
            npm run build
            echo -e "${GREEN}✓ 构建完成${NC}"
            ;;
        
        "commit-push")
            # 提交并推送
            echo "提交并推送..."
            cd "$WORKDIR"
            git status
            echo ""
            read -p "输入提交信息: " message
            git add -A
            git commit -m "$message"
            git push origin main
            echo -e "${GREEN}✓ 推送成功${NC}"
            ;;
        
        *)
            echo -e "${RED}未知任务：$task${NC}"
            echo "可用任务：analyze, generate-languages, check-seo, build, commit-push"
            exit 1
            ;;
    esac
}

show_menu() {
    echo "可用任务:"
    echo "  1. analyze           - 分析项目结构"
    echo "  2. generate-languages - 生成多语言页面"
    echo "  3. check-seo         - SEO 检查"
    echo "  4. build             - 构建项目"
    echo "  5. commit-push       - 提交并推送"
    echo ""
    echo "或指定要执行的任务名称"
}

# 主程序
print_header
check_lock
set_lock

case "${1:-}" in
    "")
        show_status
        show_menu
        echo ""
        read -p "选择任务 (或输入任务名): " choice
        run_task "$choice"
        ;;
    "help"|"-h"|"--help")
        show_menu
        ;;
    *)
        run_task "$1"
        ;;
esac

echo ""
echo -e "${GREEN}✅ 任务完成${NC}"
