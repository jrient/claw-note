#!/bin/bash
# 任务注册表监控脚本
# 轻量级检测，不调用大模型

REGISTRY_FILE="$HOME/.openclaw/workspace/task-registry.json"
TELEGRAM_BOT="8407755939:AAGohngkXf_3aEJcTPK-2AeN_Yr_tSeTAkE"
TELEGRAM_CHAT="527599126"
LOG_FILE="$HOME/.openclaw/workspace/logs/task-monitor.log"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 发送Telegram通知
send_alert() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT}" \
        -d "text=${message}" \
        -d "parse_mode=Markdown" > /dev/null
}

# 检查任务状态
check_tasks() {
    if [ ! -f "$REGISTRY_FILE" ]; then
        log "Registry file not found"
        return
    fi
    
    current_time=$(date +%s)
    
    # 读取任务列表
    tasks=$(jq -r '.tasks | to_entries[] | @base64' "$REGISTRY_FILE" 2>/dev/null)
    
    if [ -z "$tasks" ]; then
        log "No tasks to check"
        return
    fi
    
    echo "$tasks" | while read -r task_b64; do
        task=$(echo "$task_b64" | base64 -d)
        task_id=$(echo "$task" | jq -r '.key')
        status=$(echo "$task" | jq -r '.value.status')
        last_update=$(echo "$task" | jq -r '.value.lastUpdate')
        timeout=$(echo "$task" | jq -r '.value.timeout // 300')
        retries=$(echo "$task" | jq -r '.value.retries // 0')
        max_retries=$(echo "$task" | jq -r '.value.maxRetries // 3')
        session_key=$(echo "$task" | jq -r '.value.sessionKey // ""')
        description=$(echo "$task" | jq -r '.value.description // "未知任务"')
        
        # 检查超时
        if [ "$status" = "running" ]; then
            update_time=$(date -d "$last_update" +%s 2>/dev/null || echo "0")
            elapsed=$((current_time - update_time))
            
            if [ "$elapsed" -gt "$timeout" ]; then
                log "Task $task_id TIMEOUT (elapsed: ${elapsed}s, timeout: ${timeout}s)"
                
                # 更新任务状态
                jq ".tasks[\"$task_id\"].status = \"timeout\"" "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp"
                mv "${REGISTRY_FILE}.tmp" "$REGISTRY_FILE"
                
                # 发送警报
                send_alert "⚠️ *任务超时*\n\n任务: $description\nID: \`$task_id\n超时: ${elapsed}秒\n\n请检查子代理状态"
            fi
        fi
        
        # 检查失败任务
        if [ "$status" = "failed" ]; then
            if [ "$retries" -lt "$max_retries" ]; then
                log "Task $task_id FAILED, can retry ($retries/$max_retries)"
                send_alert "❌ *任务失败*\n\n任务: $description\n重试次数: $retries/$max_retries\n\n发送 \`重试 $task_id\` 重新执行"
            fi
        fi
    done
    
    # 更新最后检查时间
    jq ".lastCheck = \"$(date -Iseconds)\"" "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp"
    mv "${REGISTRY_FILE}.tmp" "$REGISTRY_FILE"
}

# 主循环
log "Task monitor started"
check_tasks
log "Task monitor check completed"