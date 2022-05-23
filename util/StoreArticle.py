import sqlite3
import os
from datetime import datetime


def hs(s):
    return abs(hash(s)) % (10 ** 8)


def saveArticle(news):
    now = datetime.now()
    date = now.strftime("%Y%m%d")

    path = os.path.join(os.path.dirname(__file__), "../BE/articleTopic/db.sqlite3")
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    query = []

    cur.execute("SELECT hashkey FROM articleHeatMap_article WHERE date == " + date)
    rows = cur.fetchall()

    newsDict = dict()
    for key in rows:
        newsDict[int(key[0])] = True

    for i in range(len(news.titleBox)):
        title = news.titleBox[i]
        curHash = hs(title)
        if curHash not in newsDict:
            url = news.URLBox[i]
            query.append((title, url, int(date), curHash))

    # TODO ADD NEW ARTICLE TO THE DB
    cur.executemany(
        'INSERT INTO articleHeatMap_article(title, URL, date, hashkey) VALUES (?, ?, ?, ?)',
        query
    )
    conn.commit()
    conn.close()

