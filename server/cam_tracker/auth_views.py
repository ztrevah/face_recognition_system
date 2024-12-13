from datetime import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from .models import User
import bcrypt
import jwt
from os import getenv
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


load_dotenv()
SECRET_JWT_ACCESS_KEY = getenv('SECRET_JWT_ACCESS_KEY')
SECRET_JWT_REFRESH_KEY = getenv('SECRET_JWT_REFRESH_KEY')

ACCESS_TOKEN_MAX_AGE = 600 # 10 minutes
REFRESH_TOKEN_MAX_AGE = 604800 # 1 weeks


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
        
        access_token = sign_access_token(existing_user)
        refresh_token = sign_refresh_token(existing_user)
        response_data = UserSerializer(existing_user).data
        del response_data['password']

        response = Response({
            'status': 'ok',
            'description': 'Successfully sign in',
            'data': response_data
        }, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='strict', max_age=ACCESS_TOKEN_MAX_AGE)
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='strict', max_age=REFRESH_TOKEN_MAX_AGE)
        return response

    except Exception as e:
        print(e)
        return Response({
            'status': 'error',
            'error': {
                'message': 'This username has not been registered.'
            },
        }, status=status.HTTP_404_NOT_FOUND)  
    
@api_view(['POST'])
@csrf_exempt
def refresh(req):
    response = Response()

    access_token = req.COOKIES.get('access_token', None)
    at_verified, user = verify_access_token(access_token)
    if not at_verified:
        refresh_token = req.COOKIES.get('refresh_token', None)
        rt_verified, user = verify_refresh_token(refresh_token)
        if not rt_verified:
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            response.data = {
                'status': 'unsuccessful'
            }
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        access_token = sign_access_token(user=user)
        
    response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='strict', max_age=ACCESS_TOKEN_MAX_AGE)
    response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='strict', max_age=REFRESH_TOKEN_MAX_AGE)
    response.data = {
        'status': 'ok'
    }
    response.status_code = status.HTTP_200_OK
    return response

def sign_access_token(user, expired_time=ACCESS_TOKEN_MAX_AGE):
    try: 
        serializer = UserSerializer(user)
        response_data = serializer.data
        del response_data['password']
        response_data['exp'] = round(datetime.timestamp(datetime.now() + timedelta(seconds=expired_time)))
        access_token = jwt.encode(payload=response_data, key=SECRET_JWT_ACCESS_KEY, algorithm='HS256')
        return access_token
    except Exception as e: 
        raise e
    
def sign_refresh_token(user, expired_time=REFRESH_TOKEN_MAX_AGE):
    try: 
        serializer = UserSerializer(user)
        response_data = serializer.data
        del response_data['password']
        response_data['exp'] = round(datetime.timestamp(datetime.now() + timedelta(seconds=expired_time)))
        access_token = jwt.encode(payload=response_data, key=SECRET_JWT_REFRESH_KEY, algorithm='HS256')
        return access_token
    except Exception as e: 
        raise e

def verify_access_token(token):
    try: 
        data = jwt.decode(token, SECRET_JWT_ACCESS_KEY, algorithms='HS256', options={
            'verify_signature': True,
            'verify_exp': True
        })
        user = User.objects.get(id=data.get('id'))
        return True, user
    except Exception as e:
        return False, None
    
def verify_refresh_token(token):
    try: 
        data = jwt.decode(token, SECRET_JWT_REFRESH_KEY, algorithms='HS256', options={
            'verify_signature': True,
            'verify_exp': True
        })
        user = User.objects.get(id=data.get('id'))
        return True, user
    except Exception as e:
        return False, None
    

