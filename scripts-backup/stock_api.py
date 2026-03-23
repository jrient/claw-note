#!/usr/bin/env python3
"""
股票数据获取工具 - 使用腾讯财经API
腾讯API是目前唯一可用的免费A股API
"""

import urllib.request
import json
from typing import Dict, Optional, List

class StockAPI:
    """腾讯财经API封装"""
    
    BASE_URL = "http://qt.gtimg.cn/q="
    
    @staticmethod
    def get_quote(code: str) -> Optional[Dict]:
        """
        获取单只股票行情
        
        Args:
            code: 股票代码，如 "sh601288" 或 "601288"
        
        Returns:
            {
                "name": "农业银行",
                "code": "601288",
                "price": 6.53,
                "change": -0.23,
                "change_pct": -3.40,
                "open": 6.74,
                "prev_close": 6.76,
                "high": 6.75,
                "low": 6.50,
                "volume": 3260959,
                "amount": 2149395258,
                "time": "20260323120510"
            }
        """
        # 自动添加前缀
        if code.isdigit():
            if code.startswith('6'):
                code = f"sh{code}"
            else:
                code = f"sz{code}"
        
        url = f"{StockAPI.BASE_URL}{code}"
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = response.read().decode('gbk')
            
            if 'v_' not in data:
                return None
            
            # 解析数据
            parts = data.split('~')
            if len(parts) < 35:
                return None
            
            return {
                "name": parts[1],
                "code": parts[2],
                "price": float(parts[3]),
                "prev_close": float(parts[4]),
                "open": float(parts[5]),
                "volume": int(parts[6]),
                "high": float(parts[33]) if len(parts) > 33 and parts[33] else float(parts[3]),
                "low": float(parts[34]) if len(parts) > 34 and parts[34] else float(parts[3]),
                "amount": int(parts[37].split('/')[1]) if len(parts) > 37 and '/' in parts[37] else 0,
                "change": float(parts[31]) if len(parts) > 31 else 0,
                "change_pct": float(parts[32]) if len(parts) > 32 else 0,
                "time": parts[30] if len(parts) > 30 else ""
            }
        except Exception as e:
            print(f"Error fetching {code}: {e}")
            return None
    
    @staticmethod
    def get_quotes(codes: List[str]) -> Dict[str, Dict]:
        """获取多只股票行情"""
        # 自动添加前缀
        formatted_codes = []
        for code in codes:
            if code.isdigit():
                if code.startswith('6'):
                    formatted_codes.append(f"sh{code}")
                else:
                    formatted_codes.append(f"sz{code}")
            else:
                formatted_codes.append(code)
        
        url = f"{StockAPI.BASE_URL}{','.join(formatted_codes)}"
        
        results = {}
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = response.read().decode('gbk')
            
            for line in data.split(';'):
                if 'v_' not in line or '~' not in line:
                    continue
                
                parts = line.split('~')
                if len(parts) < 35:
                    continue
                
                code = parts[2]
                results[code] = {
                    "name": parts[1],
                    "code": code,
                    "price": float(parts[3]),
                    "prev_close": float(parts[4]),
                    "change": float(parts[31]),
                    "change_pct": float(parts[32])
                }
        except Exception as e:
            print(f"Error: {e}")
        
        return results
    
    @staticmethod
    def get_index() -> Dict[str, Dict]:
        """获取主要指数"""
        codes = ["sh000001", "sz399001", "sz399006", "sh000300"]
        return StockAPI.get_quotes(codes)


def test_api():
    """测试API"""
    print("=== 测试腾讯财经API ===")
    
    # 单只股票
    print("\n1. 单只股票测试:")
    quote = StockAPI.get_quote("sh601288")
    if quote:
        print(f"  {quote['name']}({quote['code']}): {quote['price']} ({quote['change_pct']}%)")
    
    # 多只股票
    print("\n2. 多只股票测试:")
    quotes = StockAPI.get_quotes(["601288", "601398", "600036"])
    for code, q in quotes.items():
        print(f"  {q['name']}: {q['price']} ({q['change_pct']}%)")
    
    # 指数
    print("\n3. 指数测试:")
    indices = StockAPI.get_index()
    for code, q in indices.items():
        print(f"  {q['name']}: {q['price']} ({q['change_pct']}%)")


if __name__ == "__main__":
    test_api()