import asyncio
from playwright.async_api import async_playwright, Page
import logging

class ChatGPTBrowser:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.is_ready = False
        
    async def start(self):
        """Starts the Playwright browser"""
        self.playwright = await async_playwright().start()
        
        try:
            print("Attempting to connect to existing Chrome on port 9222...")
            self.browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9222")
            
            # Get the default context
            if self.browser.contexts:
                self.context = self.browser.contexts[0]
            else:
                self.context = await self.browser.new_context()

            # Find existing ChatGPT tab or create new one
            pages = self.context.pages
            self.page = None
            for p in pages:
                if "chatgpt.com" in p.url:
                    self.page = p
                    break
            
            if not self.page:
                self.page = await self.context.new_page()
                await self.page.goto("https://chatgpt.com")
            
            print("Successfully connected to Chrome!")
            self.is_ready = True
            
        except Exception as e:
            print(f"Failed to connect to Chrome: {e}")
            print("Make sure you ran 'start_chrome_debug.bat' first!")
            raise e

    async def send_message(self, message: str, file_paths: list = None):
        """Sends a message to ChatGPT and waits for the response"""
        if not self.page:
            return "Error: Browser not started"

        try:
            # Log current page state
            current_url = self.page.url
            page_title = await self.page.title()
            print(f"[DEBUG] Current page: {current_url}")
            print(f"[DEBUG] Page title: {page_title}")
            
            # Check if we're on ChatGPT
            if "chatgpt.com" not in current_url:
                print(f"[WARNING] Not on ChatGPT page! Navigating...")
                await self.page.goto("https://chatgpt.com", timeout=10000)
                await asyncio.sleep(2)
            
            print("[INFO] Waiting for input area...")
            
            # Handle file uploads if any
            if file_paths:
                print(f"Uploading files: {file_paths}")
                try:
                    # ChatGPT usually maintains a hidden file input
                    # We look for input[type='file']
                    file_input = await self.page.wait_for_selector("input[type='file']", state="attached", timeout=5000)
                    await file_input.set_input_files(file_paths)
                    
                    # Wait for uploads to process
                    # Look for deletion buttons or progress indicators to stabilize
                    print("Waiting for uploads to attach...")
                    await asyncio.sleep(5) 
                except Exception as e:
                    print(f"Error uploading files: {e}")
                    return f"Error: Could not upload files. {e}"

            # Try specific ID first, then generic contenteditable
            # ChatGPT often uses #prompt-textarea
            try:
                print("[DEBUG] Looking for #prompt-textarea...")
                textarea = await self.page.wait_for_selector("#prompt-textarea", state="visible", timeout=5000)
                print("[DEBUG] Found #prompt-textarea")
            except Exception as e:
                print(f"[DEBUG] ID selector failed: {e}")
                print("[DEBUG] Trying generic contenteditable...")
                try:
                    textarea = await self.page.wait_for_selector("div[contenteditable='true']", state="visible", timeout=5000)
                    print("[DEBUG] Found contenteditable div")
                except Exception as e2:
                    # Take a screenshot for debugging
                    screenshot_path = "error_screenshot.png"
                    await self.page.screenshot(path=screenshot_path)
                    print(f"[ERROR] Screenshot saved to {screenshot_path}")
                    raise Exception(f"Could not find input textarea. URL: {self.page.url}. Error: {e2}")
            
            if not textarea:
                raise Exception("Could not find input textarea")

            print("[INFO] Found input area, filling message...")
            await textarea.click()
            # Use type instead of fill for better simulation
            # Fallback to .type for older Playwright versions if needed, or stick to .fill if simulation is not key
            await textarea.type(message, delay=10) 
            
            print("[INFO] Clicking send button...")
            # Click send button - try multiple selectors
            send_button = None
            selectors = [
                "form button[type='button']",  # New ChatGPT interface
                "button[data-testid='send-button']",  # Old selector
                "button[data-testid='fruitjuice-send-button']",
            ]
            
            for selector in selectors:
                try:
                    send_button = await self.page.wait_for_selector(selector, state="visible", timeout=2000)
                    if send_button:
                        print(f"[DEBUG] Found send button with selector: {selector}")
                        break
                except:
                    continue
            
            if not send_button:
                screenshot_path = "send_button_error.png"
                await self.page.screenshot(path=screenshot_path)
                raise Exception(f"Could not find send button with any known selector. Screenshot: {screenshot_path}")
            
            # Ensure it's enabled
            is_disabled = await send_button.is_disabled()
            if is_disabled:
                 print("[WARNING] Send button disabled, waiting briefly...")
                 await asyncio.sleep(1)
            
            print("[DEBUG] Clicking send button now...")
            await send_button.click()
            print("[INFO] Message sent!")
            
        except Exception as e:
            # Capture debug info
            title = await self.page.title()
            print(f"Error acting on page. Title: {title}. Error: {e}")
            return f"Error: Could not send message. Page Title: {title}. Error: {e}"

        print("[INFO] Waiting for response...")
        # Wait for generation to complete
        
        # Strategy: 
        # 1. Wait for the 'Stop generating' button to appear (indicating generation started) - Optional but good
        # 2. Wait for the 'Send' button to reappear and be enabled
        
        # Give it a moment to switch state
        await asyncio.sleep(2)

        try:
             # Wait for the send button to be clickable again
             # We use a polling loop because sometimes waiting for attributes is flaky
             print("[INFO] Polling for response completion (max 90 seconds)...")
             for i in range(90): # Try for 90 seconds (increased from 60)
                 await asyncio.sleep(1)
                 
                 # Progress indicator every 10 seconds
                 if (i + 1) % 10 == 0:
                     print(f"[DEBUG] Still waiting... ({i + 1}s elapsed)")
                 
                 # Check if button exists and is not disabled
                 is_ready = await self.page.evaluate("""() => {
                    // Try new selector first
                    let btn = document.querySelector("form button[type='button']");
                    if (!btn) {
                        // Fall back to old selector
                        btn = document.querySelector("button[data-testid='send-button']");
                    }
                    return btn && !btn.disabled;
                 }""")
                 
                 if is_ready:
                     print(f"[INFO] Generation finished after {i + 1} seconds")
                     break
             else:
                 print("[ERROR] Timed out after 90 seconds waiting for response")
                 screenshot_path = "timeout_screenshot.png"
                 await self.page.screenshot(path=screenshot_path)
                 return f"Error: Response timeout after 90 seconds. Screenshot saved to {screenshot_path}"
                 
        except Exception as e:
            print(f"Warning: Error checking button state. {e}")

        # Get the last response
        # Try multiple selectors for robustness
        try:
            print("[INFO] Extracting response text...")
            # Try modern ChatGPT selectors
            response_elements = await self.page.query_selector_all("div[data-message-author-role='assistant']")
            print(f"[DEBUG] Found {len(response_elements)} assistant messages")
            
            if not response_elements:
                print("[DEBUG] Trying .markdown selector...")
                response_elements = await self.page.query_selector_all(".markdown")
                print(f"[DEBUG] Found {len(response_elements)} markdown elements")
            
            if not response_elements:
                print("[DEBUG] Trying article selector...")
                response_elements = await self.page.query_selector_all("article")
                print(f"[DEBUG] Found {len(response_elements)} article elements")
            
            if response_elements:
                last_response = await response_elements[-1].inner_text()
                print(f"[INFO] Successfully extracted response ({len(last_response)} chars)")
                return last_response.strip()
            else:
                screenshot_path = "no_response_screenshot.png"
                await self.page.screenshot(path=screenshot_path)
                return f"Error: No response elements found. Screenshot: {screenshot_path}"
        except Exception as e:
            print(f"[ERROR] Error retrieving response: {e}")
            screenshot_path = "extract_error_screenshot.png"
            await self.page.screenshot(path=screenshot_path)
            return f"Error: Could not retrieve response. {e}. Screenshot: {screenshot_path}"

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
