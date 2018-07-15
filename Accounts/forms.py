#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2018/6/27 下午9:07
from django import forms
from django.contrib.auth.models import User


class ChangeNicknameForm(forms.Form):
    new_nickname = forms.CharField(label='新的昵称',
                                   max_length=25,
                                   widget=forms.TextInput(attrs={'placeholder': '请输入新的昵称'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = self.request.user
        if user.email == '':
            raise forms.ValidationError('你还没有注册邮箱，不能更改昵称！')
        return self.cleaned_data

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname', '').strip()
        if new_nickname == '':
            raise forms.ValidationError('邮箱不能为空')
        if User.objects.filter(profile__nick_name=new_nickname).exists():
            raise forms.ValidationError('这个昵称已经存在，想另一个吧')
        return new_nickname


class ChangeAvatarForm(forms.Form):
    new_avatar = forms.ImageField(label='新头像')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = self.request.user
        if user.email == '':
            raise forms.ValidationError('你还没有注册邮箱，不能更改昵称！')
        return self.cleaned_data

    def clean_new_avatar(self):
        new_avatar = self.cleaned_data['new_avatar']
        end_name = new_avatar.name.split('.')[-1]
        if end_name.lower() != 'jpg' and end_name.lower() != 'jpeg' and end_name.lower() != 'png':
            raise forms.ValidationError('我们只支持JPEG，JPG和PNG格式的图片')
        return new_avatar


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'placeholder': '请输入要绑定的邮箱账号'}))

    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(attrs={'placeholder': '请输入发送至邮箱的验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            return forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，重新输入邮箱地址')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code']
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code