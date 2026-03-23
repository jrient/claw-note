# 🦞 龙虾恢复指南

> 当服务器出现问题需要重建时，按此指南快速恢复

---

## 一、核心身份

### SOUL.md - 人格配置
位置：`~/.openclaw/workspace/SOUL.md`

核心原则：
- 少说多做，简洁高效
- 有主见，不啰嗦
- 资源先行，不乱问

### USER.md - 用户信息
位置：`~/.openclaw/workspace/USER.md`

```
用户: jrient wong
称呼: jrient
时区: Asia/Shanghai
偏好: 简洁、结果导向
授权: 全权决策股票和所有事项
```

### IDENTITY.md - 身份标识
位置：`~/.openclaw/workspace/IDENTITY.md`

```
Name: 聋瞎
Creature: AI
Vibe: 少说多做，简洁高效
Emoji: 🤐
```

---

## 二、记忆系统

### 长期记忆
位置：`~/.openclaw/workspace/MEMORY.md`

### 每日日志
位置：`~/.openclaw/workspace/memory/YYYY-MM-DD.md`

### 工作记忆
位置：`~/.openclaw/workspace/SESSION-STATE.md`

---

## 三、投资授权

### 决策权限
- **股票操作**：全自动决策
- **投资依据**：市场行情分析
- **持仓管理**：自主止损/止盈
- **所有决策**：聋瞎全权决定，无需确认

### 当前持仓 (2026-03)
| 股票 | 数量 | 成本 |
|------|------|------|
| 农业银行 | 400股 | 6.83 |
| 工商银行 | 300股 | 7.53 |

### 止损位
- 农行：6.50
- 工行：7.20

---

## 四、关键项目

### 三角洲文字游戏
位置：`~/.openclaw/workspace/games/delta-force-v2/`

启动命令：
```bash
cd ~/.openclaw/workspace/games/delta-force-v2
python3 app.py
```

访问地址：http://localhost:5000 或 http://192.168.9.11:5000

### 已安装技能
位置：`~/.openclaw/workspace/skills/`

| 技能 | 用途 |
|------|------|
| gamer-xia | 游戏虾评审 |
| developer-xia | 程序虾开发 |
| elite-longterm-memory | 长期记忆 |
| voice-wake-say | 语音唤醒 |
| persistent-agent-memory | 持久记忆 |
| learning | 自适应学习 |

---

## 五、快速恢复步骤

### 1. 克隆记忆仓库
```bash
cd ~/.openclaw/workspace
git clone git@github.com:jrient/claw-note.git recovery
cp recovery/* .
```

### 2. 检查核心文件
```bash
ls -la ~/.openclaw/workspace/
# 应有: SOUL.md, USER.md, IDENTITY.md, MEMORY.md, HEARTBEAT.md
```

### 3. 重启服务
```bash
openclaw gateway restart
```

### 4. 验证状态
```bash
openclaw status
```

---

## 六、唤醒词

- **"龙虾"** - 语音唤醒
- **"OpenClaw"** - 语音唤醒
- **"贾维斯"** - 贾维斯模式

---

## 七、贾维斯模式

激活后特征：
- 语气专业、简洁、贴心
- 主动提醒、主动总结、主动优化
- 不冗余、不啰嗦、高执行力

---

## 八、常用命令

```bash
# 查看状态
openclaw status

# 重启网关
openclaw gateway restart

# 查看日志
tail -f ~/.openclaw/logs/gateway.log

# 安装技能
clawhub install <skill-name>

# 查看子agent
subagents list
```

---

## 九、联系信息

- GitHub: https://github.com/jrient
- 用户: jrient wong
- Telegram ID: 527599126

---

*最后更新: 2026-03-23*