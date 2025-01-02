from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/streaming/<str:cam_id>/', consumers.ImageConsumer.as_asgi()),
    path('ws/logs/<str:cam_id>/', consumers.LogConsumer.as_asgi()),
]