#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/13 下午7:14
from django.core.paginator import Paginator

def paginator(request, obj, count=10):
    # 分页器
    paginator = Paginator(obj, count)
    page_num_now = request.GET.get('page', 1)
    page_of_obj = paginator.get_page(page_num_now)
    current_page = page_of_obj.number

    # 显示的页码范围
    page_range = list(range(max(current_page - 2, 1), current_page)) + \
                 list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))

    # 加上中间缺省页
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] > 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    return page_of_obj, page_range