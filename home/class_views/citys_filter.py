from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.filters import BaseFilterBackend
from rest_framework_swagger import renderers
from ..settings import BASE_DIR
import coreapi
import coreschema
import os
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
        #return JsonResponse([x for x in data if x['name']])
        
        """
        a = []
        sw = False
        for d in data:
            sw = False
            for k, v in d.items():
                if (k == 'name'):
                    sw = filter(filter_name, v)
            if (sw):
                a.append(d)
        return HttpResponse(a)
        
        
        """
        filter_arr = []
        filter_arr = filter_name(name_json(True), [f_dict['name'].lower()])
        print(filter_arr)
        
        arr = []
        sw = False 
        for d in data:
            sw = False
            for k, v in d.items():
                if k == 'name':
                    if v.lower() in filter_arr:
                        sw = True
            if sw:
                arr.append(d)
        return HttpResponse(arr)

        # astro = astropyfr.astropyfr(f_dict["year_month_day"], f_dict["hour_min"], utc, lat, lng)
        return HttpResponse('ok + ' + f_dict['name'])

def name_json(sw_lower):
    a = [] 
    for d in data:
        for k, v in d.items():
            if k == 'name':
                if sw_lower:
                    a.append(v.lower())
                else:
                    a.append(v)
    return a

string_total = ['tes', 'test', 't', 'test1234', '1234test']
def filter_name(string, substr):
    
    # return [s for s in string if any(sub in s for sub in substr)]

    return [s for s in string if any(sub in s for sub in substr)]
 
    #return[s for s in string 
    #if re.match(r'[^\d]+|^', s).group(0) in substr]
"""
def filter_name(name):
    a = [] 
    for d in data:
        for k, v in d.items():
            if (k == 'name'):
                a.append(v)
    if (name in a):
        return True
    else:
        return False
"""