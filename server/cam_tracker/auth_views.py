from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import bcrypt
import json
import jwt
from os import getenv
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


load_dotenv()
SECRET_JWT_KEY = getenv('SECRET_JWT_KEY')

@api_view(['POST'])  
@csrf_exempt
def signup(req):
    serializer = UserSerializer(data=req.data)
    serializer.is_valid()
    username = serializer.data.get('username')
    password = serializer.data.get('password')
    if username == None or password == None:
        return Response({
            'status': 'error',
            'error': {
                'message': 'Invalid data'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        existing_user = User.objects.get(username=username)
        return Response({
            'status': 'error',
            'error': {
                'message': 'This username has existed'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    except:
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        try: 
            User.objects.create(username=username, password=hashed_pw.decode('utf-8'))
            return Response({
                'status': 'ok',
                'description': 'New user has been created'
            }, status=status.HTTP_201_CREATED)
        
        except: 
            return Response({
                'status': 'error',
                'error': {
                    'message': 'This username has existed'
                }
            }, status=status.HTTP_400_BAD_REQUEST)     


@api_view(['POST'])    
@csrf_exempt
def signin(req):
    serializer = UserSerializer(data=req.data)
    serializer.is_valid()
    username = serializer.data.get('username')
    password = serializer.data.get('password')
    if username == None or password == None:
        return Response({
            'status': 'error',
            'error': {
                'message': 'Invalid data'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        existing_user = User.objects.get(username=username)
        if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(existing_user.password, 'utf-8')):
            return Response({
                'status': 'error',
                'error': {
                    'message': 'Wrong password.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)  
        
        serializer = UserSerializer(existing_user)
        response_data = serializer.data
        del response_data['password']
        token = jwt.encode(response_data, SECRET_JWT_KEY)

        response = Response({
            'status': 'ok',
            'description': 'Successfully sign in',
            'data': response_data
        }, status=status.HTTP_200_OK)
        response.set_cookie('access_token', token, httponly=True, secure=True, max_age=86400)
        return response

    except Exception as e:
        return Response({
            'status': 'error',
            'error': {
                'message': 'This username has not been registered.'
            },
        }, status=status.HTTP_404_NOT_FOUND)  


def verify_token(token):
    data = jwt.decode(token, SECRET_JWT_KEY, algorithms='HS256')
    try: 
        User.objects.get(
            id=data.get('id'),
            username=data.get('username'), 
            password=data.get('password'),
            type=data.get('type')
        )
        return True, data.get('type')
    except Exception as e:
        return False, None
