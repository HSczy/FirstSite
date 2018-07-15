#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/12 下午5:07

from Notification.models import Notice


def notifications_read(func):
    def wrapper(request, *args, **kwargs):
        notify_key = 'notification'
        if notify_key in request.GET:
            try:
                notify_id = int(request.GET[notify_key])
                notify = Notice.objects.get(id=notify_id)
                notify.is_read = True
                notify.save()
            except ValueError:
                pass
            except Notice.DoesNotExist:
                pass
        return func(request, *args, **kwargs)

    return wrapper
