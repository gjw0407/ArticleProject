from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


class NewsStand:
    def __init__(self):
        self.bodyBox = []
        self.titleBox = []
        self.URLBox = []

    def get_articles(self, args):
        for i in range(len(args)):
            url = args[i]
            print("Extracting Articles from", url)
            webpage = session.get(url)
            soup = BeautifulSoup(webpage.content, "html.parser")

            cnt = 0

            for art in soup.find_all("strong", "tit_g"):
                articleURL = re.search("(?P<url>https?://[^\s]+)", str(art)).group("url")
                articleTitle = art.text
                self.URLBox.append(articleURL)
                self.titleBox.append(articleTitle)
                # TODO
                # ADD Article Media (<span class="txt_info">이데일리</span>)
                # ADD Article Recursively
                cnt += 1

            print("Extracted", cnt, "Articles")
            print()
