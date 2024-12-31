import json, base64, numpy as np, cv2, face_recognition, os
from channels.generic.websocket import WebsocketConsumer
from cam_tracker.models import Camera, Attendance
from cvzone.FaceDetectionModule import FaceDetector
from datetime import datetime
import time
from cam_tracker.lib.cam import getMembersEncodingsWithIdsFromDb
import threading
from cam_tracker.lib.auth import checkpassword


detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)


class ImageConsumer(WebsocketConsumer): 
    cam = None
    cam_id = ''
    def connect(self):
        self.cam_id = self.scope['url_route']['kwargs']['cam_id']
        self.room_group_name = f'receiver_{self.cam_id}'
        try:
            self.cam = Camera.objects.get(id=self.cam_id)
            self.accept()
            self.channel_layer.group
        except Exception as e:
            print(e)
            pass

    def receive(self, text_data=None):
        message_dict = json.loads(text_data)
        message_type = message_dict.get('type', None)
        if message_type == 'image':
            try:
                start = time.time()

                t = threading.Thread(target=image_analyze, args=(text_data, self.cam_id))
                t.start()

                stop = time.time()
                print(stop-start)
                self.send("all good")
                # t.join()
            except Exception as e:
                self.send("not good")
                print(self.cam_id)

        # elif message_type == "init": 
        #     auth_token = message_dict.get('auth_token', None)
        #     if not checkpassword(auth_token, self.cam.auth_token):
        #         self.send("Wrong password")
        #         return
        #     self.room_group_name = f'sender_{self.cam_id}'
            
        # else:
        #     self.send("Invalid")

    
def image_analyze(text_data, cam_id):
    try: 
        img_b64 = json.loads(text_data).get('img_b64', None)
        img_bytes= base64.b64decode(img_b64)
        img_encode = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_encode, flags=1)

        memberIds, memberFaceEncodings = getMembersEncodingsWithIdsFromDb(cam_id)
    
        img, bboxs = detector.findFaces(img, draw=False)
        response_data = {
            'status': 'ok',
            'data': {
                'faces': []
            }
        }
        face_frames = []
        for bbox in bboxs:
            x, y, w, h = bbox['bbox']
            face_frames.append((y, x + w, y + h, x))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_frame_encodings = face_recognition.face_encodings(img, face_frames)

        for face_frame, face_frame_encoding in zip(face_frames,face_frame_encodings):
            y1, x2, y2, x1 = face_frame
            face = {
                'location': [x1,y1,x2,y2],
                'identity': None,
            }
            matched = face_recognition.compare_faces(memberFaceEncodings, face_frame_encoding, tolerance=0.5)
            face_dis = face_recognition.face_distance(memberFaceEncodings, face_frame_encoding)
            matched_index = np.argmin(face_dis)
            if matched[matched_index]:
                face['identity'] = memberIds[matched_index]
                try:
                    attendances = Attendance.objects.filter(member__id=memberIds[matched_index]).order_by('-time')
                    if len(attendances) == 0 or (datetime.now().astimezone() - attendances[0].time.astimezone()).total_seconds() > 15:
                        Attendance.objects.create(member_id=memberIds[matched_index])
                except Exception as e:
                    raise e

            response_data['data']['faces'].append(face)

        print(response_data)
    except Exception as e:
        print(e)
        return