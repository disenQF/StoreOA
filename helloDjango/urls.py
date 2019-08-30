"""helloDjango URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include


# 声明views的处理函数
# view处理函数必须要求声明一个request参数，表示客户端的请求对象
# 请求对象中包含哪些信息：
#     - 请求头headers(method, content_type, path,path_info, get_full_path(), COOKIES)
#     - 字典结构请求信息
#        - request.COOKIES   Cookie信息
#        - request.GET  查询参数
#        - request.POST 表单参数
#  请求体： body(字节类型)
def index(request: HttpRequest):

    # return HttpResponse('<h1 style="color:green;">hi, Django</h1>')
    # 将数据渲染到模板中，并将渲染之后html响应给客户端
    return render(request, 'index.html',locals())

urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置子路由，
    # include()导入app模块下urls.py中声明的所有子路由
    path('user/', include('mainapp.urls')),
    path('', index),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
