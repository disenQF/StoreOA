#!/usr/bin/python3
# coding: utf-8
from django.urls import path, re_path
from django.conf.urls import url

from orderapp import views

app_name = 'orderapp'

urlpatterns = [
    path('list_999/<city_code>/<order_num>', views.order_list, name='list'),
    path('cancel/<uuid:order_num>', views.cancle_order, name='cancel'),
    re_path(r'^search/(?P<phone>1[3-57-9][\d]{9})$', views.search, name='search'),
    # url(r'^list2/(?P<city_code>\w+)/(?P<order_num>\d+)$', views.order_list)
    path('query', views.query)
]