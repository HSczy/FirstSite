from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadRecord(models.Model):
    class Meta:
        verbose_name = '访问记录'
        verbose_name_plural = '访问记录'
        ordering = ['-read_time', ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    read_time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间时间')
    ip_address = models.GenericIPAddressField(verbose_name='访问IP地址')
    user = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,verbose_name='阅读用户')
    read_content = content_object


