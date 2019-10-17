from django.http import HttpResponse
from django.shortcuts import render
from astropyfr import astropyfr

def index(request):
    return render(request, 'index.html', {})

def hello(request):
    astro = astropyfr.astropyfr('2000/04/04', '12:24', '+02:00', '46n12', '6e9')
    return HttpResponse(astro.get_data())