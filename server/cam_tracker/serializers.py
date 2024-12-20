from rest_framework import serializers
from .models import User, Camera, Subscription, Member, Attendance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        exclude = ['auth_token']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'