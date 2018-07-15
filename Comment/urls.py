#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/5 下午2:08

from django.urls import path
from . import views

urlpatterns = [
    path('comment_update', views.comment_update, name='comment_update'),
]
