# MEMORY.md - 长期记忆中枢

> 🧠 这是聋瞎的永久记忆库，存储重要的决策、偏好、教训和关键信息。

## 用户画像

### jrient wong
- **称呼**: jrient
- **时区**: Asia/Shanghai (GMT+8)
- **沟通风格**: 喜欢简洁，不喜欢废话
- **核心偏好**: 少说多做、无需询问直接执行

## 消息反应规则

### 火焰反应机制
- **收到消息时** → 系统自动添加 🔥 确认反应
- **任务完成后** → 添加 👍 反应
- **触发词**："火花反应" → 添加 🔥 确认收到
- **禁止**: 消息内发表情文字（如"🔥"、"👍"）

## 当前持仓 (2026-04-09 收盘)

| 代码 | 名称 | 数量 | 成本 | 现价 | 市值 | 盈亏 |
|------|------|------|------|------|------|------|
| 601288 | 农业银行 | 400股 | 6.83 | 6.76 | 2,704元 | -28元 (-1.02%) |
| 601398 | 工商银行 | 300股 | 7.53 | 7.46 | 2,238元 | -21元 (-0.93%) |

**账户状态 (2026-04-14 收盘)**
- 持仓市值：4,942元
- 累计浮亏：-49元 (-0.98%)
- 止损线：-8%（当前安全）

## 定时任务

### 每日任务
- **09:00** 早间行情提醒
- **交易时间** 盘中监控（每10分钟检查止损）
- **14:30** A股收盘快报
- **21:00** 晚间总结

### 182云服务器
- **IP**: 182.92.94.214
- **用户**: root → su claude
- **定时任务**: 每天 6:00 国际要闻 + Claude Code更新检查
- **日志**: `/data/project/logs/daily-news.log`

## 技能矩阵

### 职责分工 (2026-03-27)
- **我（聋瞎）**：任务记录、分配任务、收集进度、汇报结果
- **人贩子虾**：创建agent虾执行实际工作
- **重要**：聋瞎不做实际操作，只做协调和汇报。所有任务由人贩子虾创建agent虾执行

### 已装载技能
- **运维虾** (`skills/ops-xia`) - 系统运维和故障排查
- **测试虾** - 小说平台测试
- **开发者虾** (`developer-xia`) - 游戏开发
- **游戏虾** (`gamer-xia`) - 游戏评审
- **context-manager** - 上下文自动管理

### 创建的工具
- `scripts/check-large-files.sh` - 大文件检查（>100KB预警）

## 已安装插件

- **openclaw-weixin** (v2.0.1) - 微信扫码登录插件
  - 安装命令: `npx -y @tencent-weixin/openclaw-weixin-cli@latest install`
  - 扫码链接格式: `https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=xxx&bot_type=3`

## 项目文档

### 方案文档
- **企业物资存管系统** - 完整版已分割至 `docs/material-system/`
  - 主索引: `docs/material-system/INDEX.md`
  - 完整版备份: `docs/material-system/full-document.md.bak` (~260KB)
  - 精简版: `docs/企业物资存管系统小程序方案文档.md` (<1KB)

### 测试报告
- `docs/小说平台扩写模块测试报告.md` - 测试虾执行

## 重要教训

### 1. 编辑工具冲突 (2026-03-23)
- `write` 和 `edit` 不能混用
- 用 `write` 后不再用 `edit`

### 2. API输入长度限制 (2026-03-27)
- 阿里云百炼API限制: **202,752字符**
- 大文件(>100KB)会导致 `HTTP 400: Range of input length should be [1, 202752]`
- 解决: 分割大文件，主文件保持<50KB

### 3. 脚本权限问题 (2026-03-27)
- cron任务脚本需要执行权限
- 解决: `chmod +x scripts/*.sh`

### 4. 技能reference目录超限 (2026-03-27)
- tushare-finance技能reference目录1.5MB，远超202KB API限制
- 根因: `接口文档/`子目录含207个md文件共1.1M未清理
- 解决: 整个目录移出压缩为 `tushare-api-docs-backup.tar.gz`
- 预防: 技能reference总大小 < 500KB，单文件 < 20KB
- **教训**: 压缩文件在reference目录内无效，必须移出reference目录

## 关键配置

### API最大上下文处理机制
- **阿里云百炼API限制**: 202,752字符
- **超限错误**: `HTTP 400: Range of input length should be [1, 202752]`
- **预防措施**:
  - 技能reference目录总大小 < 500KB
  - 单个md文件 < 20KB
  - 超过50KB的文档压缩存档，不放入reference
  - 大文件必须移出reference目录，不能仅压缩
- **检查命令**:
  ```bash
  find ~/.openclaw/workspace -name "*.md" -type f -exec wc -c {} \; | sort -rn | head -10
  du -sh ~/.openclaw/workspace/skills/*/reference/
  ```

### API Keys
- **novel.al.jrient.cn**: dtMH2F5t5PNYfmAgnadg23mmxmN4NiLWXMKrYmh7bvBCXelxG9jzFDFWmHKHjQMS

### 服务器
- **182云**: 182.92.94.214 (root) - jrient指定服务器

### 本机信息
- **锁屏密码**: hongshu888
- **截图方式**: spectacle（Wayland环境）
- **API限制**: 202,752字符

---
*最后更新: 2026-04-02 08:00*