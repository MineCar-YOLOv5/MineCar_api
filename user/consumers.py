import json
import time

import cv2
from yolov5.detect_qt5 import my_lodelmodel, main_detect
from PIL import Image
from io import BytesIO
import base64
import os
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class SyncConsumer(WebsocketConsumer):
    def connect(self):
        self.username = "xiao"  # 临时固定用户名
        print('WebSocket建立连接：', self.username)
        # 直接从用户指定的通道名称构造通道组名称
        self.channel_group_name = 'msg_%s' % self.username
        # 加入通道层
        # async_to_sync(…)包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用的是异步通道层方法。(所有通道层方法都是异步的。)
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name,
            self.channel_name
        )

        # 接受WebSocket连接。
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name,
            {
                'type': 'get_message',
            }
        )

    def disconnect(self, close_code):
        print('WebSocket关闭连接')
        # 离开通道
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group_name,
            self.channel_name
        )

    # 从WebSocket中接收消息
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # while True:
        #     print('WebSocket接收消息：', text_data, type(text_data))
        #     text_data_json = json.loads(text_data)
        #     message = text_data_json['message']
        #     time.sleep(1)
        #     print(message)
        print(message)
        if message == "close":
            self.disconnect(self.channel_group_name)
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.channel_group_name,
                {
                    'type': 'get_message',
                    'message': message
                }
            )

    def get_message(self, event):
        # print(event.get("message"))
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while (cap.isOpened()):
            retval, frame = cap.read()
            filePath = f"yolov5/data/index.jpg"
            cv2.imwrite(filePath, frame)
            try:
                im0, label = main_detect(my_lodelmodel(), filePath)
                width = im0.shape[1]
                height = im0.shape[0]
                show = cv2.resize(im0, (width, height))
                im0 = cv2.cvtColor(show, cv2.COLOR_RGB2BGR)
                image = Image.fromarray(im0)
                img_buffer = BytesIO()
                image.save(img_buffer, format='JPEG')
                byte_data = img_buffer.getvalue()
                base64_data = base64.b64encode(byte_data)
                base64_str = base64_data.decode('utf-8')
                self.send(text_data=base64_str)
                time.sleep(0.001)
                if event.get('message'):
                    message = event['message']
                    if message == 'close':
                        break
            except:
                self.send(text_data="视频检测失败")
            finally:
                os.remove(filePath)

