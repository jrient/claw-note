#!/bin/bash
# 每日记忆备份脚本
# 将记忆文件同步到GitHub仓库

set -e

WORKSPACE="/home/hongshu/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE/claw-note"
LOG_FILE="$WORKSPACE/logs/memory-backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log "===== 开始记忆备份 ====="

# 进入备份目录
cd "$BACKUP_DIR"

# 复制最新记忆文件
log "复制记忆文件..."
cp "$WORKSPACE/MEMORY.md" . 2>/dev/null || true
cp "$WORKSPACE/SOUL.md" . 2>/dev/null || true
cp "$WORKSPACE/USER.md" . 2>/dev/null || true
cp "$WORKSPACE/IDENTITY.md" . 2>/dev/null || true
cp "$WORKSPACE/RECOVERY.md" . 2>/dev/null || true
cp "$WORKSPACE/HEARTBEAT.md" . 2>/dev/null || true

# 复制每日日志
log "复制每日日志..."
cp -r "$WORKSPACE/memory/"* ./memory/ 2>/dev/null || true

# Git提交
log "Git提交..."
git add -A
git commit -m "chore: 每日记忆备份 $(date '+%Y-%m-%d %H:%M')" || log "无变更需要提交"

# 推送到远程
log "推送到GitHub..."
git push origin main || log "推送失败，可能网络问题"

log "===== 备份完成 ====="
log ""