from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

import json
# from res.utils import *

def bad_endpoint(request):
    response = redirect('/api/v1/')
    return response