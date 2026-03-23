#!/usr/bin/env python3
"""
A股市场快报生成脚本
使用新浪财经和东方财富API获取市场数据
"""

import requests
import json
from datetime import datetime

def get_index_quote():
    """获取主要指数行情（新浪财经）"""
    codes = ['sh000001', 'sz399001', 'sz399006']
    url = f"https://hq.sinajs.cn/list={','.join(['s_' + c for c in codes])}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn',
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        data = {}
        for line in r.text.strip().split('\n'):
            if 'var hq_str_s_' in line:
                # 解析: var hq_str_s_sh000001="上证指数,3957.0527,-49.4996,-1.24,6667983,96486311";
                parts = line.split('"')
                if len(parts) >= 2:
                    code_part = line.split('s_')[1].split('=')[0]
                    values = parts[1].split(',')
                    if len(values) >= 6:
                        name = values[0]
                        price = float(values[1])
                        change = float(values[2])
                        change_pct = float(values[3])
                        volume = int(values[4])  # 万手
                        amount = float(values[5])  # 万元
                        
                        data[code_part] = {
                            'name': name,
                            'price': price,
                            'change': change,
                            'change_pct': change_pct,
                            'volume': volume,
                            'amount': amount
                        }
        return data
    except Exception as e:
        print(f"获取指数失败: {e}")
        return None

def get_sector_rank_sina():
    """获取板块涨跌排行（新浪财经）"""
    # 新浪板块接口
    url = "http://vip.stock.finance.sina.com.cn/q/go.new/ddx.v2data/fl"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://vip.stock.finance.sina.com.cn',
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        return r.text
    except:
        return None

def get_north_money():
    """获取北向资金（尝试多个数据源）"""
    # 尝试使用新浪财经
    url = "https://hq.sinajs.cn/list=hk_sh,hk_sz"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn',
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            # 解析北向资金数据
            return r.text
    except:
        pass
    
    return None

def main():
    """生成市场报告"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    report = f"""# A股市场快报 ({date_str} {time_str})

## 主要指数
"""
    
    # 获取指数数据
    index_data = get_index_quote()
    if index_data:
        report += "| 指数 | 点位 | 涨跌 | 涨跌幅 |\n"
        report += "|------|------|------|--------|\n"
        
        for code, data in index_data.items():
            sign = "+" if data['change'] >= 0 else ""
            report += f"| {data['name']} | {data['price']:.2f} | {sign}{data['change']:.2f} | {sign}{data['change_pct']:.2f}% |\n"
    else:
        report += "\n*指数数据获取失败*\n"
    
    # 板块排行
    report += "\n## 热门板块\n\n"
    report += "*注：板块数据暂时无法获取，可能是非交易时间或网络问题*\n"
    
    # 北向资金
    report += "\n## 北向资金\n\n"
    north_data = get_north_money()
    if north_data:
        report += f"```\n{north_data}\n```\n"
    else:
        report += "*北向资金数据暂时无法获取*\n"
    
    # 简要分析
    report += "\n## 简要分析\n\n"
    if index_data:
        sh = index_data.get('sh000001', {})
        if sh:
            trend = "下跌" if sh.get('change', 0) < 0 else "上涨"
            report += f"- 上证指数{trend}，当前点位{sh.get('price', 0):.2f}点\n"
        
        cyb = index_data.get('sz399006', {})
        if cyb:
            trend = "走强" if cyb.get('change', 0) > 0 else "走弱"
            report += f"- 创业板指{trend}，涨跌幅{cyb.get('change_pct', 0):.2f}%\n"
    else:
        report += "- 数据获取失败，无法进行分析\n"
    
    report += "\n---\n"
    report += f"*数据来源：新浪财经 | 生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return report

if __name__ == '__main__':
    print(main())