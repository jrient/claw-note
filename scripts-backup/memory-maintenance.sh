#!/bin/bash
# OpenClaw 记忆维护脚本
# 定期清理过期记忆，保留重要内容

WORKSPACE="/home/hongshu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LONGTERM_MEMORY="$WORKSPACE/MEMORY.md"

# 保留最近30天的每日记忆
find "$MEMORY_DIR" -name "*.md" -mtime +30 -delete 2>/dev/null

# 检查记忆文件大小
MEMORY_SIZE=$(wc -c < "$LONGTERM_MEMORY" 2>/dev/null || echo 0)
if [ "$MEMORY_SIZE" -gt 50000 ]; then
    echo "警告: MEMORY.md 超过50KB，建议整理"
fi

echo "记忆维护完成 $(date)"