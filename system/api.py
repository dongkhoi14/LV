from system.models import *
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from system.serializer import *

# Dang nhap, lay thong tin ho ten
class loginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class =LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,

        })

# Lay thong tin bao trong model sinhvien
class getStudnetIDAPI(generics.GenericAPIView):
    serializer_class = StudentIDSerializer

    def post(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "mssv":StudentID(user,context=self.get_serializer_context()).data,
        })
    

#Lay thong tin cac hoc phan co trong lop
class getSubjectAPI(generics.GenericAPIView):
    serializer_class = SubjectSerializer
        
   
    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data


        return Response(GetSubjectSerializer(subject,context=self.get_serializer_context()).data)

class getAttAPI(generics.GenericAPIView):

    serializer_class = AttSerializer

    def post(self, request,*args,**kwargs) :

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data

        return Response(getSubject(subject,context=self.get_serializer_context()).data)