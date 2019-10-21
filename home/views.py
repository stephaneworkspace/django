from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url
# from django.http import JsonResponse return JsonResponse(data)
import json
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from astropyfr import astropyfr

def index(request):
    return render(request, 'index.html', {})

@api_view()
def test(request):
    astro = astropyfr.astropyfr('1986/04/03', '04:54', '+02:00', '46n12', '6e9')
    return HttpResponse(astro.get_data())