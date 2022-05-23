from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import os
import io

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    with open(os.path.join(os.path.dirname(__file__), "../memo.txt"), encoding='UTF-8') as f:
        LAST_DATA = f.read()
except io.UnsupportedOperation:
    LAST_DATA = "sample_data"
except FileNotFoundError:
    LAST_DATA = "sample_data"
    with open("memo.txt", "w+") as f:
        pass
finally:
    f.close()


def preprocess(tit):
    return re.sub('\s+', ' ', tit).replace("\'", "")


class NewsStand:
    def __init__(self):
        self.bodyBox = []
        self.titleBox = []
        self.URLBox = []
        self.mediaBox = []

    def hasChanged(self, text):
        if LAST_DATA == "":
            print("Initial Update. Executing Crawling Script")
            return 1

        for i in range(len(min(text, LAST_DATA))):
            if text[i] != LAST_DATA[i]:
                print("Update Detected. Executing Crawling Script")
                return 1

        print("No Update has been Found")
        return 0

    def checkChanges(self, args):
        # TODO Last Modified Header로 교체
        for url in args:
            res = requests.get(url)
            if self.hasChanged(res.text):
                self.get_articles(url)
            break

    def get_articles(self, url):
        print("Extracting Articles from", url)
        webpage = session.get(url)
        soup = BeautifulSoup(webpage.content, "html.parser")

        with open(os.path.join(os.path.dirname(__file__), "../memo.txt"), 'w', encoding='UTF-8') as fw:
            fw.write(str(requests.get(url).text))
            fw.close()

        cnt = 0
        for art in soup.find_all("strong", "tit_g"):
            articleURL = re.search("(?P<url>https?://[^\s]+)", str(art)).group("url")
            articleTitle = art.text
            self.URLBox.append(articleURL)
            self.titleBox.append(preprocess(articleTitle))
            # TODO
            # ADD Article Media (<span class="txt_info">이데일리</span>)
            cnt += 1
        print(self.titleBox)
        print("Extracted", cnt, "Articles")
        print()
