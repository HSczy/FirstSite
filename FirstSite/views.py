#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/5 下午3:09
from markdown import Markdown
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.db.models.aggregates import Count

from Blog.models import Blog, Category, TimeLine, Carousel


def home(request):
    blog_list = Blog.objects.filter(is_deleted=False)
    carousel_list = Carousel.objects.all()

    # # 分页器
    # paginator = Paginator(blog_list, 10)
    # page_num_now = request.GET.get('page', 1)
    # page_of_blogs = paginator.get_page(page_num_now)
    # current_page = page_of_blogs.number
    #
    # # 显示的页码范围
    # page_range = list(range(max(current_page - 2, 1), current_page)) + \
    #              list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    #
    # # 加上中间缺省页
    # if page_range[0] - 1 > 2:
    #     page_range.insert(0, '...')
    # if paginator.num_pages - page_range[-1] > 2:
    #     page_range.append('...')
    #
    # # 加上首页和尾页
    # if page_range[0] != 1:
    #     page_range.insert(0, 1)
    # if page_range[-1] != paginator.num_pages:
    #     page_range.append(paginator.num_pages)

    context = {}
    # context['page_of_blogs'] = page_of_blogs
    context['page_of_blogs'] = blog_list
    context['carousel_list'] = carousel_list
    context['active_page'] = 'page_home'
    # context['page_range'] = page_range
    context['category_list'] = Category.objects.annotate(blog_count=Count('blog'))
    return render(request, 'home.html', context)


@cache_page(60 * 20)
def timeline(request):
    timelines = TimeLine.objects.all()

    md = Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    for obj in timelines:
        obj.update_content = md.convert(obj.update_content)
        obj.save()
    context = {}
    context['timelines'] = timelines
    return render(request, 'timeline.html', context)


# 文章归档
def archive(request):
    blog_list = Blog.objects.filter(is_deleted=False)
    context = {}
    context['category_list'] = Category.objects.annotate(blog_count=Count('blog'))
    context['blog_list'] = blog_list
    context['active_page'] = 'page_archive'

    return render(request, 'archive.html', context)


# 关于
def about(request):
    context = {}
    context['category_list'] = Category.objects.annotate(blog_count=Count('blog'))
    context['active_page'] = 'page_about'

    return render(request, 'about.html', context)
