"""Veo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from App.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # ------------------------------------- APP -------------------------------
    url(r'^login/$', log_in),
    url(r'^logout/$', log_out),
    url(r'^signin/$', sign_in),

    # HomePage
    url(r'^$', home),

    # Movies
    url(r'^movies/$', movies),

    # Shows
    url(r'^shows/$', shows),

    # Social
    url(r'^social/$', social),

    # Change Theme
    url(r'^changeTheme/(?P<theme>\d+)/$', changeTheme),

    # Movie
    url(r'^movie/(?P<id>\d+)/$', movie),

    # Shwow
    url(r'^show/(?P<id>\d+)/$', show),

]
