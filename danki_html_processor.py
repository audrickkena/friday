import requests
from bs4 import BeautifulSoup

# function for getting the title of a video directly from the webpage because pytube is not doing it
async def getYoutubeTitle(link: str) -> str:
    try:
        page = requests.get(link)

        # if the request was succesful
        if page.status_code >= 200 and page.status_code < 300:
            
            # get a beautiful soup obj from the page using python's build in html parser
            soup = BeautifulSoup(page.text, 'html.parser')

            # title of video is in a meta tag, specifically <meta name="title"> so to get the title, 
            # need to access this tag's content then return the result
            title = soup.find(name="meta", attrs={"property": "og:title"}).get("content")
            return title

    except Exception as err:
        raise err
