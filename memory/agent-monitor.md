# Agent监控与故障处理流程

## 问题背景
Agent可能显示"running"状态，但实际已卡住无响应。不能只看状态，必须核实是否真的在工作。

## 检查流程

### 1. 状态检查
```bash
subagents action=list recentMinutes=60
```
查看：
- `status` 是否为 `running`
- `runtime` 运行时间是否异常长（>10分钟无更新）
- `recent` 列表是否为空（空=近期无完成）

### 2. 核实真实进度
```bash
sessions_history sessionKey=<agent-key> limit=5
```
检查：
- 最后一条消息的时间戳
- 最后的工具调用是什么
- 是否有长时间无响应

### 3. 判断卡住的标准
- ✗ 运行>15分钟 + 最后活动>10分钟前
- ✗ 查看history最后消息时间太久
- ✗ 无新工具调用
- ✗ 没有任何输出

### 4. 处理流程
```bash
# 1. Kill卡住的agent
subagents action=kill target=<label>

# 2. 检查是否有遗留进程
process action=list

# 3. 重新派发（注意避免相同卡点）
sessions_spawn label=<label>-v2 task="..." mode=run
```

## 注意事项

1. **不要被status蒙蔽** - `running`不代表在工作
2. **看历史消息** - 最后活动时间才是真实状态
3. **运行时间** - >10分钟无更新=可疑
4. **避免相同卡点** - 重派发时排除会导致卡住的操作（如重启gateway）

## 记录模板

```
**Agent检查：**

| Agent | 状态 | 运行时间 | 最后活动 | 判断 |
|-------|------|----------|----------|------|
| xxx | running | 15分钟 | 10分钟前 | ⚠️ 卡住 |
| yyy | running | 5分钟 | 刚刚 | ✅ 正常 |
```

## 案例

### 2026-03-20 ops-api卡住
- 状态：running 27分钟
- 最后活动：重启gateway后无响应
- 处理：kill + 重新派发v2

### 2026-03-20 dev-frontend卡住
- 状态：running 32分钟
- 最后活动：检查Docker后无响应
- 处理：kill + 重新派发v2

---

**记住：** 状态会骗人，历史消息不会。

---

# 工作质量要求

## 查资料要认真
- ❌ 不能瞎编参数
- ❌ 不能随便填数字
- ✓ 必须查官方文档
- ✓ 查不到就说查不到，不要乱写

## 错误案例
2026-03-20 maxTokens参数错误
- 错误：GLM-5写了4096，实际应该是8192
- 原因：没有认真查官方文档
- 教训：查不到就问用户，不要编