import markdown
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class Comment(models.Model):
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE, verbose_name='评论用户')

    root = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='root_comment',
                             verbose_name='根评论')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='parent_comment',
                               verbose_name='父评论')
    reply_to = models.ForeignKey(User, null=True, blank=True, related_name='reply_to', on_delete=models.CASCADE,
                                 verbose_name='回复用户')

    def get_md_text(self):
        md = markdown.markdown(self.text,
                               extensions=[
                                   'markdown.extensions.extra',
                                   'markdown.extensions.codehilite',
                               ])
        return md

    def __str__(self):
        return self.text[:20]
