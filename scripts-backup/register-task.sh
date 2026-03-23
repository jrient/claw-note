#!/bin/bash
# 任务注册脚本 - 由子代理调用

REGISTRY_FILE="$HOME/.openclaw/workspace/task-registry.json"

# 用法: register-task.sh <task_id> <session_key> <description> [timeout_seconds]
TASK_ID="$1"
SESSION_KEY="$2"
DESCRIPTION="$3"
TIMEOUT="${4:-300}"

if [ -z "$TASK_ID" ] || [ -z "$SESSION_KEY" ]; then
    echo "Usage: $0 <task_id> <session_key> <description> [timeout]"
    exit 1
fi

# 确保文件存在
if [ ! -f "$REGISTRY_FILE" ]; then
    echo '{"tasks": {}, "lastCheck": null, "config": {"checkIntervalMs": 60000, "timeoutMs": 300000, "maxRetries": 3}}' > "$REGISTRY_FILE"
fi

# 注册任务
jq --arg id "$TASK_ID" \
   --arg key "$SESSION_KEY" \
   --arg desc "$DESCRIPTION" \
   --argjson timeout "$TIMEOUT" \
   '.tasks[$id] = {
       "sessionKey": $key,
       "description": $desc,
       "status": "running",
       "lastUpdate": (now | todate),
       "timeout": $timeout,
       "retries": 0,
       "maxRetries": 3,
       "progress": [],
       "createdAt": (now | todate)
   }' "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp"

mv "${REGISTRY_FILE}.tmp" "$REGISTRY_FILE"

echo "Task registered: $TASK_ID"