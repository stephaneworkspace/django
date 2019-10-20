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

schema_view = get_swagger_view(title='Astrologie API by Stéphane Bressani')

urlpatterns = [
    url(r'^$', schema_view)
]
"""
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Astrologie API by Stéphane Bressani')
    return response.Response(generator.get_schema(request=request))
"""
def index(request):
    return render(request, 'index.html', {})

@api_view()
def hello(request):
    astro = astropyfr.astropyfr('1986/04/03', '04:54', '+02:00', '46n12', '6e9')
    return HttpResponse(astro.get_data())

@api_view()
def theme_natal(request):
    try:
        data = json.loads(request.raw_post_data)
        year_month_day = data['year_month_day']
        hour_min = data['hour_min']
        utc = data['utc']
        geo_pos_ns = data['geo_pos_ns']
        geo_pos_we = data['geo_pos_we']
        print(year_month_day, hour_min, utc, geo_pos_ns, geo_pos_we)
    except:
        print('errors')
    param = request.GET.get('param','All')
    # QueryDict.fromkeys(['a', 'a', 'b'], value='val')
    astro = astropyfr.astropyfr('1986/04/03', '04:54', '+02:00', '46n12', '6e9')
    return HttpResponse(astro.get_data())