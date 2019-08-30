#!/usr/bin/python3
# coding: utf-8
from django.http import HttpRequest
from django.shortcuts import render


def login(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # 验证用户是否存在

    return render(request, 'user/login.html')