from util.read_excel_file import read_csv
from util.get_articles import *
from util.bow import bagofwords
import time
from timeloop import Timeloop
from datetime import timedelta

timeloop = Timeloop()


@timeloop.job(interval=timedelta(seconds=10))
def sample_job_every_2s():
    url = [read_csv()]
    news = NewsStand()
    news.checkChanges(url)
    bagofwords(news)


timeloop.start()
while True:
    print("Other Logic")
    time.sleep(15)
