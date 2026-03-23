#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股市场快报生成器
数据来源：腾讯财经API + 东方财富API（禁用代理）
"""

import requests
import json
import re
import os
from datetime import datetime

# 禁用代理
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# 创建不使用代理的session
session = requests.Session()
session.trust_env = False  # 忽略环境变量中的代理设置

def get_tencent_index_data():
    """使用腾讯财经API获取指数数据"""
    codes = ["sh000001", "sz399001", "sz399006"]
    url = "https://web.sqt.gtimg.cn/q=" + ",".join(codes)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://gu.qq.com/"
    }
    
    try:
        resp = session.get(url, headers=headers, timeout=15)
        resp.encoding = 'gbk'
        text = resp.text
        
        indices = []
        for line in text.strip().split('\n'):
            if not line:
                continue
            
            match = re.match(r'v_(\w+)="(.*)"', line.strip())
            if match:
                code = match.group(1)
                data = match.group(2).split('~')
                
                if len(data) >= 35:
                    name = data[1]
                    price = float(data[3]) if data[3] else 0
                    yesterday = float(data[4]) if data[4] else 0
                    change = price - yesterday if yesterday > 0 else 0
                    change_pct = (change / yesterday * 100) if yesterday > 0 else 0
                    
                    indices.append({
                        "name": name,
                        "code": code,
                        "price": price,
                        "change": change,
                        "change_pct": change_pct
                    })
        
        return indices
    except Exception as e:
        print(f"获取指数数据失败: {e}")
        return []

def get_eastmoney_sectors():
    """获取板块数据"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "fid": "f3",
        "po": "1",
        "pz": "50",
        "pn": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fs": "m:90+t:2",
        "fields": "f12,f14,f2,f3"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://quote.eastmoney.com",
        "Accept": "application/json"
    }
    
    try:
        resp = session.get(url, params=params, headers=headers, timeout=15)
        data = resp.json()
        
        sectors = []
        if data and "data" in data and "diff" in data["data"]:
            for item in data["data"]["diff"]:
                name = item.get("f14", "")
                change_pct = item.get("f3", 0)
                
                if isinstance(change_pct, (int, float)):
                    sectors.append({
                        "name": name,
                        "change_pct": change_pct / 100
                    })
        
        sorted_sectors = sorted(sectors, key=lambda x: x["change_pct"], reverse=True)
        return {
            "top5": sorted_sectors[:5],
            "bottom5": sorted_sectors[-5:] if len(sorted_sectors) >= 5 else []
        }
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        return {"top5": [], "bottom5": []}

def get_north_money():
    """获取北向资金"""
    # 方法1: 使用东财数据中心接口
    try:
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "pageSize": 1,
            "pageNumber": 1,
            "reportName": "RPT_MUTUAL_STOCK_FUND_FLOW",
            "columns": "TRADE_DATE,NET_INFLOW",
            "_": str(int(datetime.now().timestamp() * 1000))
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        resp = session.get(url, params=params, headers=headers, timeout=15)
        data = resp.json()
        
        if data and "result" in data and "data" in data["result"]:
            item = data["result"]["data"][0]
            inflow = float(item.get("NET_INFLOW", 0)) / 100000000  # 转换为亿
            return {
                "date": item.get("TRADE_DATE", ""),
                "net_inflow": inflow
            }
    except Exception as e:
        print(f"获取北向资金失败(方法1): {e}")
    
    # 方法2: 使用简化接口
    try:
        url2 = "https://push2.eastmoney.com/api/qt/stock/get"
        params2 = {
            "secid": "1.000001",
            "fields": "f62,f184",
            "ut": "b2884a393a59ad64002292a3e90d46a5"
        }
        
        headers2 = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://quote.eastmoney.com"
        }
        
        resp2 = session.get(url2, params=params2, headers=headers2, timeout=15)
        data2 = resp2.json()
        
        if data2 and "data" in data2:
            # f62是北向资金流入
            inflow = data2["data"].get("f62", 0)
            if isinstance(inflow, (int, float)):
                return {"net_inflow": inflow / 100000000}  # 转换为亿
    except Exception as e:
        print(f"获取北向资金失败(方法2): {e}")
    
    return {"net_inflow": 0, "note": "暂不可用"}

def format_report(indices, sectors, north_money):
    """格式化报告"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    report = f"""## A股市场快报 ({date_str})

### 主要指数
| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
"""
    
    for idx in indices:
        change_sign = "+" if idx["change_pct"] >= 0 else ""
        report += f"| {idx['name']} | {idx['price']:.2f} | {change_sign}{idx['change_pct']:.2f}% |\n"
    
    if not indices:
        report += "| 数据获取中 | - | - |\n"
    
    report += "\n### 热门板块\n\n**涨幅前5：**\n"
    for s in sectors["top5"]:
        report += f"- {s['name']} (+{s['change_pct']:.2f}%)\n"
    if not sectors["top5"]:
        report += "- 数据获取中\n"
    
    report += "\n**跌幅前5：**\n"
    for s in sectors["bottom5"]:
        change_sign = "+" if s["change_pct"] >= 0 else ""
        report += f"- {s['name']} ({change_sign}{s['change_pct']:.2f}%)\n"
    if not sectors["bottom5"]:
        report += "- 数据获取中\n"
    
    report += "\n### 北向资金\n"
    if "note" in north_money:
        report += f"- {north_money.get('note', '数据获取中')}\n"
    else:
        inflow = north_money.get("net_inflow", 0)
        sign = "+" if inflow >= 0 else ""
        report += f"- 净流入/流出：{sign}{inflow:.2f}亿\n"
    
    # 简要分析
    report += "\n### 简要分析\n"
    if indices:
        up_count = sum(1 for idx in indices if idx["change_pct"] > 0)
        down_count = sum(1 for idx in indices if idx["change_pct"] < 0)
        
        if up_count > down_count:
            report += "- 市场整体上涨，情绪积极\n"
        elif down_count > up_count:
            report += "- 市场整体下跌，情绪谨慎\n"
        else:
            report += "- 市场分化，结构性行情\n"
        
        if sectors["top5"]:
            top_sector = sectors["top5"][0]
            report += f"- 领涨板块：{top_sector['name']}，涨幅{top_sector['change_pct']:.2f}%\n"
        if sectors["bottom5"]:
            bottom_sector = sectors["bottom5"][-1]
            report += f"- 跌幅较大：{bottom_sector['name']}，跌幅{abs(bottom_sector['change_pct']):.2f}%\n"
    else:
        report += "- 当前为非交易时段或数据暂不可用\n"
    
    return report

def main():
    print("正在获取市场数据...\n")
    
    # 获取各类数据
    indices = get_tencent_index_data()
    sectors = get_eastmoney_sectors()
    north_money = get_north_money()
    
    # 生成报告
    report = format_report(indices, sectors, north_money)
    
    # 保存到文件
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"/home/hongshu/.openclaw/workspace/memory/market-hourly-{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"\n---\n已保存到 {filename}")

if __name__ == "__main__":
    main()