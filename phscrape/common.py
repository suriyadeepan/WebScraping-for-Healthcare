import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def get_page(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 404:
        return 404
    page = BeautifulSoup(response.content, "html.parser")
    return page
