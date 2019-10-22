from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status , generics
from rest_framework.filters import BaseFilterBackend
from rest_framework_swagger import renderers
import coreapi
import coreschema
from astropyfr import astropyfr
from ..exception.field_errors_json import FieldErrorsJson, FIELDERROR
        
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
            f = []
            
            # Required
            f.append({"year_month_day": request.GET.get("year_month_day")})
            f.append({"hour_min": request.GET.get("hour_min")})
            f.append({"utc": request.GET.get("utc")})
            f.append({"geo_pos_ns": request.GET.get("geo_pos_ns")})
            f.append({"geo_pos_we": request.GET.get("geo_pos_we")})
            
            for item in f:
                for k, v in item.items():
                    if (v == None):
                        err.append({k: k + ' not in query'})
            if (len(err) > 0):
                raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
            
            # Optional
            # -> No field here
        except FieldErrorsJson as error:
            return HttpResponseBadRequest(error.json, content_type='application/json')
        f_dict = { k:v for d in f for k,v in d.items() }
        astro = astropyfr.astropyfr(f_dict["year_month_day"], f_dict["hour_min"], f_dict["utc"], float(f_dict["geo_pos_ns"]), float(f_dict["geo_pos_we"]))
        return HttpResponse(astro.get_data())