from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.filters import BaseFilterBackend
from rest_framework_swagger import renderers
import coreapi
import coreschema
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json
with open(os.path.join(BASE_DIR, 'assets/citys.json')) as f:
    data = json.load(f)

class citys_filter(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get_param_fields(self, view):
        return [
            coreapi.Field(
                name='name',
                required=False,
                location='query',
                schema=coreschema.String(
                    description='City name or partial name'
                ),
            ),
        ]

    def get(self, request, format=None):
        """
        Get city by filter the name of the city
        """
        f = []
            
        # Required
        # -> No field here
            
        # Optional
        if (request.GET.get('name') == None):
            f.append({'name': ''})
        else:
            f.append({'name': request.GET.get('name')})
    
        """
        Add form query field to dictionary
        """
        f_dict = { k:v for d in f for k,v in d.items() }
        
        # print(data)
        
        # astro = astropyfr.astropyfr(f_dict["year_month_day"], f_dict["hour_min"], utc, lat, lng)
        return HttpResponse('ok + ' + f_dict['name'])