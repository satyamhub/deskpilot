"""
browser.py - Browser automation module using Playwright
Provides functions to interact with web pages
"""

import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page


class BrowserManager:
    """Manages browser lifecycle and interactions"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def start(self):
        """Start the browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            print("🌐 Browser started")
        except Exception as e:
            print(f"ERROR: Failed to start browser: {e}")
            raise
    
    async def stop(self):
        """Close the browser"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("🌐 Browser closed")
        except Exception as e:
            print(f"ERROR: Failed to close browser: {e}")
    
    async def open_website(self, url: str):
        """Open a website"""
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            
            print(f"🔗 Opening: {url}")
            await self.page.goto(url, wait_until="load", timeout=8000)
            print(f"✅ Loaded: {url}")
        except Exception as e:
            print(f"ERROR: Failed to open website: {e}")
    
    async def search(self, query: str):
        """
        Search on the current page.
        Looks for search input and enters query.
        """
        try:
            print(f"🔍 Searching for: {query}")
            
            # Try to find search input - common selectors
            search_selectors = [
                'input[placeholder*="Search"]',
                'input[aria-label*="Search"]',
                'input[type="search"]',
                'input[type="text"]',
                'search-box',
                '[role="search"] input',
            ]
            
            for selector in search_selectors:
                try:
                    search_input = self.page.locator(selector).first
                    if await search_input.is_visible(timeout=2000):
                        await search_input.click()
                        await search_input.fill(query)
                        await self.page.keyboard.press("Enter")
                        await self.page.wait_for_load_state("load", timeout=3000)
                        print(f"✅ Search completed")
                        return
                except:
                    continue
            
            print("ERROR: Could not find search input on page")
        except Exception as e:
            print(f"ERROR: Failed to search: {e}")
    
    async def click_element(self, selector: str):
        """Click an element by selector or text content"""
        try:
            print(f"🖱️  Clicking: {selector}")
            
            # First try as a CSS selector
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=1000):
                    await element.click()
                    await asyncio.sleep(1)
                    print(f"✅ Clicked element")
                    return
            except:
                pass
            
            # Try to find by text content (case-insensitive)
            text_selectors = [
                f'button:has-text("{selector}")',
                f'a:has-text("{selector}")',
                f'div:has-text("{selector}")',
                f'[role="button"]:has-text("{selector}")',
                f'text="{selector}"',
            ]
            
            for text_selector in text_selectors:
                try:
                    element = self.page.locator(text_selector).first
                    if await element.is_visible(timeout=1000):
                        await element.click()
                        await asyncio.sleep(1)
                        print(f"✅ Clicked element with text: {selector}")
                        return
                except:
                    continue
            
            # Try with partial text match for buttons/links
            buttons = await self.page.query_selector_all('button, a, [role="button"]')
            for button in buttons:
                try:
                    text = await button.text_content()
                    if text and selector.lower() in text.lower():
                        await button.click()
                        await asyncio.sleep(1)
                        print(f"✅ Clicked element with matching text: {selector}")
                        return
                except:
                    continue
            
            print(f"WARNING: Could not find element to click: {selector}")
        except Exception as e:
            print(f"ERROR: Failed to click element: {e}")
    
    async def type_text(self, selector: str, text: str):
        """Type text into an element - searches by selector or field name"""
        try:
            print(f"⌨️  Typing into {selector}: {text}")
            
            # First try exact CSS selector
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=1000):
                    await element.click()
                    await element.fill(text)
                    print(f"✅ Text entered")
                    return
            except:
                pass
            
            # Try to find by field name/placeholder patterns
            field_selectors = [
                f'input[name*="{selector}"]',
                f'input[placeholder*="{selector}"]',
                f'input[aria-label*="{selector}"]',
                f'input[type="{selector}"]',
                f'input[id*="{selector}"]',
                f'textarea[name*="{selector}"]',
                f'textarea[placeholder*="{selector}"]',
            ]
            
            for field_selector in field_selectors:
                try:
                    element = self.page.locator(field_selector).first
                    if await element.is_visible(timeout=1000):
                        await element.click()
                        await element.fill(text)
                        print(f"✅ Text entered into field: {selector}")
                        return
                except:
                    continue
            
            # Try to find input fields and match by label text
            inputs = await self.page.query_selector_all('input, textarea')
            for input_elem in inputs:
                try:
                    # Check placeholder
                    placeholder = await input_elem.get_attribute('placeholder') or ''
                    if selector.lower() in placeholder.lower():
                        await input_elem.click()
                        await input_elem.fill(text)
                        print(f"✅ Text entered into field: {selector}")
                        return
                    
                    # Check name attribute
                    name = await input_elem.get_attribute('name') or ''
                    if selector.lower() in name.lower():
                        await input_elem.click()
                        await input_elem.fill(text)
                        print(f"✅ Text entered into field: {selector}")
                        return
                    
                    # Check aria-label
                    aria_label = await input_elem.get_attribute('aria-label') or ''
                    if selector.lower() in aria_label.lower():
                        await input_elem.click()
                        await input_elem.fill(text)
                        print(f"✅ Text entered into field: {selector}")
                        return
                    
                    # Check associated label
                    input_id = await input_elem.get_attribute('id') or ''
                    if input_id:
                        label = await self.page.locator(f'label[for="{input_id}"]').inner_text()
                        if label and selector.lower() in label.lower():
                            await input_elem.click()
                            await input_elem.fill(text)
                            print(f"✅ Text entered into field: {selector}")
                            return
                except:
                    continue
            
            print(f"WARNING: Could not find field to type into: {selector}")
        except Exception as e:
            print(f"ERROR: Failed to type text: {e}")
    
    async def wait(self, seconds: float = 2):
        """Wait for specified seconds"""
        try:
            print(f"⏳ Waiting {seconds} seconds...")
            await asyncio.sleep(seconds)
            print(f"✅ Wait complete")
        except Exception as e:
            print(f"ERROR: Wait failed: {e}")
    
    async def get_page_content(self) -> Optional[str]:
        """Get the current page HTML content"""
        try:
            return await self.page.content()
        except Exception as e:
            print(f"ERROR: Failed to get page content: {e}")
            return None


# Global browser manager instance
browser_manager: Optional[BrowserManager] = None


async def get_browser_manager() -> BrowserManager:
    """Get or create the global browser manager"""
    global browser_manager
    if browser_manager is None:
        browser_manager = BrowserManager()
        await browser_manager.start()
    return browser_manager


async def close_browser():
    """Close the global browser"""
    global browser_manager
    if browser_manager:
        await browser_manager.stop()
        browser_manager = None
