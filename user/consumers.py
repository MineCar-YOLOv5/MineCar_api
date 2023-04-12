import cv2
from yolov5.detect_qt5 import my_lodelmodel, main_detect
from PIL import Image
from io import BytesIO
import base64
import os
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class CameraConsumer(WebsocketConsumer):
    def connect(self):
        self.video = True
        self.camera = cv2.VideoCapture(0)
        self.accept()

    def disconnect(self, close_code):
        self.camera.release()

    def receive(self, text_data=None, bytes_data=None):
        if text_data == 'start':
            filePath = f"yolov5/data/index.jpg"
            ret, frame = self.camera.read()
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
            except:
                self.send(text_data="视频检测失败")
        else:
            self.camera.release()


