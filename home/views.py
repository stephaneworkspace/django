from django.http import HttpResponse
from django.shortcuts import render
from astropyfr import astropyfr

def index(request):
    return render(request, 'index.html', {})

def hello(request):
    astro = astropyfr.astropyfr('1986/04/03', '04:54', '+02:00', '46n12', '6e9')
    return HttpResponse(astro.get_data())