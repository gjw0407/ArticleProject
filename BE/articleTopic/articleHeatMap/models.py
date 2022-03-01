from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=400)
    URL = models.CharField(max_length=200, default="")
    date = models.IntegerField(default=20220301)
    hashkey = models.IntegerField(default=-1)
