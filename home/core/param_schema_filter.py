from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import BaseFilterBackend

"""
Schema for documentation in Swagger
"""

class param_schema_filter(BaseFilterBackend):
    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        fields = super().get_schema_fields(view)
        if hasattr(view, 'get_param_fields'):
            print(view)
            fields += view.get_param_fields(view)
        return fields