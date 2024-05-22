from playwright.async_api import async_playwright

async def create_rhyme(text: str):
    async with (async_playwright() as pw):
        browser = await pw.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://maximal.github.io/reduplicator/#')
        input_element = await page.query_selector("#inp-text")
        await input_element.fill('')
        await input_element.type(text, delay=0)
        await page.keyboard.press("Enter")
        result_element = await page.query_selector("#hui-result")
        result = await result_element.inner_text()
        await browser.close()
    return result
