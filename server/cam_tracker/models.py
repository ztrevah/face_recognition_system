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
    
    class Meta:
        indexes = [
            models.Index(fields=['username'])
        ]


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
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'cam_id'], name='unique_subscription')
        ] 
        indexes = [
            models.Index(fields=['user_id'])
        ]
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
    
    class Meta:
        indexes = [
            models.Index(fields=['cam_id'])
        ]

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    member = ForeignKey(to=Member, to_field="id", db_column="member_id", on_delete=models.CASCADE)
    cam = ForeignKey(to=Camera, to_field="id", db_column="cam_id", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["cam_id"]),
            models.Index(fields=["time"])
        ]
        ordering = ['-time']

    def __str__(self):
        return f'{self.member_id} - {self.time}'


class FaceEncodings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    member = ForeignKey(to=Member, to_field="id", db_column="member_id", on_delete=models.CASCADE)
    dimen1 = models.FloatField()
    dimen2 = models.FloatField()
    dimen3 = models.FloatField()
    dimen4 = models.FloatField()
    dimen5 = models.FloatField()
    dimen6 = models.FloatField()
    dimen7 = models.FloatField()
    dimen8 = models.FloatField()
    dimen9 = models.FloatField()
    dimen10 = models.FloatField()
    dimen11 = models.FloatField()
    dimen12 = models.FloatField()
    dimen13 = models.FloatField()
    dimen14 = models.FloatField()
    dimen15 = models.FloatField()
    dimen16 = models.FloatField()
    dimen17 = models.FloatField()
    dimen18 = models.FloatField()
    dimen19 = models.FloatField()
    dimen20 = models.FloatField()
    dimen21 = models.FloatField()
    dimen22 = models.FloatField()
    dimen23 = models.FloatField()
    dimen24 = models.FloatField()
    dimen25 = models.FloatField()
    dimen26 = models.FloatField()
    dimen27 = models.FloatField()
    dimen28 = models.FloatField()
    dimen29 = models.FloatField()
    dimen30 = models.FloatField()
    dimen31 = models.FloatField()
    dimen32 = models.FloatField()
    dimen33 = models.FloatField()
    dimen34 = models.FloatField()
    dimen35 = models.FloatField()
    dimen36 = models.FloatField()
    dimen37 = models.FloatField()
    dimen38 = models.FloatField()
    dimen39 = models.FloatField()
    dimen40 = models.FloatField()
    dimen41 = models.FloatField()
    dimen42 = models.FloatField()
    dimen43 = models.FloatField()
    dimen44 = models.FloatField()
    dimen45 = models.FloatField()
    dimen46 = models.FloatField()
    dimen47 = models.FloatField()
    dimen48 = models.FloatField()
    dimen49 = models.FloatField()
    dimen50 = models.FloatField()
    dimen51 = models.FloatField()
    dimen52 = models.FloatField()
    dimen53 = models.FloatField()
    dimen54 = models.FloatField()
    dimen55 = models.FloatField()
    dimen56 = models.FloatField()
    dimen57 = models.FloatField()
    dimen58 = models.FloatField()
    dimen59 = models.FloatField()
    dimen60 = models.FloatField()
    dimen61 = models.FloatField()
    dimen62 = models.FloatField()
    dimen63 = models.FloatField()
    dimen64 = models.FloatField()
    dimen65 = models.FloatField()
    dimen66 = models.FloatField()
    dimen67 = models.FloatField()
    dimen68 = models.FloatField()
    dimen69 = models.FloatField()
    dimen70 = models.FloatField()
    dimen71 = models.FloatField()
    dimen72 = models.FloatField()
    dimen73 = models.FloatField()
    dimen74 = models.FloatField()
    dimen75 = models.FloatField()
    dimen76 = models.FloatField()
    dimen77 = models.FloatField()
    dimen78 = models.FloatField()
    dimen79 = models.FloatField()
    dimen80 = models.FloatField()
    dimen81 = models.FloatField()
    dimen82 = models.FloatField()
    dimen83 = models.FloatField()
    dimen84 = models.FloatField()
    dimen85 = models.FloatField()
    dimen86 = models.FloatField()
    dimen87 = models.FloatField()
    dimen88 = models.FloatField()
    dimen89 = models.FloatField()
    dimen90 = models.FloatField()
    dimen91 = models.FloatField()
    dimen92 = models.FloatField()
    dimen93 = models.FloatField()
    dimen94 = models.FloatField()
    dimen95 = models.FloatField()
    dimen96 = models.FloatField()
    dimen97 = models.FloatField()
    dimen98 = models.FloatField()
    dimen99 = models.FloatField()
    dimen100 = models.FloatField()
    dimen101 = models.FloatField()
    dimen102 = models.FloatField()
    dimen103 = models.FloatField()
    dimen104 = models.FloatField()
    dimen105 = models.FloatField()
    dimen106 = models.FloatField()
    dimen107 = models.FloatField()
    dimen108 = models.FloatField()
    dimen109 = models.FloatField()
    dimen110 = models.FloatField()
    dimen111 = models.FloatField()
    dimen112 = models.FloatField()
    dimen113 = models.FloatField()
    dimen114 = models.FloatField()
    dimen115 = models.FloatField()
    dimen116 = models.FloatField()
    dimen117 = models.FloatField()
    dimen118 = models.FloatField()
    dimen119 = models.FloatField()
    dimen120 = models.FloatField()
    dimen121 = models.FloatField()
    dimen122 = models.FloatField()
    dimen123 = models.FloatField()
    dimen124 = models.FloatField()
    dimen125 = models.FloatField()
    dimen126 = models.FloatField()
    dimen127 = models.FloatField()
    dimen128 = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['member_id']),
        ]