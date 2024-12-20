from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cam_tracker.models import User
from cam_tracker.serializers import UserSerializer
from cam_tracker.lib import auth

@api_view(['POST'])  
@csrf_exempt
def signup(req):
    username = req.data.get('username', None)
    password = req.data.get('password', None)
    if username is None or password is None:
        return Response({
            'error': {
                'message': 'Invalid data'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        existing_user = User.objects.get(username=username)
        return Response({
            'error': {
                'message': 'This username has existed'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        try: 
            new_user = User.objects.create(username=username, password=auth.hashedpassword(password))
            return Response(
                UserSerializer(new_user).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e: 
            return Response({
                'error': {
                    'message': 'This username has existed'
                }
            }, status=status.HTTP_400_BAD_REQUEST)     


@api_view(['POST'])    
@csrf_exempt
def signin(req):
    username = req.data.get('username', None)
    password = req.data.get('password', None)
    if username is None or password is None:
        return Response({
            'error': {
                'message': 'Invalid data'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        existing_user = User.objects.get(username=username)
        if not auth.checkpassword(password, existing_user.password):
            return Response({
                'error': {
                    'message': 'Wrong password.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response(
            UserSerializer(existing_user).data,
            status=status.HTTP_200_OK
        )
        response = auth.set_jwt_cookie(existing_user, response)
        return response

    except Exception as e:
        print(e)
        return Response({
            'error': {
                'message': 'This username has not been registered.'
            },
        }, status=status.HTTP_404_NOT_FOUND)  
    

@api_view(['POST'])
@csrf_exempt
def logout(req):
    response = Response({
        'status': 'ok',
        'description': 'Log out successfully'
    }, status=status.HTTP_200_OK)
    response = auth.delete_jwt_cookie(response)
    return response

@api_view(['GET'])
@csrf_exempt
def verify(req):
    user = auth.current_user(req)
    if user is None:
        response = Response({
            'status': 'error',
            'error': {
                'message': 'Unauthorized'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
        response = auth.delete_jwt_cookie(response)
    else:
        response = Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )
        response = auth.set_jwt_cookie(user, response)

    return response
    