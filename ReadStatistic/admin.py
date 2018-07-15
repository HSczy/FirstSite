from django.contrib import admin
from .models import ReadRecord, ReadNum


# Register your models here.

@admin.register(ReadRecord)
class ReadRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ip_address', 'read_time', 'read_content']
    list_per_page = 100
    list_display_links = ['user', 'ip_address', 'read_time', 'read_content']
