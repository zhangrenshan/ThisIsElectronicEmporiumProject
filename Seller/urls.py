"""DjangoWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from Seller.views import *


urlpatterns = [
    path('born/', born),
    path('base/', base),
    path('rb/', registerBase),
    path('register/', register),
    path('login/', login),
    path('fp/', forgotPassword),
    path('index/', index),
    re_path('^$', login),
    path('pi/', personalInfo),
    path('goodsType/', goodsType),
    path('addGoods/', addGoods),
    path('StoreInformation/', storeInformation),
    re_path('goodsList/(?P<page>\d+)/(?P<status>[012])/', goodsList),
    re_path('goods_status/(?P<status>\d+)/(?P<id>\d+)', goods_status),
]