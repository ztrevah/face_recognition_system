import json, base64, numpy as np, cv2, face_recognition, os, time, threading
from datetime import datetime

from cvzone.FaceDetectionModule import FaceDetector

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from cam_tracker.lib.auth import checkpassword
from cam_tracker.lib.cam import image_analyze 
from cam_tracker.models import Camera, Attendance
from cam_tracker.serializers import AttendanceSerializer, MemberSerializer


detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

class ImageConsumer(WebsocketConsumer): 
    cam = None
    cam_id = ''
    is_sender = False
    def connect(self):
        self.cam_id = self.scope['url_route']['kwargs']['cam_id']
        self.room_group_name = f'streaming_{self.cam_id}'
        try:
            self.cam = Camera.objects.get(id=self.cam_id)
            self.accept()
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        except Exception as e:
            print(e)
            pass

    def receive(self, text_data=None):
        time_sent = datetime.now().astimezone()
        try:
            message_dict = json.loads(text_data)
            message_type = message_dict.get('type', None)
            auth_token = message_dict.get('auth_token')
            if message_type == 'image_send':
                if self.is_sender == False:
                    if not checkpassword(auth_token, self.cam.auth_token):
                        self.send('Unauthorized')
                        return
                    self.is_sender = True

                start = time.time()
                t = threading.Thread(target=image_analyze, args=(text_data, self.cam_id, time_sent))
                async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
                    'type': 'image_send',
                    'img_b64': message_dict.get('img_b64', None)
                })
                t.start()
                stop = time.time()
                print(stop-start)

            self.send('Invalid type')
        except Exception as e:
            print(e)
    
    def disconnect(self, code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        except Exception as e:
            print(e)

    def image_send(self, event):
        if self.is_sender:
            return
        try:
            self.send(event['img_b64'])
        except Exception as e:
            print(e)
 

class LogConsumer(WebsocketConsumer):
    cam = None
    cam_id = ''
    def connect(self):
        self.cam_id = self.scope['url_route']['kwargs']['cam_id']
        self.room_group_name = f'logs_{self.cam_id}'
        try:
            self.cam = Camera.objects.get(id=self.cam_id)
            self.accept()
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        except Exception as e:
            print(e)
            pass

    def disconnect(self, code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        except Exception as e:
            print(e)

    def log_receive(self,event):
        try:
            log = event.get('log', None)
            if log is not None:
                self.send(json.dumps(log))
        except Exception as e:
            print(e)