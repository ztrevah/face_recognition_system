import base64, os, pickle, cv2, face_recognition, shutil
from datetime import datetime
import numpy as np

from cvzone.FaceDetectionModule import FaceDetector

from cam_tracker.models import Member, Camera, FaceEncodings
from cam_tracker.serializers import CameraSerializer, MemberSerializer
from cam_tracker.lib import auth

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from cam_tracker.lib.cam import getMembersEncodingsWithIdsFromDb, convertEncodingsToDbRow


detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)
FaceDirPath = os.path.realpath(os.path.join('.', 'cam_tracker/static/cam_tracker/images'))

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
    name = request.data.get('name', None)
    location = request.data.get('location', None)
    auth_token = request.data.get('auth_token', None)

    if name is None or location is None or auth_token is None:
        return Response({
            'error': {
                'message': 'Required fields missing.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        print(name, location, auth_token)
        cam = Camera.objects.create(
            name=name,
            location=location,
            auth_token=auth.hashedpassword(auth_token)
        )

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
        
        camera.delete()
        return Response({
            "id": cam_id,
            "name": camera.name,
            "location": camera.location
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


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
        _, member_face_encodings = getMembersEncodingsWithIdsFromDb(cam_id)
        x, y, w, h = bboxs[0]['bbox']
        face_frame = [(y, x + w, y + h, x)]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_frame_encoding = face_recognition.face_encodings(img,face_frame)[0]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        matched = face_recognition.compare_faces(member_face_encodings, face_frame_encoding, tolerance=0.5)
        for m in matched:
            if m:
                return Response({
                    'error': {
                        'message': 'This person is already in the members list.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({
            'error': {
                'message': 'Internal error'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    new_member = Member.objects.create(
        cam = camera,
        name=request.data.get('name'),
        gender=request.data.get('gender'),
        dob=request.data.get('dob'),
    )
    encodings = FaceEncodings.objects.create(**(convertEncodingsToDbRow(new_member.id, face_frame_encoding)))
    cv2.imwrite(os.path.join(FaceDirPath, f'{new_member.id}.png'), img)
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
        camera_members = Member.objects.filter(cam_id=cam_id)
        return Response(
            MemberSerializer(camera_members, many=True).data,
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print(e)
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def camera_views(request):
    if request.method == 'GET':
        return get_camera_list(request)
    
    if request.method == 'POST':
        return add_camera(request)
    
    return delete_camera(request) 


@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def camera_member_views(request, cam_id):
    if request.method == 'GET':
        return get_member_list(request, cam_id)
    
    if request.method == 'POST':
        return add_member(request, cam_id)
    
    return delete_member(request, cam_id) 