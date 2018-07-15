#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/30 下午8:35

import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadRecord


def read_statistic(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '{}_{}_read'.format(ct.model, obj.pk)

    if not request.COOKIES.get(key):
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()

        read_time = datetime.datetime.now()

        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip_address = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip_address = request.META['REMOTE_ADDR']

        user = request.user if request.user.is_authenticated else None

        readrecode, created = ReadRecord.objects.get_or_create(content_type=ct,
                                                               object_id=obj.id,
                                                               read_time=read_time,
                                                               ip_address=ip_address,
                                                               user=user)
        readrecode.read_num += 1
        readrecode.save()

    return key
