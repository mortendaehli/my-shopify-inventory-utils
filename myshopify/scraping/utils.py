from io import BytesIO
from typing import List
from retry import retry
import requests
from bs4 import BeautifulSoup, Comment
from PIL import Image


def get_clean_text_from_soup(soup: BeautifulSoup) -> str:
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text  # text.encode('utf-8')


def get_clean_text_from_soup2(soup: BeautifulSoup) -> List[str]:
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    return comments.find_all_next(text=True)


def get_clean_text_from_soup3(soup: BeautifulSoup) -> List[str]:
    return soup.get_Text(" ", strip=True)


def process_image(image: Image) -> Image:
    return image.resize((i * 2 for i in image.size))


def get_page_html_from_url(url: str) -> str:
    r = requests.get(url)
    r.raise_for_status()
    return r.text


@retry(requests.exceptions.SSLError, delay=3, tries=5)
def get_image_from_url(url: str) -> Image:
    r = requests.get(url)
    r.raise_for_status()
    return Image.open(BytesIO(r.content))


def clean_html_text(string: str) -> str:
    return "\n".join([x for x in string.splitlines() if x.strip()])
