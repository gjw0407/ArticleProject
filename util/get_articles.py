from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import pandas as pd
import pickle
import os
from datetime import datetime

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
        self.media = []
        
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
                self.media.append(url) # [다음, 다음, 다음, 네이버, 네이버]
                # TODO
                # ADD Article Media (<span class="txt_info">이데일리</span>)
                # ADD Article Recursively
                cnt += 1

            print("Extracted", cnt, "Articles")
            print()
        
        # save results as dataframe(pickle)

        data = {'media':self.media,
                'titleBox':self.titleBox,
                'URLBox': self.URLBox
                }
        self.news = pd.DataFrame(data)

        path = os.getcwd() + '\\article\\'
        if not os.path.exists(path):
            os.makedirs(path)
        
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".pkl"

        with open(path+filename, 'wb') as f:
            pickle.dump(self.news, f)

        print('dataframe saved as {}'.format(filename))