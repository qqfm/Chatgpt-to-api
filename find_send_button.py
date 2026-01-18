"""
查找 ChatGPT 发送按钮选择器
"""
import asyncio
from playwright.async_api import async_playwright

async def find_send_button():
    print("查找 ChatGPT 发送按钮...")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    
    # 找到 ChatGPT 页面
    chatgpt_page = None
    for page in context.pages:
        if "chatgpt.com" in page.url:
            chatgpt_page = page
            break
    
    if not chatgpt_page:
        print("❌ 找不到 ChatGPT 页面")
        return
    
    print(f"✅ 找到页面: {chatgpt_page.url}\n")
    
    # 尝试多种选择器
    selectors = [
        "button[data-testid='send-button']",
        "button[data-testid='fruitjuice-send-button']",
        "button[aria-label='Send prompt']",
        "button[aria-label='发送提示']",
        "button[type='button'] svg",
        "form button[type='button']",
        "button:has-text('Send')",
        "button:has-text('发送')",
        "[data-testid*='send']",
        "button.absolute.bottom",
        "textarea ~ button",
        "#prompt-textarea ~ div button",
    ]
    
    print("测试以下选择器:\n")
    working_selectors = []
    
    for selector in selectors:
        try:
            element = await chatgpt_page.wait_for_selector(selector, timeout=1000, state="attached")
            is_visible = await element.is_visible()
            
            if is_visible:
                print(f"✅ 有效: {selector}")
                working_selectors.append(selector)
            else:
                print(f"⚠️  存在但不可见: {selector}")
        except:
            print(f"❌ 无效: {selector}")
    
    if working_selectors:
        print(f"\n找到 {len(working_selectors)} 个有效选择器:")
        for s in working_selectors:
            print(f"  - {s}")
        
        # 获取按钮属性
        print("\n检查第一个有效按钮的属性:")
        btn = await chatgpt_page.wait_for_selector(working_selectors[0])
        
        # 获取所有属性
        attrs = await btn.evaluate("""(el) => {
            const attrs = {};
            for (let attr of el.attributes) {
                attrs[attr.name] = attr.value;
            }
            return attrs;
        }""")
        
        print("按钮属性:")
        for key, value in attrs.items():
            print(f"  {key}: {value}")
        
        # 获取 HTML
        html = await btn.evaluate("(el) => el.outerHTML")
        print(f"\n按钮 HTML:\n{html[:500]}...")
    else:
        print("\n❌ 没有找到任何有效的发送按钮选择器")
        print("可能的原因:")
        print("  1. 输入框为空（发送按钮被禁用或隐藏）")
        print("  2. ChatGPT 界面已更新")
        print("  3. 页面未完全加载")
    
    await browser.close()
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(find_send_button())
