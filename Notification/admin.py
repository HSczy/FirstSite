from django.contrib import admin
from .models import Notice


# Register your models here.
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['post_user', 'get_user', 'notice_object', 'created_time']
