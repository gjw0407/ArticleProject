from util.read_excel_file import read_csv
from util.get_articles import *
from util.bow import bagofwords


if __name__ == "__main__":
    url = [read_csv()]
    news = NewsStand()
    news.checkChanges(url)
    bagofwords(news)
