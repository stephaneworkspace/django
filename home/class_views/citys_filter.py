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
import removeaccents
import simplejson as json
with open(os.path.join(BASE_DIR, 'assets/citys.json')) as f:
    data = json.load(f)
    data.sort(key=lambda s : s['name'])

with open(os.path.join(BASE_DIR, 'assets/flags.json')) as f:
    country_data = json.load(f)

def name_json(sw_lower_and_no_accent):
    """
    Lower case and without accent for data['name'] in a json array
    """
    a = [] 
    for d in data:
        for k, v in d.items():
            if k == 'name':
                if sw_lower_and_no_accent:
                    a.append(removeaccents.remove_accents(v.lower()))
                else:
                    a.append(v)
    return a

def flag(country_iso_alpha_2):
    """
    Return flag base64 png 20x30 by country isoAlpha2
    """
    for d in country_data:
        for k, v in d.items():
            if k == 'isoAlpha2':
                if v == country_iso_alpha_2:
                    return d['flag']
    return ''

def filter_name(string, substr):
    """
    Filter comparaison between 2 array, return array of result filtered
    """
    return [s for s in string if any(sub in s for sub in substr)]

class citys_filter(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def get_param_fields(self, view):
        """
        Query param for method get()
        """
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
        if request.GET.get('name') == None or request.GET.get('name') == '':
            return HttpResponse('[]')
        else:
            f.append({'name': request.GET.get('name')})
    
        """
        Add form query field to dictionary
        """
        f_dict = { k:v for d in f for k,v in d.items() }
        
        """
        Filter in lowercase
        """
        filter_arr = []
        filter_arr = filter_name(name_json(True), [removeaccents.remove_accents(f_dict['name'].lower())])
        
        """
        Return result
        """
        arr = []
        arr_country = []
        sw = False 
        for d in data:
            sw = False
            for k, v in d.items():
                if k == 'name':
                    if removeaccents.remove_accents(v.lower()) in filter_arr:
                        sw = True
            if sw:
                for cd in country_data:
                    sw_next = True
                    if d['country'] in cd['isoAlpha2']:
                        for ac in arr_country:
                            if d['country'] in ac['country']:
                                sw_next = False
                        if sw_next:        
                            arr_country.append({'country': d['country'], 'flag': flag(d['country'])})
                #d['flag'] = flag(d['country'])
                arr.append(d)
        json_return = { 'filter' : arr, 'country': arr_country }

        return HttpResponse(json.dumps(json_return, encoding="utf-8", ensure_ascii=False, indent=4, sort_keys=False))