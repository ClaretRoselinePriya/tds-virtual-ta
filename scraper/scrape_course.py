import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import aiosqlite

BASE_URL = "https://tds.s-anand.net/#/2025-01/"

async def scrape_and_store():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL)

        await page.wait_for_selector('nav a')
        links = await page.query_selector_all('nav a')

        for link in links:
            href = await link.get_attribute('href')
            text = await link.text_content()
            full_url = BASE_URL + href
            await page.goto(full_url)
            await page.wait_for_timeout(800)
            content = await page.content()
            cleaned_text = extract_text(content)
            data.append((text, cleaned_text))
            await page.goto(BASE_URL)
            await page.wait_for_timeout(500)

        await browser.close()

    await store_in_sqlite(data)

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text

async def store_in_sqlite(data):
    async with aiosqlite.connect("data/tds_course_content.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS course (topic TEXT, content TEXT)")
        for topic, content in data:
            await db.execute("INSERT INTO course (topic, content) VALUES (?, ?)", (topic, content))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(scrape_and_store())
