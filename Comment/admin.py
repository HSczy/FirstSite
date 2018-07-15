from django.contrib import admin
from .models import Comment


# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'created_time', 'text', 'root', 'parent')

    list_per_page = 50

    list_display_links = ('comment_user', 'created_time', 'text', 'root', 'parent')
