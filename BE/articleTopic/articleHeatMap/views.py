# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render

from .models import Article


def index(request):
    return render(request, 'todo/index.html', {})


def articleList(request):
    aritcle = Article.objects.all()
    article_list = []

    for index, arti in enumerate(aritcle, start=1):
        article_list.append({'id': index, 'title': arti.title})

    return JsonResponse(article_list, safe=False)