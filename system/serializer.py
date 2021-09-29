from rest_framework import fields, serializers
from .models import *
class StudentInfo(serializers.ModelSerializer):
    class Meta:
        model = phanquyen
        fields =['__all__']

class ListStudent(serializers.ModelSerializer):
    info = StudentInfo(many =True, read_only = True)
    class Meta:
        model = sinhvien
        fields = ['mssv','info']
