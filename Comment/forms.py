#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/7/4 下午2:56

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    comment = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}),error_messages={'required':'我们需要聆听你的声音'})

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'comment_user' in kwargs:
            self.comment_user = kwargs.pop('comment_user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.comment_user.is_authenticated:
            self.cleaned_data['comment_user'] = self.comment_user
        else:
            raise forms.ValidationError('请先登录再发表评论')

        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']

        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_object = model_class.objects.get(id=object_id)
            self.cleaned_data['model_class'] = model_class
            self.cleaned_data['content_object'] = model_object
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']

        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(id=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(id=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')

        return reply_comment_id
