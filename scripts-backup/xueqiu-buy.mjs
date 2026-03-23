import puppeteer from 'puppeteer-core';

// 延迟函数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function buyStock() {
  console.log('🚀 开始执行雪球模拟盘买入操作...\n');
  
  // 连接到Chrome
  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9222',
    defaultViewport: null
  });
  
  console.log('✅ 已连接到Chrome');
  
  // 获取或创建页面
  const pages = await browser.pages();
  let page = pages.find(p => p.url().includes('xueqiu.com')) || pages[0];
  
  if (!page) {
    page = await browser.newPage();
  }
  
  // 导航到组合管理页面
  console.log('📍 导航到 https://xueqiu.com/performance ...');
  await page.goto('https://xueqiu.com/performance', { waitUntil: 'networkidle2' });
  await delay(2000);
  
  // 先截图看看当前页面状态
  await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-page-1.png', fullPage: true });
  console.log('📸 已保存页面截图到 memory/xueqiu-page-1.png');
  
  // 检查页面内容
  const pageUrl = page.url();
  console.log('📍 当前URL:', pageUrl);
  
  // 等待页面加载
  await delay(3000);
  
  // 获取页面文本内容来调试
  const bodyText = await page.evaluate(() => document.body.innerText);
  console.log('📄 页面内容预览:', bodyText.substring(0, 500));
  
  // 检查是否需要登录
  if (bodyText.includes('登录') && bodyText.includes('注册')) {
    console.log('⚠️ 检测到需要登录！请先在浏览器中登录雪球账号。');
    return '需要登录雪球账号';
  }
  
  try {
    // 查找并点击"模拟仓"或类似按钮
    console.log('\n🔍 查找模拟交易入口...');
    
    // 尝试多种方式找到交易按钮
    const tradeSelectors = [
      'a[href*="trade"]',
      'a:has-text("模拟仓")',
      'a:has-text("交易")',
      '[class*="trade"]',
      'a[href="/performance/trade"]'
    ];
    
    let clicked = false;
    
    // 方法1: 使用选择器
    for (const selector of tradeSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          console.log('✅ 找到交易入口:', selector);
          await element.click();
          clicked = true;
          await delay(2000);
          break;
        }
      } catch (e) {
        // 继续尝试下一个
      }
    }
    
    // 方法2: 使用XPath查找文本
    if (!clicked) {
      const tradeButton = await page.evaluateHandle(() => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.find(a => a.textContent.includes('模拟仓') || a.textContent.includes('交易'));
      });
      
      if (tradeButton) {
        console.log('✅ 通过文本找到交易入口');
        await tradeButton.click();
        clicked = true;
        await delay(2000);
      }
    }
    
    // 方法3: 直接导航到交易页面
    if (!clicked) {
      console.log('📍 直接导航到交易页面...');
      await page.goto('https://xueqiu.com/performance/trade', { waitUntil: 'networkidle2' });
      await delay(2000);
    }
    
    // 截图交易页面
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-trade-page.png', fullPage: true });
    console.log('📸 已保存交易页面截图');
    
    // 查找买入按钮
    console.log('\n🔍 查找买入按钮...');
    
    const buyButton = await page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
      return buttons.find(b => b.textContent.includes('买入') || b.textContent.includes('买'));
    });
    
    if (buyButton) {
      console.log('✅ 找到买入按钮，点击...');
      await buyButton.click();
      await delay(2000);
    } else {
      console.log('⚠️ 未找到买入按钮，尝试其他方式...');
    }
    
    // 截图当前状态
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-after-buy-click.png', fullPage: true });
    
    // 输入股票代码
    console.log('\n📝 输入股票代码: 601288');
    
    // 查找输入框
    const codeInput = await page.evaluateHandle(() => {
      const inputs = Array.from(document.querySelectorAll('input'));
      return inputs.find(i => 
        i.placeholder?.includes('代码') || 
        i.placeholder?.includes('输入') ||
        i.placeholder?.includes('股票') ||
        i.name?.includes('code') ||
        i.id?.includes('code')
      );
    });
    
    if (codeInput) {
      await codeInput.click();
      await delay(500);
      await codeInput.type('601288', { delay: 100 });
      await delay(2000);
      console.log('✅ 已输入股票代码');
      
      // 选择农业银行
      console.log('📍 选择农业银行...');
      await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-code-input.png', fullPage: true });
      
      // 点击搜索结果中的农业银行
      const agBank = await page.evaluateHandle(() => {
        const items = Array.from(document.querySelectorAll('[class*="stock"], [class*="item"], li, div'));
        return items.find(item => item.textContent.includes('农业银行') && item.textContent.includes('601288'));
      });
      
      if (agBank) {
        await agBank.click();
        await delay(1000);
        console.log('✅ 已选择农业银行');
      }
    }
    
    // 输入价格
    console.log('\n📝 输入价格: 6.83');
    const priceInput = await page.evaluateHandle(() => {
      const inputs = Array.from(document.querySelectorAll('input'));
      return inputs.find(i => 
        i.placeholder?.includes('价格') || 
        i.name?.includes('price') ||
        i.id?.includes('price')
      );
    });
    
    if (priceInput) {
      await priceInput.click();
      await delay(500);
      // 先清空
      await priceInput.evaluate(el => el.value = '');
      await priceInput.type('6.83', { delay: 100 });
      console.log('✅ 已输入价格');
    }
    
    // 输入数量
    console.log('📝 输入数量: 400');
    const amountInput = await page.evaluateHandle(() => {
      const inputs = Array.from(document.querySelectorAll('input'));
      return inputs.find(i => 
        i.placeholder?.includes('数量') || 
        i.name?.includes('amount') ||
        i.id?.includes('amount') ||
        i.name?.includes('volume')
      );
    });
    
    if (amountInput) {
      await amountInput.click();
      await delay(500);
      await amountInput.evaluate(el => el.value = '');
      await amountInput.type('400', { delay: 100 });
      console.log('✅ 已输入数量');
    }
    
    // 截图输入完成状态
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-before-confirm.png', fullPage: true });
    console.log('📸 已保存输入完成截图');
    
    // 确认买入
    console.log('\n✅ 确认买入...');
    const confirmButton = await page.evaluateHandle(() => {
      const buttons = Array.from(document.querySelectorAll('button, div[role="button"]'));
      return buttons.find(b => 
        b.textContent === '确定' || 
        b.textContent === '确认' || 
        b.textContent === '提交' ||
        b.textContent.includes('买入')
      );
    });
    
    if (confirmButton) {
      await confirmButton.click();
      await delay(3000);
      console.log('✅ 已点击确认按钮');
    }
    
    // 检查结果
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-result.png', fullPage: true });
    console.log('📸 已保存结果截图');
    
    // 检查持仓
    console.log('\n📊 检查持仓状态...');
    await page.goto('https://xueqiu.com/performance', { waitUntil: 'networkidle2' });
    await delay(3000);
    
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-portfolio.png', fullPage: true });
    console.log('📸 已保存持仓页面截图');
    
    const portfolioText = await page.evaluate(() => document.body.innerText);
    const hasPosition = portfolioText.includes('601288') || portfolioText.includes('农业银行');
    
    console.log('\n' + '='.repeat(50));
    console.log('📊 执行结果：');
    console.log('='.repeat(50));
    
    if (hasPosition) {
      console.log('✅ 买入成功！');
      console.log('   股票: 601288 农业银行');
      console.log('   价格: 6.83元');
      console.log('   数量: 400股');
      console.log('   金额: 2732元');
    } else {
      console.log('⚠️ 请查看截图确认持仓状态');
      console.log('   截图保存在 memory/xueqiu-portfolio.png');
    }
    
    return hasPosition ? '买入成功' : '需要人工确认';
    
  } catch (error) {
    console.error('❌ 操作出错:', error.message);
    await page.screenshot({ path: '/home/hongshu/.openclaw/workspace/memory/xueqiu-error.png', fullPage: true });
    console.log('📸 已保存错误截图');
    return '操作失败: ' + error.message;
  }
}

buyStock().catch(console.error);