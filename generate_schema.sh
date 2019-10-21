#!/bin/sh
python3 manage.py generateschema > api.yml
python3 swagger-yaml-to-html.py < api.yml > api.html