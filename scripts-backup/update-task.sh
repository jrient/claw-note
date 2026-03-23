#!/bin/bash
# 更新任务进度脚本 - 由子代理调用

REGISTRY_FILE="$HOME/.openclaw/workspace/task-registry.json"

# 用法: update-task.sh <task_id> <status> [progress_message]
TASK_ID="$1"
STATUS="$2"
PROGRESS="${3:-}"

if [ -z "$TASK_ID" ] || [ -z "$STATUS" ]; then
    echo "Usage: $0 <task_id> <status> [progress_message]"
    exit 1
fi

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "Registry file not found"
    exit 1
fi

# 更新任务
if [ -n "$PROGRESS" ]; then
    jq --arg id "$TASK_ID" \
       --arg status "$STATUS" \
       --arg progress "$PROGRESS" \
       '.tasks[$id].status = $status |
        .tasks[$id].lastUpdate = (now | todate) |
        .tasks[$id].progress += [$progress]' "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp"
else
    jq --arg id "$TASK_ID" \
       --arg status "$STATUS" \
       '.tasks[$id].status = $status |
        .tasks[$id].lastUpdate = (now | todate)' "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp"
fi

mv "${REGISTRY_FILE}.tmp" "$REGISTRY_FILE"

echo "Task updated: $TASK_ID -> $STATUS"