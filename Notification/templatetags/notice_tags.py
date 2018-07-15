#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/12 上午9:26

from django import template

register = template.Library()

@register.simple_tag
def get_notice_list_count(user, read_status=None):
    if read_status == 'True':
        notice_list = user.get_user.filter(is_read=True)
    elif read_status == 'False':
        notice_list = user.get_user.filter(is_read=False)
    else:
        notice_list = user.get_user.all()
    return notice_list.count()
