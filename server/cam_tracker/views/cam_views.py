import base64, os, pickle, cv2, face_recognition, shutil
from datetime import datetime
import numpy as np
import bcrypt

from cvzone.FaceDetectionModule import FaceDetector

from cam_tracker.models import Attendance, Member, Camera
from cam_tracker.serializers import CameraSerializer
from cam_tracker.lib import auth

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)
FaceDirPath = os.path.realpath(os.path.join('..', 'faces'))

def get_camera_list(request):
    try:
        camera_list = Camera.objects.all()
        serializer = CameraSerializer(camera_list, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    except Exception as e: 
        return Response({
            'error': {
                'message': 'Internal error'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def add_camera(request):
    name = request.data.get('name', None),
    location = request.data.get('location', None),
    auth_token = request.data.get('auth_token', None)

    if name is None or location is None or auth_token is None:
        return Response({
            'error': {
                'message': 'Required fields missing.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:    
        cam = Camera.objects.create(
            name=name,
            location=location,
            auth_token=auth.hashedpassword(auth_token)
        )
        new_camera_dir_path = os.path.join(FaceDirPath, str(cam.id))
        if(os.path.exists(new_camera_dir_path)):
            shutil.rmtree(new_camera_dir_path)
        
        os.makedirs(f'{new_camera_dir_path}/images')
        open(f'{new_camera_dir_path}/encodings.p', 'w+').close()
        return Response({
            'status': 'successful',
            'data': {
                'id': cam.id,
                'name': cam.name,
                'location': cam.location,
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e) 
        return Response({
            'status': 'error',
            'error': {
                'message': 'Internal error'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_camera(request):
    cam_id = request.data.get('cam_id', None)
    auth_token = request.data.get('auth_token', None)
    if cam_id is None or auth_token is None:
        return Response({
            'error': {
                'message': 'Missing cam_id or auth_token'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        camera = Camera.objects.get(id=cam_id)
        if not auth.checkpassword(auth_token, camera.auth_token):
            return Response({
                'error': {
                    'message': 'Unauthorized'
                }
            }, status=status.HTTP_401_UNAUTHORIZED) 
        
        serializer = CameraSerializer(camera)
        camera.delete()
        deleted_camera_dir_path = os.path.join(FaceDirPath, cam_id)
        if os.path.exists(deleted_camera_dir_path):
            shutil(deleted_camera_dir_path)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@csrf_exempt
def post_image(request, cam_id):
    try:
        Camera.objects.get(id=cam_id)
    except Exception as e:
        return Response({
            'status': 'error',
            'error': {
                'message': 'Cam ID not existed.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try: 
        img_b64 = request.data.get('img_b64')
        img_bytes= base64.b64decode(img_b64)
        img_encode = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_encode, flags=1) 
        cv2.imwrite(os.path.join(os.path.dirname(__file__), 'test.png'), img=img) 
    except Exception as e:
        return Response({
            'status': 'error',
            'error': {
                'message': 'Image error'
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try: 
        file = open(os.path.join(FaceDirPath, f'{cam_id}/encodings.p'), 'rb')
        memberFaceEncodingsWithId = pickle.load(file)
        memberFaceEncodings, memberIds = memberFaceEncodingsWithId
        file.close()
    except EOFError: 
        return Response({
            'status': 'ok',
            'data': {
                'faces': []
            },
            'description': 'Encodings file is empty. No member has been added.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({
            'status': 'error',
            'error': {
                'message': 'Error when getting encodings.'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
                pass

        response_data['data']['faces'].append(face)

    return Response(response_data, status=status.HTTP_200_OK)


def add_member(request, cam_id):
    try:
        camera = Camera.objects.get(id=cam_id)
    except Exception as e:
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        })
    
    image_stream = request.data.get('image', None)
    if image_stream is None:
        return Response({
            'error': {
                'message': 'No image provided.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    img = np.asarray(bytearray(image_stream.read()), dtype="uint8")
    img = cv2.imdecode(img, flags=1)
    img, bboxs = detector.findFaces(img, draw=False)
    if len(bboxs) != 1:
        return Response({
            'error': {
                'message': f'Found {len(bboxs)} faces. Only one face must be found in the provided image. Or the image is not clear enough.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        file = open(os.path.join(FaceDirPath, f'{cam_id}/encodings.p'), 'rb')
    except Exception as e:
        return Response({
            'error': {
                'message': 'Encodings file error'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        memberFaceEncodingsWithId = pickle.load(file)
        memberFaceEncodings = memberFaceEncodingsWithId[0]
        x, y, w, h = bboxs[0]['bbox']
        face_frame = [(y, x + w, y + h, x)]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_frame_encoding = face_recognition.face_encodings(img,face_frame)[0]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        matched = face_recognition.compare_faces(memberFaceEncodings, face_frame_encoding)
        for m in matched:
            if m:
                return Response({
                    'error': {
                        'message': 'This person is already in the members list.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        pass
    
    new_member = Member.objects.create(
        cam = camera,
        name=request.data.get('name'),
        gender=request.data.get('gender'),
        dob=request.data.get('dob'),
    )
    cv2.imwrite(os.path.join(FaceDirPath, f'{cam_id}/images/{new_member.id}.png'), img)
    find_encodings(cam_id)
    return Response({
        'id': new_member.id,
        'cam_id': cam_id,
        'name': new_member.name,
        'dob': new_member.dob,
        'gender': new_member.gender,
    }, status=status.HTTP_201_CREATED)

def delete_member(request, cam_id):
    deleted_member = {
        'id': request.data.get('id'),
    }
    try: 
        member = Member.objects.get(id=deleted_member['id'])
    except Exception as e: 
        return Response({
            'error': {
                'message': 'This member is not in the members list'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    image_path = os.path.join(FaceDirPath, f"{cam_id}/images/{member.id}.png")
    if os.path.exists(image_path):
        os.remove(image_path)

    
    deleted_member['cam_id'] = member.cam.id
    deleted_member['name'] = member.name
    deleted_member['dob'] = member.dob
    deleted_member['gender'] = member.gender
    member.delete()
    find_encodings(cam_id)
    return Response(
        deleted_member,
        status=status.HTTP_200_OK
    )

def get_member_list(request, cam_id):
    if cam_id is None:
        return Response({
            'error': {
                'message': 'Missing cam_id'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        camera = Camera.objects.get(id=cam_id)
        return Response(
            CameraSerializer(camera).data,
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)

def find_encodings(cam_id):
    images_dir = os.path.join(FaceDirPath, f"{cam_id}/images")
    images_path_list = os.listdir(images_dir)
    image_list = []
    member_ids = []
    member_face_encodings = []
    for path in images_path_list:
        image_list.append(cv2.imread(os.path.join(images_dir, path)))
        member_ids.append(os.path.splitext(path)[0])

    for img in image_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        member_face_encodings.append(encode)

    member_face_encodings_with_ids = [member_face_encodings, member_ids]

    encodings_filepath = os.path.join(FaceDirPath, f"{cam_id}/encodings.p")
    file = open(encodings_filepath, "wb")
    pickle.dump(member_face_encodings_with_ids, file)
    file.close()

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def camera_views(request):
    if request.method == 'GET':
        return get_camera_list(request)
    
    if request.method == 'POST':
        return add_camera(request)
    
    return delete_member(request) 


@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def camera_member_views(request, cam_id):
    if request.method == 'GET':
        return get_member_list(request, cam_id)
    
    if request.method == 'POST':
        return add_member(request, cam_id)
    
    return delete_member(request, cam_id) 