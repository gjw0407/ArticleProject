from django.shortcuts import render
from django.http import JsonResponse 
from articleHeatMap.models import Article 

import json

def index(request):
    return render(request, 'main/index.html', {})

def keys(request): 
    articleKeywords = Article.objects.all() 
    articleKeywords_list = [] 
    data = [
              {
                "x":'INTC',"y": 1.2
              },
              {
                "x":'INTC',"y": 0.2
              },{
                "x":'INTC',"y": -1.2
              },         
            ]
    print(data)
    print("inviews")
    
    # for index, todo in enumerate(todos, start=1): 
    #     todo_list.append({'id':index,'title':todo.title,'completed':todo.completed}) 
        
    return JsonResponse(data, safe=False) 
    # return data