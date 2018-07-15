from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Comment.models import Comment


# Create your models here.
class Notice(models.Model):
    class Meta:
        verbose_name = '消息提醒'
        verbose_name_plural = '消息提醒'
        ordering = ['-created_time']

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    post_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送者', related_name='post_user')
    get_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接受者', related_name='get_user')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_read = models.BooleanField(verbose_name='是否已读', default=False)
    notice_object = content_object

    def mark_to_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    def __str__(self):
        return '{}@了{}'.format(self.post_user, self.get_user)


@receiver(post_save, sender=Comment, weak=False)
def notify_handel(sender, instance, created, **kwargs):
    blog = instance.content_object
    comment = instance
    post_user = instance.comment_user
    # 只在创建时发送signal
    if created:
        # 如果是个回复内容，就发送给被回复的人和文章作者，两人为一人，就发送一条
        if comment.reply_to:
            # 如果回复对象和文章作者是一人，发送一条signal
            if blog.auth == comment.reply_to:
                get_user = blog.auth
                if post_user != get_user:
                    Notice.objects.create(post_user=post_user, get_user=get_user,
                                          content_type=ContentType.objects.get_for_model(comment),
                                          object_id=comment.pk)
            # 如果回复对象和文章作者不是一人，发送两条signal
            else:
                if post_user != blog.auth:
                    Notice.objects.create(post_user=post_user, get_user=blog.auth,
                                          content_type=ContentType.objects.get_for_model(comment),
                                          object_id=comment.pk)
                if post_user != comment.reply_to:
                    Notice.objects.create(post_user=post_user, get_user=comment.reply_to,
                                          content_type=ContentType.objects.get_for_model(comment),
                                          object_id=comment.pk)
        # 评论内容 直接发给作者
        else:
            # 如果发送者不是作者，发送一条signal给作者
            if post_user != blog.auth:
                Notice.objects.create(post_user=post_user, get_user=blog.auth,
                                      content_type=ContentType.objects.get_for_model(comment),
                                      object_id=comment.pk)
