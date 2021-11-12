from django.shortcuts import render
from django.http import HttpResponse
from res.utils import *

def hello(request):
    return HttpResponse("API v2")

