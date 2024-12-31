from django.urls import path

from cam_tracker.views import subscribe_views, auth_views, cam_views


urlpatterns = [
    path('cameras/', cam_views.camera_views, name='cameraView'),
    path('cameras/<str:cam_id>/members/',cam_views.camera_member_views, name='cameraMembersView'),
    path('auth/signup/',auth_views.signup, name='signup'),
    path('auth/signin/',auth_views.signin, name='signin'),
    path('auth/logout/',auth_views.logout, name='logout'),
    path('auth/verify/',auth_views.verify, name='verify'),
    path('subscriptions/', subscribe_views.subscription_view, name='subscriptionView')
]