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

from yolov5.detect_qt5 import my_lodelmodel,main_detect
import cv2
import base64
def imagePredict(request):
    if request.method == "GET":
        fileData = request.GET.get("image")
        print(33333, fileData)
        # with open("yolov5/data/images/index.jpg", 'wb+') as f:
        #     # 分块写入文件
        #     for chunk in fileData.chunks():
        #         f.write(chunk)
        # bytes = read_into_buffer("yolov5/data/images/index.jpg")
        # print(1111, type(bytes))
        # im0,label = main_detect(my_lodelmodel(), "yolov5/data/images/index.jpg")
        im0, label = main_detect(my_lodelmodel(), fileData)
        print(im0, label)

        width = im0.shape[1]
        height = im0.shape[0]

        # 设置新的图片分辨率框架
        width_new = 700
        height_new = 500

        # 判断图片的长宽比率
        if width / height >= width_new / height_new:

            show = cv2.resize(im0, (width_new, int(height * width_new / width)))
        else:

            show = cv2.resize(im0, (int(width * height_new / height), height_new))
        im0 = cv2.cvtColor(show, cv2.COLOR_RGB2BGR)
        from PIL import Image
        im = Image.fromarray(im0)
        im.save("index.jpg")
        with open("index.jpg", 'rb') as f:
            img_data = f.read()
        base64_data = base64.b64encode(img_data)
        base64_str = base64_data.decode('utf-8')
        return HttpResponse(Response(code=200, data=base64_str, message=label))

    return None
import os
def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    f.close()
    return buf