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
from ..core.time_tools import offset, concat

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
                name="lat",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Latitude of birth"
                ),
            ),
            coreapi.Field(
                name="lng",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Longitude of birth"
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
            f.append({"lat": request.GET.get("lat")})
            f.append({"lng": request.GET.get("lng")})
            
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
        
        """
        Add form query field to dictionary
        """
        f_dict = { k:v for d in f for k,v in d.items() }
        
        """
        Check if float latitude and longitude is valid
        and then check if date time is valid
        """
        try:
            for d in f:
                for k, v in d.items():
                    if (k == 'lat'):
                        lat = float(v)
                    if (k == 'lng'):
                        lng = float(v)
        except ValueError as error:
            try:
                err = []
                err.append({k: str(error)})
                raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
            except FieldErrorsJson as error:
                return HttpResponseBadRequest(error.json, content_type='application/json')
        
        """
        Check if date time is valid
        """
        try:
            dt = concat(f_dict["year_month_day"], f_dict["hour_min"])
        except FieldErrorsJson as error:
            return HttpResponseBadRequest(error.json, content_type='application/json')
            
        """
        Compute utc
        """
        dict_offset = dict({'lat': lat, 'lng': lng, 'dt': dt})
        try:
            offset(dict_offset)
        except FieldErrorsJson as error:
            return HttpResponseBadRequest(error.json, content_type='application/json')
        """
        try:
            tf = TimezoneFinder(in_memory=True)
            tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
            datetime_str = f_dict["year_month_day"] + ' ' + f_dict["hour_min"]
            datetime_object = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M')
            
            offset = tz_target.utcoffset(datetime_object)
            #offset -= tz_target.dst(datetime_object)
            print(offset)
            
            offset = tz_target.utcoffset(datetime.now())
            #offset -= tz_target.dst(datetime.now())
            print(offset)
        except pytz.exceptions.UnknownTimeZoneError:
            print('test 46')
            pass
        except ValueError as error:
            pass
        """
        """
        astro = astropyfr.astropyfr(f_dict["year_month_day"], f_dict["hour_min"], f_dict["utc"], float(f_dict["geo_pos_ns"]), float(f_dict["geo_pos_we"]))
        return HttpResponse(astro.get_data())
        """
        return HttpResponse('ok')
    
    """
    timezonefinder>=4.1.0

    longitude = 13.358
    latitude = 52.5061
    tf = TimezoneFinder(in_memory=True)
    print(tf.timezone_at(lng=longitude, lat=latitude))
    tz_target = timezone(tf.certain_timezone_at(lng=longitude, lat=latitude))
    print(datetime.now())
    print(tz_target.utcoffset(datetime.now()))
    """