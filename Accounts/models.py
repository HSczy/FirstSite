import time
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Profile(models.Model):
    class Meta:
        verbose_name = '账户'
        verbose_name_plural = '账户'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=25,
                                 default='新用户' + str(int(round(time.time() * 1000))),  # 用新用户+时间戳的方式得到昵称
                                 verbose_name='昵称', unique=True, blank=True)
    avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/avatar.png',
                                 processors=[ResizeToFill(200, 200)],
                                 format='png',
                                 options={'quality': 95},
                                 verbose_name='头像')


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nick_name


def get_avatar(self):
    profile = Profile.objects.get(user=self)
    return profile.avatar.url


# User 动态绑定方法
User.get_avatar = get_avatar
User.get_nickname = get_nickname
