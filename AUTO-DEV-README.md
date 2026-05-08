# China Travel Site - 自动化开发系统

## 系统概述

这是一个基于 **Hermes Agent + Cron Job** 的自动化开发系统，用于持续开发和维护 `traveltochinaguide.github.io` 多语言旅游网站。

### 核心功能

- ✅ **自动内容丰富**: 为现有城市页面添加历史、美食、实用信息等
- ✅ **自动页面创建**: 生成新城市/专题的多语言页面（8 种语言）
- ✅ **自动 SEO 优化**: 检查并改进 meta 标签、Schema 标记
- ✅ **自动 Bug 修复**: 检测并修复网站问题
- ✅ **进度跟踪**: 基于文件的状态持久化，支持断点续跑
- ✅ **Git 自动化**: 自动提交、推送更改

---

## 架构设计

```
┌─────────────────────────────────────────────────────┐
│                   用户 (WeChat)                      │
│              查看进度 / 调整方向 / 审核               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Cron Job (每 30 分钟触发)                  │
│  触发条件：*/30 * * * *                              │
│  投递目标：WeChat (用户)                             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           Hermes Agent (开发助手)                    │
│  1. 读取进度文件 ~/.hermes/cron/china-travel-progress.md  │
│  2. 选择待办任务 (P0-P4 优先级)                       │
│  3. 执行 1-2 个具体任务                                │
│  4. 更新进度文件 + Git Commit                        │
│  5. 输出简短报告 (≤200 字)                            │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         项目仓库 (traveltochinaguide.github.io)      │
│  - 修改 HTML/JS/CSS                                  │
│  - 生成多语言版本 (8 种)                              │
│  - Git 提交推送                                       │
└─────────────────────────────────────────────────────┘
```

---

## 快速开始

### 1. 查看当前状态

```bash
# 查看进度
cat ~/.hermes/cron/china-travel-progress.md

# 查看 cron 任务状态
cronjob action="list"

# 查看项目 git 状态
cd ~/traveltochinaguide.github.io
git status
```

### 2. 手动触发任务

```bash
# 方式 1: 使用快捷脚本
cd ~/traveltochinaguide.github.io
./dev-helper.sh

# 方式 2: 运行 Python 脚本
python3 scripts/auto-dev-task.py --task status
python3 scripts/auto-dev-task.py --task enrich-beijing
python3 scripts/auto-dev-task.py --task check-seo

# 方式 3: 直接修改进度文件，等待 cron 自动执行
vim ~/.hermes/cron/china-travel-progress.md
```

### 3. 查看执行日志

```bash
# 查看最近一次 cron 输出
ls -lt ~/.hermes/cron/output/d610b933a5ea/ | head -3
cat ~/.hermes/cron/output/d610b933a5ea/$(ls -t ~/.hermes/cron/output/d610b933a5ea/ | head -1)

# 查看 git 提交历史
cd ~/traveltochinaguide.github.io
git log --oneline -10
```

---

## 任务优先级

系统按以下优先级选择任务：

| 优先级 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **P0** | Bug 修复 | 修复网站错误、功能异常 | 修复导航菜单在小屏幕不显示 |
| **P1** | 内容丰富 | 为现有页面添加内容 | 为北京页面添加 798 艺术区介绍 |
| **P2** | 新增页面 | 创建新城市/专题页面 | 创建南京页面 |
| **P3** | SEO 优化 | 改进搜索引擎优化 | 为所有页面添加 FAQ Schema |
| **P4** | 多语言 | 补充缺失翻译 | 完善俄语、西班牙语翻译 |

---

## 进度文件格式

进度文件位于 `~/.hermes/cron/china-travel-progress.md`，格式如下：

```markdown
# China Travel Site - 开发进度跟踪

## 当前状态
- **最近更新时间**: 2026-05-08 14:50
- **当前任务**: 丰富成都页面内容
- **完成进度**: 15%

## 待办事项列表

### P0 - 高优先级（Bug 修复）
- [ ] 检查所有页面的 hreflang 标签
- [ ] 验证 JSON-LD Schema 正确性

### P1 - 内容丰富（现有页面扩展）
- [ ] **北京页面**: 
  - [ ] 添加 798 艺术区介绍
  - [ ] 补充长城游览攻略
  - [ ] 添加美食推荐

### P2 - 新增页面
- [ ] 南京页面（中山陵、夫子庙）
- [ ] 杭州页面（西湖、灵隐寺）

### 已完成任务
- [x] 项目代码结构分析
- [x] 创建定时任务系统
```

---

## 自动化工作流

### 典型执行流程

1. **Cron 触发** (每 30 分钟)
   ```
   */30 * * * * → 触发 Hermes Agent
   ```

2. **Agent 启动**
   - 检查锁文件（防止并发）
   - 读取进度文件
   - 选择下一个待办任务

3. **执行任务** (以"丰富成都页面"为例)
   ```bash
   # 读取现有内容
   read_file chengdu.html
   
   # 分析缺失内容
   # - 缺少美食详细介绍
   # - 缺少实用交通信息
   
   # 生成新内容
   # - 添加麻婆豆腐、宫保鸡丁介绍
   # - 添加地铁线路说明
   
   # 更新翻译文件 (8 种语言)
   patch js/translations.js
   
   # 运行多语言生成器
   node scripts/generate-multilang.js
   ```

4. **提交更改**
   ```bash
   git add -A
   git commit -m "Auto: content - 丰富成都页面美食内容"
   git push origin main
   ```

5. **更新进度**
   ```markdown
   ## 2026-05-08 15:00
   - [x] 成都页面美食内容扩展
   ```

6. **输出报告** (≤200 字)
   ```
   [完成] content - 成都页面美食扩展
   - 添加 3 道川菜详细介绍
   - 补充 5 家老字号餐厅推荐
   - 更新 8 种语言翻译
   
   [下轮] 继续丰富西安页面历史内容
   
   [统计] 本次提交：+1,234 行，修改 3 个文件
   ```

---

## 自定义任务

### 添加新任务类型

编辑 `scripts/auto-dev-task.py`，添加新的处理函数：

```python
def my_custom_task():
    """自定义任务"""
    print("执行自定义任务...")
    # 你的逻辑
    return True

# 在 main() 中添加
if args.task == 'my-task':
    my_custom_task()
```

### 调整任务优先级

编辑 `~/.hermes/cron/china-travel-progress.md`，调整待办事项顺序：

```markdown
### P0 - 高优先级（Bug 修复）
- [ ] 紧急修复任务  # 会最先执行

### P1 - 内容丰富
- [ ] 重要内容更新  # 其次执行
```

---

## 故障排查

### 问题 1: Cron 任务未执行

**检查**:
```bash
# 查看 cron 状态
cronjob action="list"

# 查看 gateway 日志
grep "cron\|delivery" ~/.hermes/logs/gateway.log | tail -20
```

**解决**:
```bash
# 重启 cron
cronjob action="pause" job_id="d610b933a5ea"
cronjob action="resume" job_id="d610b933a5ea"
```

### 问题 2: Git 推送失败

**检查**:
```bash
cd ~/traveltochinaguide.github.io
git status
git remote -v
```

**解决**:
```bash
# 检查远程仓库配置
git remote set-url origin https://github.com/traveltochinaguide/traveltochinaguide.github.io

# 手动推送
git push origin main
```

### 问题 3: 多语言生成失败

**检查**:
```bash
cd ~/traveltochinaguide.github.io
node scripts/generate-multilang.js 2>&1 | head -50
```

**解决**:
```bash
# 重新安装依赖
npm install

# 检查 Node 版本
node -v  # 需要 16+
```

---

## 最佳实践

### ✅ 推荐做法

1. **小步快跑**: 每次 cron 只做 1-2 个小任务
2. **及时提交**: 完成就 commit，避免大量未提交更改
3. **多语言同步**: 添加内容时同时更新 8 种语言
4. **性能优先**: 图片压缩、代码精简
5. **进度跟踪**: 及时更新 `.task_progress.md`

### ❌ 避免做法

1. **大批量修改**: 一次性修改太多文件容易冲突
2. **跳过测试**: 修改后不检查直接推送
3. **忽略翻译**: 只更新英语不更新其他语言
4. **大文件提交**: 提交超过 1MB 的图片或资源

---

## 监控和维护

### 日常检查清单

- [ ] 查看最近一次 cron 执行日志
- [ ] 检查 git 提交是否正常
- [ ] 访问网站验证修改效果
- [ ] 查看进度文件更新情况

### 定期维护

- **每周**: 清理过期的进度文件
- **每月**: 检查 cron 任务健康状态
- **每季度**: 审查已完成任务，总结经验

---

## 资源链接

- **项目仓库**: https://github.com/traveltochinaguide/traveltochinaguide.github.io
- **在线网站**: https://travelchinaguide.dpdns.org
- **Hermes Agent 文档**: `skill_view('hermes-agent')`
- **Cron 监控技能**: `skill_view('cronjob-git-monitoring')`

---

## 联系和支持

如有问题，请查看：
1. 进度文件：`~/.hermes/cron/china-travel-progress.md`
2. Cron 日志：`~/.hermes/cron/output/d610b933a5ea/`
3. Git 历史：`git log --oneline -20`
