import random
import time
import string
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse

from .forms import ChangeNicknameForm, ChangeAvatarForm, BindEmailForm
from .models import Profile
from Notification.models import Notice
from FirstSite.utils import paginator


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()
    return render(request, 'Accounts/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = AuthenticationForm
    return render(request, 'Accounts/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    notice_list = Notice.objects.filter(get_user=user)
    page_notice_list, page_range = paginator(request, notice_list, 50)
    data = {}
    data['page_notice_list'] = page_notice_list
    data['page_range'] = page_range
    return render(request, 'Accounts/profile.html', data)


@login_required
# 学艺不精，加之时间有限，只能用这种最次的方法
def mark_all_to_read(request):
    user = request.user
    no_read_list = Notice.objects.filter(get_user=user, is_read=False)
    for item in no_read_list:
        item.mark_to_read()
    return redirect('profile')


@login_required
def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, request=request)
        if form.is_valid():
            new_nickname = form.cleaned_data['new_nickname']
            profile = Profile.objects.get(user=request.user)
            profile.nick_name = new_nickname
            profile.save()
            return redirect('profile')
    else:
        form = ChangeNicknameForm()
    data = {}
    data['form'] = form
    data['title'] = '更改昵称'
    return render(request, 'Accounts/change_profile.html', data)


@login_required
def change_avatar(request):
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            new_avatar = form.cleaned_data['new_avatar']
            profile = Profile.objects.get(user=request.user)
            profile.avatar = new_avatar
            profile.save()
            return redirect('profile')
    else:
        form = ChangeAvatarForm()
    data = {}
    data['form'] = form
    data['title'] = '更改头像'
    return render(request, 'Accounts/change_profile.html', data)


@login_required
def bind_email(request):
    if request.method == "POST":
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect('profile')

    else:
        form = BindEmailForm()
    data = {}
    data['form'] = form
    data['title'] = '绑定邮箱'
    return render(request, 'Accounts/bind_email.html', data)


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        # 发送验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 6))

        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)

        if now - send_code_time < 120:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['sed_code_time'] = now

            # 发送邮件
            send_mail(
                "Do'N Achieve验证码",
                "您好，感谢注册Do'N Achieve的账号，您本次的验证码为：" + code + "\n如果您没有注册或者绑定" + email
                + "邮箱，请忽略这封邮件，谢谢",
                "461310757@qq.com",
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)
