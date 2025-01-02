from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, api_settings

from cam_tracker.models import Subscription, Camera
from cam_tracker.serializers import SubscriptionSerializer
from cam_tracker.lib import auth

from asgiref.sync import sync_to_async


def subscribe_camera(req):
    user = auth.current_user(req)
    if user is None:
        response = Response({
            'error': {
                'message': 'Unauthorized'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
        response = auth.delete_jwt_cookie(response)
        return response
    
    cam_id = req.data.get('cam_id')
    if cam_id is None:
        return Response({
            'error': {
                'message': 'Missing cam_id'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    try:
        camera = Camera.objects.get(id=cam_id)
        try:
            subscription = Subscription.objects.create(user_id=user.id, cam_id=camera.id)
            response = Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_200_OK
            )
            response = auth.set_jwt_cookie(user, response)
            return response
        except Exception as e:
            return Response({
                'error': {
                    'message': 'Failed to subscribe'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


def unsubscribe_camera(req):
    user = auth.current_user(req)
    if user is None:
        response = Response({
            'error': {
                'message': 'Unauthorized'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
        response = auth.delete_jwt_cookie(response)
        return response
    
    cam_id = req.data.get('cam_id')
    if cam_id is None:
        return Response({
            'error': {
                'message': 'Missing cam_id'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        camera = Camera.objects.get(id=cam_id)
        try:
            subscription = Subscription.objects.get(user_id=user.id, cam_id=camera.id)
            deleted_subscription = SubscriptionSerializer(subscription).data
            subscription.delete()
            response = Response(
                deleted_subscription,
                status=status.HTTP_200_OK
            )
            response = auth.set_jwt_cookie(user, response)
            return response
        except Exception as e:
            return Response({
                'error': {
                    'message': 'Subscrption not found'
                }
            }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': {
                'message': 'Camera not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)
    

def get_subscriptions(req):
    user = auth.current_user(req)
    if user is None:
        response = Response({
            'error': {
                'message': 'Unauthorized'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
        response = auth.delete_jwt_cookie(response)
        return response
    
    subscriptions = Subscription.objects.filter(user_id=user.id)
    response_data = []
    for subscription in subscriptions:
        response_data.append({
            'cam_id': subscription.cam_id
        })
    response = Response(
        response_data,
        status=status.HTTP_200_OK
    )
    response = auth.set_jwt_cookie(user, response)
    return response


@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def subscription_view(req):
    if req.method == 'GET':
        return get_subscriptions(req)
    
    if req.method == 'POST':
        return subscribe_camera(req)
    
    return unsubscribe_camera(req)
