from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json
from user.models import User
from user.util import Response

def Login(request):
    name = request.GET.get('name')
    password = request.GET.get('password')
    result = User.objects.filter(name=name)
    if len(result) > 0:
        if result[0].password == password:
            return HttpResponse(Response(code=200, data="null", message="登录成功"))
        else:
            return HttpResponse(Response(code=201, data="null", message="密码错误"))

    else:
        return HttpResponse(Response(code=202, data="null", message="查无此人，请先注册！"))
    # return HttpResponse("user" + name)  # 字符串作为返回内容
