#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/2 下午3:41

from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.simple_tag
def get_root_comments(obj):
    ct = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None)
    return comments.order_by('-created_time')


@register.simple_tag
def get_comments_counts(obj):
    ct = ContentType.objects.get_for_model(obj)
    count = Comment.objects.filter(content_type=ct, object_id=obj.id).count()
    return count


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.id,
        'reply_comment_id': 0,
    })
    return comment_form
