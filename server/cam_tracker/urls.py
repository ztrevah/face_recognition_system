from django.urls import path
from . import cam_views
from . import auth_views


urlpatterns = [
    path('cam/', cam_views.add_camera, name='addCamera'),
    path('cam/<str:cam_id>/',cam_views.post_image, name='postImage'),
    path('cam/<str:cam_id>/add/',cam_views.add_new_person, name='addNewPerson'),
    path('cam/<str:cam_id>/delete/',cam_views.delete_member, name='deleteMember'),
    path('auth/signup/',auth_views.signup, name='signup'),
    path('auth/signin/',auth_views.signin, name='signin'),
    path('auth/refresh/',auth_views.refresh, name='refresh'),
]