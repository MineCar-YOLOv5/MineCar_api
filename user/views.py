from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from user.models import User
from user.util import Response


def Login(request):
    name = request.GET.get('username')
    password = request.GET.get('password')
    result = User.objects.filter(name=name)
    if len(result) == 1:
        if result[0].password == password:
            return HttpResponse(Response(code=200, data="null", message="登录成功"))
        else:
            return HttpResponse(Response(code=201, data="null", message="密码错误"))
    else:
        return HttpResponse(Response(code=202, data="null", message="查无此人，请先注册！"))

def Regist(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        print(name, password)
        # result = User.objects.create(name=name, password=password)
