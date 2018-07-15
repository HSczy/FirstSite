#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/7 下午3:26

from django import template
from django.contrib.contenttypes.fields import ContentType
from Likes.models import LikeCount, LikeRecord

register = template.Library()


@register.simple_tag
def get_like_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.id)
    return like_count.like_num


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    user = context['user']
    if user.is_authenticated:
        ct = ContentType.objects.get_for_model(obj)
        if LikeRecord.objects.filter(content_type=ct, object_id=obj.id, user=user).exists():
            return 'fas'
        else:
            return 'far'
    else:
        return 'far'


@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model
