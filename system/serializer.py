from rest_framework import fields, serializers
from .models import *
from django.contrib.auth import authenticate
from .UserBackend import UserBackend
class StudentInfo(serializers.ModelSerializer):
    class Meta:
        model = phanquyen
        fields =['__all__']

class ListStudent(serializers.ModelSerializer):
    info = StudentInfo(many =True, read_only = True)
    class Meta:
        model = sinhvien
        fields = ['mssv','info']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = phanquyen
        fields = ('id','username','email','user_type')



class GetClasses(serializers.ModelSerializer):
    class Meta:
        model = lop
        fields = "__all__"
class GetSubject(serializers.ModelSerializer):
    class Meta:
        model = hocphan
        fields = "__all__"

class GetStudent(serializers.ModelSerializer):
    class Meta:
        model = sinhvien
        fields=['mssv','perm_id','id_lop_id']
        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):

        user = UserBackend.authenticate(self,**data)
        if user and user.is_active:
            return user 
        raise serializers.ValidationError("Error")


        