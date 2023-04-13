# 建立 python3.7 环境
FROM python:3.9

# 镜像作者
MAINTAINER LuoZhongnan

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置pip源为国内源
COPY pip.conf /root/.pip/pip.conf

# 在容器内创建mysite文件夹
RUN mkdir -p /var/www/html/mysite

# 设置容器内工作目录
WORKDIR /var/www/html/mysite

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD . /var/www/html/mysite

# pip安装依赖
RUN pip install -r requirements.txt

RUN python manage.py makemigrations \
    & python manage.py migrate\
    & python manage.py runserver 0.0.0.0:8000
