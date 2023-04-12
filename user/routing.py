from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # 前端请求websocket连接
    path('ws/video/', consumers.CameraConsumer),
]