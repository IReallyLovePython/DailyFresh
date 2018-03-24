import re

from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render

from apps.users.models import User

from django.views.generic import View


# Create your views here.
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
            User.objects.create_user(username=username,
                                     password=password,
                                     email=email)
        except IntegrityError:
            return render(request, 'register.html', {'message': '用户名已存在'})

        # todo: 发送激活邮件
        return HttpResponse("注册成功")


# 以下是原版： 显示注册页面 和 处理注册逻辑
# def register(request):
#     return render(request, 'register.html')
#
#
# def do_register(request):
#     # 用户名, 密码, 确认密码, 邮箱, 勾选用户协议
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     password2 = request.POST.get('password2')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#
#     # 'message'用来返回提示信息到注册界面
#     if not all([username, password, password2, email, allow]):
#         return render(request, 'register.html', {'message': '请填写完整'})
#
#     if password != password2:
#         return render(request, 'register.html', {'message': '两次输入的密码不一致'})
#
#     if allow != 'on':
#         return render(request, 'register.html', {'message': '请先同意用户协议'})
#
#     if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#         return render(request, 'register.html', {'message': '邮箱格式不正确'})
#
#     # 业务处理
#     # 保存用户到数据库中
#     # create_user: 是django提供的方法, 会对密码进行加密后再保存到数据库
#     try:
#         User.objects.create_user(username=username,
#                                  password=password,
#                                  email=email)
#     except IntegrityError:
#         return render(request, 'register.html', {'message': '用户名已存在'})
#
#
#     return HttpResponse("注册成功")
