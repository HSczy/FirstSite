from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = '博客类别'

    category_name = models.CharField(max_length=30, verbose_name='博客分类')
    slug_name = models.SlugField(max_length=40, verbose_name='网页索引名')
    description = models.CharField(max_length=200, null=True, verbose_name='分类描述')

    def __str__(self):
        return self.category_name


class Blog(models.Model):
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'
        ordering = ['-created_time', ]

    title = models.CharField(max_length=50, verbose_name='博客标题')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别')
    slug = models.SlugField(verbose_name='Slug Name')
    cover = ProcessedImageField(upload_to='covers',
                                default='covers/default.jpg',
                                processors=[ResizeToFill(300, 200)],
                                format='JPEG',
                                verbose_name='封面',
                                help_text='请上传300*200的图片')

    def get_cover(self):
        return mark_safe('<img src="{}" width = "50%%">'.format(self.cover.url))

    get_cover.short_description = '封面图'
    auth = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='博客撰写时间')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name='上次编辑时间')
    content = models.TextField(verbose_name='正文内容')

    is_deleted = models.BooleanField(default=False, verbose_name='不予显示')

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


# 时间线
class TimeLine(models.Model):
    class Meta:
        verbose_name = '开发时间线'
        verbose_name_plural = verbose_name

    update_time = models.DateField(verbose_name='上线时间')
    update_content = models.TextField(verbose_name='更新内容')
    short_cut = models.CharField(max_length=50, verbose_name='简介')

    def __str__(self):
        return self.short_cut


# 大荧幕
class Carousel(models.Model):
    class Meta:
        verbose_name = '大荧幕'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    carousel_id = models.IntegerField(verbose_name='编号', help_text='编号越小越靠前')
    blog_url = models.CharField(max_length=100, verbose_name='文章地址')
    carousel_img = ProcessedImageField(upload_to='carousl',
                                       processors=[ResizeToFill(800, 400)],
                                       format='JPEG',
                                       verbose_name='大荧幕封面',
                                       help_text='请上传800*400的图片')
    title = models.CharField(max_length=50, verbose_name='简介')
