__author__ = 'fatatoopc'
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
import datetime

def current(request):
    now = datetime.datetime.now()
    return render_to_response('index.html', {'now': now})
