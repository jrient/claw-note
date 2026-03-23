# HEARTBEAT.md — 后台任务清单

> 心跳时检查这些任务

## 每日任务
- [ ] 早间行情提醒 (9:00)
- [ ] 盘中监控 (交易时间)
- [ ] 晚间总结 (21:00)

## 心跳频率
- 工作日: 每30分钟
- 周末: 每2小时
- 夜间 (23:00-8:00): 静默

## 检查项目
1. 股票监控告警
2. 日程提醒
3. 系统状态

## Self-Improving Check

- Read `./skills/self-improving/heartbeat-rules.md`
- Use `~/self-improving/heartbeat-state.md` for last-run markers and action notes
- If no file inside `~/self-improving/` changed since the last reviewed change, return `HEARTBEAT_OK`

---
*保持简洁，避免过度打扰*