from rest_framework import fields, serializers
from .models import *
from django.contrib.auth import authenticate
from .UserBackend import UserBackend

class StudentID(serializers.ModelSerializer):
    class Meta:
        model = sinhvien
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = phanquyen
        fields = ('id','username','first_name','last_name','email','user_type','st')

class GetSubjectSerializer(serializers.ModelSerializer):    
    subject = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = lop
        fields = ['id','ten_lop','subject']
 

        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):

        user = UserBackend.authenticate(self,**data)
        if user and user.is_active:
            return user 
        raise serializers.ValidationError("Error")

#Base on perm_id = phanquyen.id
class StudentIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self,data):
        user = UserBackend.authenticate_student(self,**data)
        if user  :
            return user
        raise serializers.ValidationError("Loi")
    
class SubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self,data):
        l = UserBackend.authenticate_subject(self,**data)
        if l:
            return l
        raise serializers.ValidationError("Error")
