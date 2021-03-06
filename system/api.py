from functools import partial
from django.db.models.fields import mixins
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
            "token":AuthToken.objects.create(user)[1]

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
        att = serializer.validated_data

        return Response(getSubject(att,context=self.get_serializer_context()).data)



class UpdateAttDataAPI(generics.UpdateAPIView):
    serializer_class  = getAttData
    queryset = attendance.objects.all()
class UpdateAttDataStaffInAPI(generics.UpdateAPIView):
    serializer_class  = getAttStaffDetailIn
    queryset = staffDo_att_in.objects.all()
class UpdateAttDataStaffOutAPI(generics.UpdateAPIView):
    serializer_class  = getAttStaffDetailOut
    queryset = staffDo_att_out.objects.all()

class getAttStudentAPI(generics.GenericAPIView):
    serializer_class = AttStudentSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attStudent = serializer.validated_data
        return Response(getAttStudent(attStudent,context=self.get_serializer_context()).data)
class getAttDetailAPI(generics.GenericAPIView):
    serializer_class = AttDetailSerializer
    def post(self, request,*args,**kwargs) :
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attDetail = serializer.validated_data
        return Response(getAttData(attDetail,context=self.get_serializer_context()).data)
    
class getAttDetailStaffInAPI(generics.GenericAPIView):
    serializer_class = AttDetailStaffInSerializer
    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        attDetailStaffIn = serializer.validated_data
        return Response(getAttStaffDetailIn(attDetailStaffIn,context=self.get_serializer_context()).data)
class getAttDetailStaffOutAPI(generics.GenericAPIView):
    serializer_class = AttDetailStaffOutSerializer
    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        attDetailStaffOut = serializer.validated_data
        return Response(getAttStaffDetailOut(attDetailStaffOut,context=self.get_serializer_context()).data)
  

