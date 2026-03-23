#!/usr/bin/env python3
"""
股票价格监控脚本
监控持仓股票，触发止损/止盈时发送通知
"""

import urllib.request
import json
import subprocess
from datetime import datetime

# 持仓配置
HOLDINGS = [
    {"code": "sh601288", "name": "农业银行", "shares": 400, "cost": 6.83, "stop_loss": 6.30},
    {"code": "sh601398", "name": "工商银行", "shares": 300, "cost": 7.53, "stop_loss": 7.00},
]

# 通知阈值
STOP_LOSS_THRESHOLD = 0.02  # 距止损2%时预警
ALERT_FILE = "/tmp/stock-alert-sent.json"

def get_quote(code):
    """获取股票行情"""
    url = f"http://qt.gtimg.cn/q={code}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read().decode('gbk')
        parts = data.split('~')
        if len(parts) < 35:
            return None
        return {
            "price": float(parts[3]),
            "change_pct": float(parts[32]),
            "name": parts[1]
        }
    except:
        return None

def send_alert(title, message):
    """发送Telegram通知"""
    bot_token = "8407755939:AAGohngkXf_3aEJcTPK-2AeN_Yr_tSeTAkE"
    chat_id = "527599126"
    
    text = f"⚠️ {title}\n\n{message}"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

def check_alert_sent(code, alert_type):
    """检查是否已发送过该类型警报"""
    try:
        with open(ALERT_FILE, 'r') as f:
            sent = json.load(f)
        key = f"{code}_{alert_type}"
        today = datetime.now().strftime("%Y-%m-%d")
        return sent.get(key) == today
    except:
        return False

def mark_alert_sent(code, alert_type):
    """标记已发送警报"""
    try:
        with open(ALERT_FILE, 'r') as f:
            sent = json.load(f)
    except:
        sent = {}
    
    key = f"{code}_{alert_type}"
    sent[key] = datetime.now().strftime("%Y-%m-%d")
    
    with open(ALERT_FILE, 'w') as f:
        json.dump(sent, f)

def monitor():
    """监控主函数"""
    alerts = []
    
    for holding in HOLDINGS:
        quote = get_quote(holding["code"])
        if not quote:
            continue
        
        price = quote["price"]
        stop_loss = holding["stop_loss"]
        distance_to_stop = (price - stop_loss) / stop_loss
        
        # 检查止损预警（距离止损2%以内）
        if distance_to_stop <= STOP_LOSS_THRESHOLD and not check_alert_sent(holding["code"], "stop_warning"):
            loss = (price - holding["cost"]) * holding["shares"]
            alert_msg = f"{holding['name']} {price}\n距止损 {distance_to_stop*100:.1f}%\n当前盈亏 {loss:.0f}元"
            send_alert("止损预警", alert_msg)
            mark_alert_sent(holding["code"], "stop_warning")
            alerts.append(f"{holding['name']}: 止损预警已发送")
        
        # 检查止损触发
        if price <= stop_loss and not check_alert_sent(holding["code"], "stop_triggered"):
            loss = (price - holding["cost"]) * holding["shares"]
            alert_msg = f"{holding['name']} {price}\n已触发止损线 {stop_loss}\n当前亏损 {loss:.0f}元"
            send_alert("🚨 止损触发", alert_msg)
            mark_alert_sent(holding["code"], "stop_triggered")
            alerts.append(f"{holding['name']}: 止损触发已发送")
    
    return alerts

if __name__ == "__main__":
    print(f"[{datetime.now()}] 股票监控检查...")
    alerts = monitor()
    if alerts:
        for a in alerts:
            print(f"  - {a}")
    else:
        print("  无警报")