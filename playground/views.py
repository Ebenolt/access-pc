from django.shortcuts import render
from django.http import HttpResponse
from res.utils import *

def sayHello(request):
    return render(request, 'playground_hello.html', {'name': "Anthonin", 'age': 23})

def sayGoodbye(request):
    return HttpResponse("Goodbye !")