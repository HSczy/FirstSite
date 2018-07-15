from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.db.models.aggregates import Count
from django.core.cache import cache
from markdown import Markdown
from markdown.extensions.toc import TocExtension

from .models import Blog, Category
from ReadStatistic.utils import read_statistic
from .utils import notifications_read


# Create your views here.
def blog_category(request, slug_name):
    category = get_object_or_404(Category, slug_name=slug_name)
    blog_list = Blog.objects.filter(category=category, is_deleted=False)

    context = {}
    context['page_of_blogs'] = blog_list
    context['count'] = blog_list.count()
    context['category'] = category
    context['category_list'] = Category.objects.annotate(blog_count=Count('blog'))
    return render(request, 'Blog/blog_category.html', context)


@notifications_read
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    key = read_statistic(request, blog)

    category = Category.objects.get(blog__id=blog.pk)

    # 使用cache对文章进行缓存，如果重新编辑，实行缓存，没有缓存时间为十二小时
    let = blog.last_edit_time.strftime('%Y%m%d%H%M%S')
    cache_key = '{}_cache_{}'.format(blog.id, let)
    cache_blog = cache.get(cache_key)
    if cache_blog:
        blog = cache_blog
    else:
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        blog.content = md.convert(blog.content)
        blog.toc = md.toc
        cache.set(cache_key, blog, 60 * 60 * 12)
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['category'] = category
    context['blog'] = blog
    context['category_list'] = Category.objects.annotate(blog_count=Count('blog'))
    response = render(request, 'Blog/blog_detail.html', context)
    response.set_cookie(key, 'True', 1200)
    return response



