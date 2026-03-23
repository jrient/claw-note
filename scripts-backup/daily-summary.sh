#!/bin/bash
# OpenClaw 每日总结脚本
# 每天21:00运行，总结当日活动并更新MEMORY.md

WORKSPACE="/home/hongshu/.openclaw/workspace"
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"
LONGTERM_MEMORY="$WORKSPACE/MEMORY.md"

echo "=== OpenClaw 每日总结 $TODAY ===" 

# 检查今日记忆文件
if [ -f "$MEMORY_FILE" ]; then
    echo "今日活动:"
    cat "$MEMORY_FILE"
    echo ""
fi

# 检查SESSION-STATE
if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
    echo "当前会话状态:"
    cat "$WORKSPACE/SESSION-STATE.md"
    echo ""
fi

echo "总结完成。"