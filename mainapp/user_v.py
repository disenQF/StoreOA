#!/usr/bin/python3
# coding: utf-8
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

from mainapp.models import UserEntity

@csrf_exempt
def login(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)

        # 验证用户名和口令是否为空
        if not all((name, password)):
            error_msg = '用户名或口令不能为空'
        else:
            # 验证用户是否存在
            qs = UserEntity.objects.filter(name=name)
            if qs.exists():
                login_user: UserEntity = qs.first()
                if check_password(password, login_user.password):
                    # 登录成功
                    # 将登录用户信息写入到session中
                    request.session['login_user'] = {
                        'name': login_user.name,
                        'user_id': login_user.id,
                        'phone': login_user.phone
                    }

                    return redirect('/user/list')
                else:
                    error_msg = '口令错误!'
            else:
                error_msg = '用户名未注册,<a href=/user/regist>去注册</a>'

    return render(request, 'user/login.html', locals())