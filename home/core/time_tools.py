from timezonefinder import TimezoneFinder
import pytz
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError, InvalidTimeError, AmbiguousTimeError, NonExistentTimeError
from datetime import datetime
from ..exception.field_errors_json import FieldErrorsJson, FIELDERROR

def offset(target):
    """
    Return a location's time zone offset from UTC in minutes.
    ---
    Solution from:
        - communikekein https://github.com/communikein
        - phineas-pta https://github.com/phineas-pta
    """
    lat = target['lat']
    lng = target['lng']
    dt = target['dt']
    try:
        tf = TimezoneFinder(in_memory=True)
        tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))

        offset = tz_target.utcoffset(dt)
        #offset -= tz_target.dst(datetime_object) # not used here (summer time)
        seconds = offset.total_seconds()
        hours_str = str(seconds // 3600).replace('.', ':')
        if (offset.days < 0):
            return(hours_str)
        else:
            return('+' + hours_str)
    except UnknownTimeZoneError:
        err = []
        err.append({'lat': 'Unknow time zone'})
        err.append({'lng': 'Unknow time zone'})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
    except InvalidTimeError as error:
        err = []
        err.append({'lat': 'Invalid time error'})
        err.append({'lng': 'Invalid time error'})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
    except AmbiguousTimeError as error:
        err = []
        err.append({'lat': 'Ambigouous time error'})
        err.append({'lng': 'Ambigouous time error'})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
    except NonExistentTimeError as error: 
        err = []
        err.append({'lat': 'Non existent time error'})
        err.append({'lng': 'Non existent time error'})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
    except ValueError as error:
        err = []
        err.append({'lat': str(error)})
        err.append({'lng': str(error)})
        err.append({'year_month_day': str(error)})
        err.append({'hour_min': str(error)})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})
    
def concat(year_month_day, hour_min):
    try:
        dt_str = year_month_day + ' ' + hour_min
        return datetime.strptime(dt_str, '%Y/%m/%d %H:%M')
    except ValueError as error:
        err = []
        err.append({'year_month_day': str(error)})
        err.append({'hour_min': str(error)})
        raise FieldErrorsJson(FIELDERROR, {FIELDERROR: err})