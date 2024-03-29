"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from .class_views.swagger_schema_view import swagger_schema_view
from .class_views.astrology_birth_theme import astrology_birth_theme
from .class_views.citys_filter import citys_filter

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^api/astrology_birth_theme', astrology_birth_theme.as_view(), name='astrology_birth_theme'),
    url(r'^api/citys_filter', citys_filter.as_view(), name='citys'),
    url(r'^api/swagger', swagger_schema_view.as_view(), name='swagger'),
    path('test/', views.test, name='test'),
]