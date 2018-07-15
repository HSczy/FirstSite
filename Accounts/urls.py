"""FirstSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_view
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('send_verification_code', views.send_verification_code, name='send_verification_code'),
    path('bind_email', views.bind_email, name='bind_email'),
    path('profile', views.profile, name='profile'),
    path('change_nickname', views.change_nickname, name='change_nickname'),
    path('change_avatar', views.change_avatar, name='change_avatar'),
    path('mark_all_to_read',views.mark_all_to_read,name = 'mark_all_to_read'),
    path('logout', auth_view.LogoutView.as_view(), name='logout'),
    path('login', views.login, name='login'),
    path('reset', auth_view.PasswordResetView.as_view(
        template_name='Accounts/password_reset.html',
        email_template_name='Accounts/password_reset_email.html',
        subject_template_name='Accounts/password_reset_subject.txt'),
         name='password_reset'),
    path('reset/done', auth_view.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_done.html'),
         name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
            auth_view.PasswordResetConfirmView.as_view(template_name='Accounts/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/complete',
         auth_view.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('changepassword', auth_view.PasswordChangeView.as_view(template_name='Accounts/password_change.html'),
         name='password_change'),
    path('changepassword/done', auth_view.PasswordChangeDoneView.as_view(
        template_name='Accounts/password_change_done.html'),
         name='password_change_done'),

]
