import numpy as np, json, base64, cv2, face_recognition
from cvzone.FaceDetectionModule import FaceDetector
from cam_tracker.models import FaceEncodings, Member, Attendance
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

def convertEncodingsToDbRow(member_id, encodings):
    row_dict = {
        "member_id": member_id,
    }
    for i in range(1,129):
        row_dict[f'dimen{i}'] = encodings[i-1]
    return row_dict

def getMemberEncodingsFromDb(member_id):
    try:
        encodings_record = FaceEncodings.objects.get(member_id=member_id)
        encodings_dict = encodings_record.__dict__
        face_encodings = np.zeros(shape=(128,), dtype=np.float64)
        for key in encodings_dict:
            if key.startswith('dimen'):
                face_encodings[int(key.removeprefix('dimen')) - 1] = encodings_dict[key]
        return face_encodings
    except Exception as e:
        print(e)
        raise e
    
def getMembersEncodingsWithIdsFromDb(cam_id):
    try:
        members = Member.objects.filter(cam__id=cam_id)
        member_ids = []
        member_face_encodings = []
        for member in list(members):
            member_ids.append(str(member.id))
            member_face_encodings.append(getMemberEncodingsFromDb(member.id))
        return member_ids, member_face_encodings
    except Exception as e:
        print(e)
        raise e
    
def image_analyze(text_data, cam_id, time_sent):
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
                    # attendances = Attendance.objects.filter(member__id=memberIds[matched_index]).order_by('-time')
                    # if len(attendances) == 0 or (datetime.now().astimezone() - attendances[0].time.astimezone()).total_seconds() > 15:
                    #     Attendance.objects.create(member_id=memberIds[matched_index])
                    log = Attendance.objects.create(member_id=memberIds[matched_index], cam_id=cam_id, time=time_sent)
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'logs_{cam_id}', {
                        'type': 'log_receive',
                        'log': {
                            'time': log.time.__str__(),
                            'cam_id': log.cam.id.__str__(),
                            'member': {
                                'id': log.member.id.__str__(),
                                'name': log.member.name,
                                'gender': log.member.gender,
                                'dob': log.member.dob.__str__()
                            }
                        }
                    })
                except Exception as e:
                    raise e

            response_data['data']['faces'].append(face)

        print(response_data)
    except Exception as e:
        print(e)
        return
   