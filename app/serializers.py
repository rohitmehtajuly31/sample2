from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        
    def create(self, validated_data):

        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
      

    