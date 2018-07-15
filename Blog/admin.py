from django.contrib import admin
from .models import Blog, Category, TimeLine, Carousel


# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'auth', 'created_time', 'is_deleted']
    readonly_fields = ('get_cover',)
    fields = ['title', 'category', 'slug', 'cover', 'get_cover', 'auth', 'content', 'is_deleted']
    exclude = ('get_cover',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


@admin.register(TimeLine)
class TimeLineAdmin(admin.ModelAdmin):
    list_display = ['update_time', 'short_cut']


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    pass
