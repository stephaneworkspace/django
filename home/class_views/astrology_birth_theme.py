from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.filters import BaseFilterBackend
from rest_framework_swagger import renderers
import coreapi
import coreschema
import simplejson as json
from astropyfr import astropyfr

FIELDERROR = "field_error"

class FieldErrorsJson(Exception):
    def __init__(self, message, json_err, code=None, params=None):
        super().__init__(message, code, params)
        self.json = json.dumps(json_err)
        
class astrology_birth_theme(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get_param_fields(self, view):
        return [
            coreapi.Field(
                name="year_month_day",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Year/Month/Day of birth format as : yyyy/mm/dd"
                ),
            ),
            coreapi.Field(
                name="hour_min",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Hour:Minute of birth format as : hh:mm"
                ),
            ),
            coreapi.Field(
                name="utc",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Utc of birth format as : +hh:mm"
                ),
            ),
            coreapi.Field(
                name="geo_pos_ns",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Geo pos Nord/Sud as HxM : _n_or _s_"
                ),
            ),
            coreapi.Field(
                name="geo_pos_we",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Geo pos Est/West as HxM : _e_or _w_"
                ),
            ),
        ]

    def get(self, request, format=None):
        """
        Get astrology birth theme with astro_py
        """
        try:
            err = []
            field = []
            
            # Required
            field.append({"year_month_day": request.GET.get("year_month_day")})
            field.append({"hour_min": request.GET.get("hour_min")})
            field.append({"utc": request.GET.get("utc")})
            field.append({"geo_pos_ns": request.GET.get("geo_pos_ns")})
            field.append({"geo_pos_we": request.GET.get("geo_pos_we")})
            
            for item in field:
                for k, v in item.items():
                    if (v == None):
                        err.append({k: k + ' not in query'})
            if (len(err) > 0):
                raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
            
            # Optional
            # -> No field here
        except FieldErrorsJson as error:
            return HttpResponseBadRequest(error.json, content_type='application/json')
            #return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        #param = request.GET.get('param','All')
        # QueryDict.fromkeys(['a', 'a', 'b'], value='val')
        astro = astropyfr.astropyfr('1986/04/03', '04:54', '+02:00', '46n12', '6e9')
        return HttpResponse(astro.get_data())
