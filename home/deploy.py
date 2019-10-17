""" 
https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/
"""
import os

import dj_database_url

from . import *  # noqa: F403
from home.settings import BASE_DIR

# This is NOT a complete production settings file. For more, see:
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = ['localhost']

# DATABASES['default'] = dj_database_url.config(conn_max_age=600)  # noqa: F405

STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # noqa: F405

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
