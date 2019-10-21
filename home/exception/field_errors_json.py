import simplejson as json

FIELDERROR = "field_error"

class FieldErrorsJson(Exception):
    def __init__(self, message, json_err, code=None, params=None):
        super().__init__(message, code, params)
        self.json = json.dumps(json_err)