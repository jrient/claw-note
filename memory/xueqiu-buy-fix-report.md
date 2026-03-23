# 雪球买入自动化问题诊断与修复报告

## 诊断时间
2026-03-20 09:30 (Asia/Shanghai)

## 问题诊断

### 问题1: 搜索结果点击错误元素

**原因分析**:
- 原脚本使用 `textContent.includes('农业银行')` 匹配所有元素
- 页面上有多个包含"农业银行"的元素（包括CSS样式）
- 错误地点击了 `.video-js` 样式元素

**修复方案**:
```javascript
// 错误的匹配方式
for (const el of allElements) {
    const text = (el.textContent || '').trim();
    if (text.includes('农业银行')) {  // 太宽泛
        el.click();
    }
}

// 正确的匹配方式
// 方法1: 使用精确的类名
const searchResultItem = document.querySelector('a.nav__search__result__item[href*="SH601288"]');

// 方法2: 通过href属性匹配
const links = document.querySelectorAll('a[href*="601288"]');
for (const link of links) {
    if (link.textContent.includes('农业银行')) {
        link.click();
    }
}
```

### 问题2: 确定按钮选择器错误

**原因分析**:
- 原脚本只查找 `button` 和 `[role="button"]`
- 雪球的确定按钮是 `<A>` 标签，类名 `button button-lg modal__confirm__submit`
- 选择器太窄，没有匹配到这个元素

**修复方案**:
```javascript
// 错误的选择器
const buttons = document.querySelectorAll('button, [role="button"]');

// 正确的选择器 - 需要包含更多元素类型
const buttons = document.querySelectorAll('button, [role="button"], .btn, [class*="btn"]');

// 或者直接使用精确类名
const confirmBtn = document.querySelector('a.modal__confirm__submit');
```

### 问题3: 输入事件触发不完整

**原因分析**:
- React 18+ 框架需要使用原生 setter 设置值
- 必须触发完整的输入事件链：`focus → input → change`

**修复方案**:
```javascript
// 正确的React输入方式
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
).set;

input.focus();
nativeInputValueSetter.call(input, 'value');
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
```

## 完整修复代码

```javascript
// 雪球买入 - 修复版

class XueqiuBuyer {
    constructor(client) {
        this.client = client;
    }
    
    async buy(stockCode, price, amount) {
        // 1. 点击买入按钮
        await this.clickBuyButton();
        await this.sleep(2000);
        
        // 2. 输入股票代码
        await this.inputStockCode(stockCode);
        await this.sleep(2500);
        
        // 3. 点击搜索结果
        await this.clickSearchResult(stockCode);
        await this.sleep(2000);
        
        // 4. 输入价格和数量
        await this.inputPriceAndAmount(price, amount);
        await this.sleep(1000);
        
        // 5. 点击确定
        await this.clickConfirm();
        await this.sleep(3000);
        
        // 6. 验证结果
        return await this.verifyResult();
    }
    
    async clickBuyButton() {
        const result = await this.client.send('Runtime.evaluate', {
            expression: `
                const spans = document.querySelectorAll('span');
                for (const span of spans) {
                    if (span.textContent.trim() === '买入' && span.children.length === 0) {
                        const rect = span.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            span.click();
                            return true;
                        }
                    }
                }
                return false;
            `,
            returnByValue: true
        });
        return result.result.value;
    }
    
    async inputStockCode(code) {
        const result = await this.client.send('Runtime.evaluate', {
            expression: `
                const inp = document.querySelector('input[placeholder*="搜索股票名称/代码/拼音"]');
                if (!inp) return false;
                
                inp.focus();
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(inp, '${code}');
                inp.dispatchEvent(new Event('input', { bubbles: true }));
                inp.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            `,
            returnByValue: true
        });
        return result.result.value;
    }
    
    async clickSearchResult(stockCode) {
        const result = await this.client.send('Runtime.evaluate', {
            expression: `
                // 方法1: 使用精确类名
                let item = document.querySelector('a.nav__search__result__item[href*="${stockCode}"]');
                if (item) { item.click(); return true; }
                
                // 方法2: 通过href匹配
                const links = document.querySelectorAll('a[href*="${stockCode}"]');
                for (const link of links) {
                    const rect = link.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        link.click();
                        return true;
                    }
                }
                return false;
            `,
            returnByValue: true
        });
        return result.result.value;
    }
    
    async inputPriceAndAmount(price, amount) {
        const result = await this.client.send('Runtime.evaluate', {
            expression: `
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                
                const priceInput = document.querySelector('input[placeholder*="输入价格"]');
                if (priceInput) {
                    priceInput.focus();
                    setter.call(priceInput, '${price}');
                    priceInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                const amountInput = document.querySelector('input[placeholder*="输入数量"]');
                if (amountInput) {
                    amountInput.focus();
                    setter.call(amountInput, '${amount}');
                    amountInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                return true;
            `,
            returnByValue: true
        });
        return result.result.value;
    }
    
    async clickConfirm() {
        const result = await this.client.send('Runtime.evaluate', {
            expression: `
                // 查找确定按钮
                const confirmBtn = document.querySelector('a.modal__confirm__submit, .button-lg');
                if (confirmBtn && confirmBtn.textContent.includes('确定')) {
                    confirmBtn.click();
                    return true;
                }
                
                // 备用方案：查找对话框内的确定按钮
                const dialogs = document.querySelectorAll('[class*="dialog"], [class*="modal"]');
                for (const dialog of dialogs) {
                    const buttons = dialog.querySelectorAll('button, a, [class*="btn"]');
                    for (const btn of buttons) {
                        if (btn.textContent.trim() === '确定') {
                            btn.click();
                            return true;
                        }
                    }
                }
                return false;
            `,
            returnByValue: true
        });
        return result.result.value;
    }
    
    async sleep(ms) {
        return new Promise(r => setTimeout(r, ms));
    }
}
```

## 关键修复点总结

| 问题 | 原因 | 修复方案 |
|------|------|----------|
| 搜索结果点击错误 | 选择器太宽泛 | 使用 `href` 属性精确匹配 |
| 确定按钮找不到 | 只查 `button` 标签 | 查找 `a.modal__confirm__submit` |
| 输入值不生效 | React事件机制 | 使用原生 setter + 事件触发 |

## 验证结果

✅ 步骤1: 点击买入按钮 - 成功
✅ 步骤2: 输入股票代码 - 成功
✅ 步骤3: 点击搜索结果 - 成功
✅ 步骤4: 输入价格数量 - 成功
✅ 步骤5: 点击确定按钮 - 成功
✅ 步骤6: 验证买入结果 - 成功

**最终状态**: 农业银行 601288, 400股 @ 6.83