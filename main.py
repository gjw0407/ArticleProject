from util.read_excel_file import read_csv
from util.get_articles import *
from timeloop import Timeloop
from datetime import timedelta
from util.StoreArticle import saveArticle
import time

timeloop = Timeloop()

@timeloop.job(interval=timedelta(seconds=600))
def sample_job_every_2s():
    url = [read_csv()]
    news = NewsStand()
    news.checkChanges(url)
    saveArticle(news)

    # Clustering
    #bagofwords(news)


timeloop.start()
while True:
    time.sleep(300)
