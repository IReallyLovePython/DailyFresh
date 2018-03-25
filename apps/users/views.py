import re

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from DailyFresh import settings
from apps.users.models import User

from django.views.generic import View

# Create your views here.
from utils.common import send_active_email


class LoginView(View):
    def get(self, request):
        """进入登录界面"""
        return render(request, 'login.html')

    def post(self, request):
        """处理登录逻辑"""

        # 获取登录参数
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验参数合法性
        if not all([username, password]):
            return render(request, 'login.html', {'message': '请求参数不完整'})

        # 通过 django 提供的authenticate方法，
        # 验证用户名和密码是否正确
        user = authenticate(username=username, password=password)

        # 用户名或密码不正确
        if user is None:
            return render(request, 'login.html', {'message': '用户名或密码不正确'})

        if not user.is_active:  # 注册账号未激活
            # 用户未激活
            return render(request, 'login.html', {'message': '请先激活账号'})

        # 通过django的login方法，保存登录用户状态（使用session）
        login(request, user)

        # 获取是否勾选'记住用户名'
        remember = request.POST.get('remember')

        # 判断是否是否勾选'记住用户名'
        if remember != 'on':
            # 没有勾选，不需要记住cookie信息，浏览会话结束后过期
            request.session.set_expiry(0)
        else:
            # 已勾选，需要记住cookie信息，两周后过期
            request.session.set_expiry(3600)

        # 响应请求，返回html界面 (进入首页)
        return redirect(reverse('goods:index'))


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 'message'用来返回提示信息到注册界面
        if not all([username, password, password2, email, allow]):
            return render(request, 'register.html', {'message': '请填写完整'})

        if password != password2:
            return render(request, 'register.html', {'message': '两次输入的密码不一致'})

        if allow != 'on':
            return render(request, 'register.html', {'message': '请先同意用户协议'})

        if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'message': '邮箱格式不正确'})

        # 业务处理
        # 保存用户到数据库中
        # create_user: 是django提供的方法, 会对密码进行加密后再保存到数据库
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)

            # 将用户激活状态设置为未激活
            User.objects.filter(id=user.id).update(is_active=False)

        except IntegrityError:
            return render(request, 'register.html', {'message': '用户名已存在'})

        # 发送激活邮件
        token = user.generate_active_token()
        send_active_email(username, email, token)

        return redirect(reverse("users:login"))


class ActiveView(View):
    # 用户激活逻辑
    def get(self, request, token):
        try:
            # 要激活的用户id
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
            info = s.loads(token)
            user_id = info['confirm']
        except SignatureExpired:
            return HttpResponse('激活链接已过期')

            # 修改用户的激活状态为True (is_active=True)
        User.objects.filter(id=user_id).update(is_active=True)

        # 激活成功进入登录界面
        return HttpResponse('激活成功,进入登录界面')



# 以下是原版：
# 显示注册页面
# def register(request):
#     return render(request, 'register.html')
# 处理注册逻辑
# def do_register(request):
#     pass
# 显示登陆页面
# def login(request):
#     return render(request,'login.html')
