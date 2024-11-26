import uuid

from django.db import models
from django.db.models import ForeignKey


class User(models.Model):
    class Type(models.Choices):
        ADMIN = 'Admin'
        GUEST = 'Guest'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, default=Type.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Camera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} - {self.name} - {self.location}'

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    user = ForeignKey(to=User, to_field='id', db_column='user_id', on_delete=models.CASCADE)
    cam = ForeignKey(to=Camera, to_field='id', db_column='cam_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    cam = ForeignKey(to=Camera, to_field='id', db_column='cam_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    image_url = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} - {self.name}'

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    member = ForeignKey(to=Member, to_field="id", db_column="member_id", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.member_id} - {self.time}'

