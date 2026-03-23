# 火焰反应实现

## Telegram API方法

使用 `setMessageReaction` API直接给消息添加反应：

```bash
curl -s "https://api.telegram.org/bot<BOT_TOKEN>/setMessageReaction" \
  -d "chat_id=<CHAT_ID>" \
  -d "message_id=<MESSAGE_ID>" \
  -d 'reaction=[{"type":"emoji","emoji":"🔥"}]' \
  -d "is_big=false"
```

## 配置信息

- Bot Token: 从 openclaw.json 获取
- Chat ID: 527599126
- Emoji: 🔥

## 实现位置

收到用户消息后，在回复内容前调用API添加反应。