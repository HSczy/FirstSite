#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/5 下午2:08

from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug_name>', views.blog_category, name='blog_category'),
    path('<slug:slug>', views.blog_detail, name='blog_detail'),
]
