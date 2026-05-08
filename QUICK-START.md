# China Travel Site - 快速参考卡

## 🎯 一分钟速查

### 系统状态
```bash
# 查看定时任务状态
cronjob action="list"

# 下次运行时间：每 30 分钟一次
# Job ID: d610b933a5ea
```

### 手动触发
```bash
cd ~/traveltochinaguide.github.io
./dev-helper.sh              # 交互式菜单
python3 scripts/auto-dev-task.py --task status  # 查看状态
```

### 查看进度
```bash
cat ~/.hermes/cron/china-travel-progress.md   # 进度文件
git log --oneline -5                          # 最近提交
```

---

## 📋 任务优先级

| 优先级 | 类型 | 说明 |
|--------|------|------|
| P0 | Bug 修复 | 网站错误、功能异常 |
| P1 | 内容丰富 | 扩展现有页面 |
| P2 | 新增页面 | 新城市/专题 |
| P3 | SEO 优化 | meta、Schema |
| P4 | 多语言 | 翻译完善 |

---

## 🔧 常用命令

```bash
# 查看 cron 输出日志
ls -lt ~/.hermes/cron/output/d610b933a5ea/ | head -3

# 查看 git 状态
cd ~/traveltochinaguide.github.io && git status --short

# 暂停/恢复 cron
cronjob action="pause" job_id="d610b933a5ea"
cronjob action="resume" job_id="d610b933a5ea"

# 运行 SEO 检查
python3 scripts/auto-dev-task.py --task check-seo
```

---

## 📁 关键文件

| 文件 | 用途 |
|------|------|
| `~/.hermes/cron/china-travel-progress.md` | 进度跟踪 |
| `~/traveltochinaguide.github.io/dev-helper.sh` | 快捷脚本 |
| `~/traveltochinaguide.github.io/AUTO-DEV-README.md` | 完整文档 |
| `~/.hermes/skills/china-travel-site-dev/SKILL.md` | 开发规范 |

---

## 🎯 当前待办

### P1 - 内容丰富
- [ ] 北京：798 艺术区、长城攻略
- [ ] 上海：外滩历史、迪士尼
- [ ] 成都：熊猫基地、锦里

### P2 - 新增页面
- [ ] 南京、杭州、苏州
- [ ] 专题：高铁攻略、节日文化

---

## ⚠️ 注意事项

- ✅ 消息≤200 字（微信限制）
- ✅ 图片用 WebP 格式
- ✅ 多语言同步更新
- ✅ 小步快跑，及时提交

---

**详细文档**: `AUTO-DEV-README.md`  
**技能文档**: `skill_view('china-travel-site-dev')`
