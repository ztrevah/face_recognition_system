from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/',include('cam_tracker.urls')),
    path('admin/', admin.site.urls),
]