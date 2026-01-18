"""
浏览器状态诊断脚本
用于检查 Chrome 浏览器和 ChatGPT 页面状态
"""
import asyncio
from playwright.async_api import async_playwright

async def check_browser():
    print("=" * 60)
    print("浏览器状态诊断工具")
    print("=" * 60)
    
    playwright = None
    browser = None
    
    try:
        print("\n[1/5] 启动 Playwright...")
        playwright = await async_playwright().start()
        print("✅ Playwright 启动成功")
        
        print("\n[2/5] 连接到 Chrome (端口 9222)...")
        try:
            browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ 成功连接到 Chrome")
        except Exception as e:
            print(f"❌ 无法连接到 Chrome: {e}")
            print("\n解决方案: 请先运行 start_chrome_debug.bat")
            return
        
        print("\n[3/5] 获取浏览器上下文...")
        if browser.contexts:
            context = browser.contexts[0]
            print(f"✅ 找到 {len(browser.contexts)} 个浏览器上下文")
        else:
            print("❌ 没有找到浏览器上下文")
            return
        
        print("\n[4/5] 检查打开的页面...")
        pages = context.pages
        print(f"✅ 找到 {len(pages)} 个打开的标签页")
        
        chatgpt_page = None
        for i, page in enumerate(pages):
            url = page.url
            title = await page.title()
            print(f"\n  标签页 {i + 1}:")
            print(f"    URL: {url}")
            print(f"    标题: {title}")
            
            if "chatgpt.com" in url:
                chatgpt_page = page
                print(f"    ✅ 这是 ChatGPT 页面")
        
        if not chatgpt_page:
            print("\n⚠️  警告: 没有找到 ChatGPT 页面")
            print("解决方案: 在 Chrome 中打开 https://chatgpt.com")
            return
        
        print(f"\n[5/5] 检查 ChatGPT 页面状态...")
        
        # 检查输入框
        try:
            input_box = await chatgpt_page.wait_for_selector("#prompt-textarea", state="attached", timeout=3000)
            is_visible = await input_box.is_visible()
            is_enabled = await input_box.is_enabled()
            
            print(f"  输入框状态:")
            print(f"    存在: ✅")
            print(f"    可见: {'✅' if is_visible else '❌'}")
            print(f"    可用: {'✅' if is_enabled else '❌'}")
            
            if not is_visible:
                print("\n  ⚠️  输入框不可见！可能原因:")
                print("     - 有弹窗遮挡")
                print("     - 需要登录")
                print("     - 页面加载不完整")
        except Exception as e:
            print(f"  ❌ 找不到输入框: {e}")
            print("\n  可能原因:")
            print("     - 未登录 ChatGPT")
            print("     - 页面被 Cloudflare 拦截")
            print("     - 有弹窗或提示框")
        
        # 检查发送按钮
        try:
            send_btn = await chatgpt_page.wait_for_selector("button[data-testid='send-button']", state="attached", timeout=3000)
            is_visible = await send_btn.is_visible()
            is_disabled = await send_btn.is_disabled()
            
            print(f"\n  发送按钮状态:")
            print(f"    存在: ✅")
            print(f"    可见: {'✅' if is_visible else '❌'}")
            print(f"    可用: {'✅' if not is_disabled else '❌'}")
        except Exception as e:
            print(f"\n  ❌ 找不到发送按钮: {e}")
        
        # 保存截图
        screenshot_path = "browser_status_screenshot.png"
        await chatgpt_page.screenshot(path=screenshot_path, full_page=False)
        print(f"\n📸 页面截图已保存: {screenshot_path}")
        
        print("\n" + "=" * 60)
        print("诊断完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

if __name__ == "__main__":
    asyncio.run(check_browser())
