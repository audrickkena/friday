import aiohttp
from bs4 import BeautifulSoup

async def getYoutubeTitle(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        page = await response.text()
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find(name="meta", attrs={"property": "og:title"}).get("content")
        return title