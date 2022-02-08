from bs4 import BeautifulSoup


class NewsStand:
    def __init__(self):
        self.bodyBox = []
        self.titleBox = []

    def get_articles(self, args):
        for i in range(len(args)):
            url = args[i]
            #TODO
            #GET ARTICLE TITLE, BODY
            #SORT BY MEDIA


class Article:
    def __init__(self):
        self.body = ""
        self.title = ""

    def __str__(self):
        if len(self.article) == 0:
            print("Article is not Present")
        else:
            print("Tile of the Article: " + self.title)
            print("----------Body----------")
            print(self.body)
            print("------------------------")

