from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from user.models import User
from user.util import Response
from PIL import Image
import base64
from io import BytesIO


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


from yolov5.detect_qt5 import my_lodelmodel, main_detect
import cv2
import base64
import os


def imagePredict(request):
    if request.method == "POST":
        fileData = request.FILES['image']
        filePath = f"yolov5/data/{fileData}"
        with open(filePath, 'wb+') as f:
            for chunk in fileData.chunks():
                f.write(chunk)
        try:
            im0, label = main_detect(my_lodelmodel(), filePath)
            width = im0.shape[1]
            height = im0.shape[0]
            show = cv2.resize(im0, (width, height))
            # # 设置新的图片分辨率框架
            # width_new = 700
            # height_new = 500
            # # 判断图片的长宽比率
            # if width / height >= width_new / height_new:
            #     show = cv2.resize(im0, (width_new, int(height * width_new / width)))
            # else:
            #     show = cv2.resize(im0, (int(width * height_new / height), height_new))
            im0 = cv2.cvtColor(show, cv2.COLOR_RGB2BGR)
            image = Image.fromarray(im0)
            img_buffer = BytesIO()
            image.save(img_buffer, format='JPEG')
            byte_data = img_buffer.getvalue()
            base64_data = base64.b64encode(byte_data)
            base64_str = base64_data.decode('utf-8')
            return HttpResponse(Response(code=200, data=base64_str, message=label))
        except:
            return HttpResponse(Response(code=200, data=None, message="图片检测错误"))
        finally:
            os.remove(filePath)
    return None
