#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/30 下午9:21

from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ReadNum

register = template.Library()


@register.simple_tag
def read_num_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    return readnum.read_num
