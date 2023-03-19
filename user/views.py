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


from yolov5.detect import main_detect, my_lodelmodel
import cv2

def imagePredict(request):
    if request.method == "POST":
        fileData = request.FILES.get("image")
        print(fileData)
        im0, label = main_detect(my_lodelmodel, fileData)
        # QApplication.processEvents()
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
        print(im0)
        # image_name = QtGui.QImage(im0, im0.shape[1], im0.shape[0], 3 * im0.shape[1], QtGui.QImage.Format_RGB888)
        # label=label.split(' ')[0]    #label 59 0.96   分割字符串  取前一个
        # self.label2.setPixmap(QtGui.QPixmap.fromImage(image_name))
        # jpg = QtGui.QPixmap(image_name).scaled(self.label1.width(), self.label1.height())
        # self.label2.setPixmap(jpg)
