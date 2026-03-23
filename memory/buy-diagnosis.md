# 雪球买入操作诊断报告

## 诊断时间
2026-03-20 09:12 (Asia/Shanghai)

## 诊断步骤和结果

### 1. 页面状态
- URL: https://xueqiu.com/performance
- 页面标题: 持仓盈亏 - 雪球
- Chrome调试端口: 9222 (正常运行)

### 2. 买入按钮定位
- 找到3个"买入"元素
- 主要按钮: `<SPAN>` 元素，位置 (599, 377)，尺寸 26x15
- **状态: ✓ 正常**

### 3. 点击买入后
- 模态框数量: 246 (对话框成功弹出)
- 输入框 `placeholder="搜索股票名称/代码/拼音"` 可见
- **状态: ✓ 正常**

### 4. 输入股票代码 601288
- 搜索结果显示: 农业银行
- **状态: ✓ 正常**

### 5. 选择股票后
- 价格输入框可见 ✓
- 数量输入框可见 ✓
- **状态: ✓ 正常**

### 6. 输入价格 6.83 和数量 400
- **状态: ✓ 正常**

### 7. 点击确认按钮
- 找到2个按钮: "买入"(557, 377) 和 "确定"(506, 674)
- 点击"确定"按钮
- **状态: ✓ 正常**

### 8. 最终结果
- 持仓已更新: 农业银行 400股
- 总市值: 2732.00 元
- **状态: ✓ 买入成功**

---

## 可能的问题原因

用户报告"自动化失败"，但本次诊断显示流程正常。可能原因：

1. **时序问题**
   - 脚本等待时间不足
   - 建议: 增加延迟，特别是输入后等待

2. **元素选择器问题**
   - 页面上有多个"买入"按钮
   - 脚本可能点击了错误的按钮
   - 建议: 精确选择叶子节点元素

3. **输入事件问题**
   - 必须触发 `input` 和 `change` 事件
   - 否则值不会真正填入

4. **焦点问题**
   - 输入框可能没有正确获得焦点
   - 建议: 先调用 `focus()` 再设置值

---

## 修复建议

### 推荐的买入脚本结构

```javascript
// 1. 点击买入按钮 - 精确选择叶子节点
await page.evaluate(() => {
  const all = document.querySelectorAll('*');
  for (const el of all) {
    if (el.innerText?.trim() === '买入' && el.children.length === 0) {
      el.click();
      return;
    }
  }
});
await delay(2000);  // 等待对话框打开

// 2. 输入股票代码 - 触发完整事件
await page.evaluate(() => {
  const inp = document.querySelector('input[placeholder*="搜索股票名称"]');
  if (inp) {
    inp.focus();
    inp.value = '601288';
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new Event('change', { bubbles: true }));
  }
});
await delay(2000);  // 等待搜索结果

// 3. 选择股票
await page.evaluate(() => {
  const items = document.querySelectorAll('*');
  for (const item of items) {
    if (item.innerText?.includes('农业银行') && item.innerText?.includes('601288')) {
      item.click();
      return;
    }
  }
});
await delay(1500);

// 4. 输入价格和数量
await page.evaluate(() => {
  const priceInput = document.querySelector('input[placeholder*="输入价格"]');
  if (priceInput) {
    priceInput.focus();
    priceInput.value = '6.83';
    priceInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
  
  const amountInput = document.querySelector('input[placeholder*="输入数量"]');
  if (amountInput) {
    amountInput.focus();
    amountInput.value = '400';
    amountInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
});
await delay(1000);

// 5. 点击确定按钮
await page.evaluate(() => {
  const btns = document.querySelectorAll('button, [role="button"]');
  for (const btn of btns) {
    if (btn.innerText?.trim() === '确定') {
      btn.click();
      return;
    }
  }
});
await delay(2000);

// 6. 关闭对话框
await page.evaluate(() => {
  const closeBtns = Array.from(document.querySelectorAll('*'))
    .filter(el => el.innerText?.trim() === '×');
  if (closeBtns.length > 0) closeBtns[0].click();
});
```

### 关键改进点

1. **延迟增加**: 每步操作后等待1-2秒
2. **精确选择**: 选择叶子节点 (`children.length === 0`)
3. **事件触发**: 完整触发 focus → input → change 事件
4. **错误处理**: 检查每步操作结果