from rest_framework import fields, serializers
from .models import *
from django.contrib.auth import authenticate
from .UserBackend import UserBackend
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView





class StudentID(serializers.ModelSerializer):
    class Meta:
        model = sinhvien
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = phanquyen
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'user_type')


class GetSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = hocphan
        fields = ['id', 'ten_hoc_phan']


class GetSubjectSerializer(serializers.ModelSerializer):
    subject = GetSubjectsSerializer(many=True, read_only=True)

    class Meta:
        model = lop
        fields = ['id', 'ten_lop', 'subject']


class getTeacher(serializers.ModelSerializer):
    class Meta:
        model = giangvien
        fields = ["mscb", "dia_chi", "so_dien_thoai", "hocvan"]


class getTeacherAll(serializers.ModelSerializer):
    teacher = getTeacher(many=False, read_only=True)

    class Meta:
        model = phanquyen
        fields = ["id", "first_name", "last_name", "email", "teacher"]

# ---- lịch sử điểm danh của sinh viên


class getAttData(serializers.ModelSerializer):

    class Meta:
        model = attendance
        fields = ['id', 'id_diemdanh', 'id_sinhvien', 'diemdanh']


class getAtt(serializers.ModelSerializer):
    attdetails = getAttData(many=True, read_only=True)

    class Meta:
        model = diemdanh
        fields = ['id', 'ngay_diem_danh', 'attdetails']


class getSubject(serializers.ModelSerializer):
    att = getAtt(many=True, read_only=True)

    class Meta:
        model = hocphan
        fields = ['id', 'ten_hoc_phan', 'att']

# lịch sưr nhân viên


class getStaffEventHistory(serializers.ModelSerializer):
    class Meta:
        model = staff_event
        fields = ['id_event', 'name', 'time_create',
                  'id_department', 'time_start', 'time_end']


class getAttStaffCheckin(serializers.ModelSerializer):
    class Meta:
        model = staff_event_checkin
        fields = '__all__'


class getAttStaffCheckOut(serializers.ModelSerializer):
    class Meta:
        model = staff_event_checkout
        fields = '__all__'


class getStaffHistorycheckin(serializers.ModelSerializer):
    staffcheckin = getAttStaffCheckin(many=True, read_only=True)
    staffcheckout = getAttStaffCheckOut(many=True, read_only=True)

    class Meta:
        model = sinhvien
        fields = ['mssv', 'staffcheckin', 'staffcheckout']


class HistoryCheckinSerilaizer(serializers.Serializer):
    mssv = serializers.IntegerField()

    def validate(self, data):
        h = UserBackend.authenticate_staff(self, **data)
        if h:
            return h
        raise serializers.ValidationError("Error")


class HistoryCheckinAPI(generics.GenericAPIView):
    serializer_class = HistoryCheckinSerilaizer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data

        return Response(getStaffHistorycheckin(att, context=self.get_serializer_context()).data)

# ----------sự kiện


class getAttStaffEvent(serializers.ModelSerializer):
    # eventcheckin = getAttStaffCheckin(many= True, read_only=True)
    # eventcheckout = getAttStaffCheckOut(many=True,read_only = True)
    class Meta:
        model = staff_event
        fields = ['id_event', 'name', 'time_create']


class getDepartment(serializers.ModelSerializer):
    departmentatt = getAttStaffEvent(many=True, read_only=True)

    class Meta:
        model = lop
        fields = ['ten_lop', 'departmentatt']


class GetDepartmentEvent(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_department(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class departmentHistoryEventAPI(generics.GenericAPIView):
    serializer_class = GetDepartmentEvent

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data

        return Response(getDepartment(att, context=self.get_serializer_context()).data)


class GetStaffCheckinEvent(serializers.Serializer):
    id_event = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_evetn_check_in(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class StaffEventCheckinAPI(generics.GenericAPIView):
    serializer_class = GetStaffCheckinEvent

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data

        return Response(getAttStaffCheckin(att, context=self.get_serializer_context()).data)


class GetStaffCheckoutEvent(serializers.Serializer):
    id_event = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_evetn_check_out(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class StaffEventCheckoutAPI(generics.GenericAPIView):
    serializer_class = GetStaffCheckoutEvent

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data

        return Response(getAttStaffCheckOut(att, context=self.get_serializer_context()).data)
#-----------

# ----------


class getAttDataStudent(serializers.ModelSerializer):
    attdata = getAttData(many=True, read_only=True)

    class Meta:
        model = sinhvien
        fields = ['attdata']


class getAttDataDetail(serializers.ModelSerializer):
    class Meta:
        model = attendance
        fields = ['id']


class getAttStaff(serializers.ModelSerializer):
    class Meta:
        model = staff_att
        fields = ['id']


class getAttStaffDetailIn(serializers.ModelSerializer):
    class Meta:
        model = staffDo_att_in
        fields = ['id', 'id_department',
                  'id_diemdanh', 'id_nhanvien', 'diemdanh','ngay_cap_nhat']


class getAttStaffDetailOut(serializers.ModelSerializer):
    class Meta:
        model = staffDo_att_out
        fields = ['id', 'id_department',
                  'id_diemdanh', 'id_nhanvien', 'diemdanh','ngay_cap_nhat']
# -----------------lich su nhan vien


class ListStaffAtt(APIView):
    def get(self, request, format=None):
        a = staff_att.objects.all()
        list_data = []
        for i in a:

            data = {
                "id": i.id,
                "ngay_tao": i.ngay_tao,
                
            }
            list_data.append(data)
        list_data.reverse()
        return Response(list_data)
class ValidateStaffAttIn(serializers.Serializer):
    id_diemdanh = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()
    
    def validate(self,data,*args, **kwargs):
        a = UserBackend.authenticate_staff_checkin(self,**data)
        if a:
            return a
        raise serializers.ValidationError("Error")
class StaffInAPI(generics.GenericAPIView):
    serializer_class = ValidateStaffAttIn

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data
        return Response(getAttStaffDetailIn(att, context=self.get_serializer_context()).data)

class ValidateStaffAttOut(serializers.Serializer):
    id_diemdanh = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()
    
    def validate(self,data,*args, **kwargs):
        a = UserBackend.authenticate_staff_checkout(self,**data)
        if a:
            return a
        raise serializers.ValidationError("Error")
class StaffOutAPI(generics.GenericAPIView):
    serializer_class = ValidateStaffAttOut

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        att = serializer.validated_data
        return Response(getAttStaffDetailOut(att, context=self.get_serializer_context()).data)
#--------------------------
class getAttStudent(serializers.ModelSerializer):
    class Meta:
        model = attendance
        fields = ['id', 'diemdanh', 'id_diemdanh_id']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        user = UserBackend.authenticate(self, **data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Error")

# Base on perm_id = phanquyen.id


class StudentIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        user = UserBackend.authenticate_student(self, **data)
        if user:
            return user
        raise serializers.ValidationError("Loi")


class SubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        l = UserBackend.authenticate_subject(self, **data)
        if l:
            return l
        raise serializers.ValidationError("Error")


class AttStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        h = UserBackend.authenticate_att_student(self, **data)
        if h:
            return h
        raise serializers.ValidationError("Error")


class AttSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        h = UserBackend.authenticate_att(self, **data)
        if h:
            return h
        raise serializers.ValidationError("Error")


class AttDetailStaffInSerializer(serializers.Serializer):
    id_nhanvien = serializers.IntegerField()
    id_diemdanh = serializers.IntegerField()
    id_department = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_att_staff_in(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttDetailSerializer(serializers.Serializer):
    mssv = serializers.IntegerField()
    id_diemdanh = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_att_data(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttDetailStaffOutSerializer(serializers.Serializer):
    id_nhanvien = serializers.IntegerField()
    id_diemdanh = serializers.IntegerField()
    id_department = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_att_staff_out(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")

# staff checkin event


class getStaffEvent(serializers.ModelSerializer):
    class Meta:
        model = staff_event
        fields = ['id_event', 'name', 'time_create',
                  'id_department', 'time_start', 'time_end']


class getEventCheckin(serializers.ModelSerializer):
    eventcheckin = getStaffEvent(many=True, read_only=True)

    class Meta:
        model = staff_event_checkin
        fields = ['id', 'checkin', 'eventcheckin']


class AttStaffEventSerializer(serializers.Serializer):
    time_create = serializers.DateField()
    time_start = serializers.DateTimeField()
    name = serializers.CharField()
    id_department = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticatie_att_event_checkin(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttStaffEventDetailIn(serializers.Serializer):
    id_event = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticatie_att_event_detail_checkin(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttStaffEventDetailInAPI(generics.GenericAPIView):
    serializer_class = AttStaffEventDetailIn

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eventdetail = serializer.validated_data
        return Response(getEventCheckin(eventdetail, context=self.get_serializer_context()).data)


class AttStaffEventAPICheckin(generics.GenericAPIView):
    serializer_class = AttStaffEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.validated_data
        return Response(getStaffEvent(event, context=self.get_serializer_context()).data)


class UpdateAttEventDataInAPI(generics.UpdateAPIView):
    serializer_class = getEventCheckin
    queryset = staff_event_checkin.objects.all()
# staff checkout event


class getEventCheckOut(serializers.ModelSerializer):
    eventcheckout = getStaffEvent(many=True, read_only=True)

    class Meta:
        model = staff_event_checkout
        fields = ['id', 'checkout', 'eventcheckout']


class AttStaffEventOutSerializer(serializers.Serializer):
    time_create = serializers.DateField()
    time_start = serializers.DateTimeField()
    name = serializers.CharField()
    id_department = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticatie_att_event_checkin(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttStaffEventDetailOut(serializers.Serializer):
    id_event = serializers.IntegerField()
    id_nhanvien = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticatie_att_event_detail_checkout(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class AttStaffEventDetailOutAPI(generics.GenericAPIView):
    serializer_class = AttStaffEventDetailOut

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eventdetail = serializer.validated_data
        return Response(getEventCheckOut(eventdetail, context=self.get_serializer_context()).data)


class AttStaffEventAPICheckout(generics.GenericAPIView):
    serializer_class = AttStaffEventOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.validated_data
        return Response(getStaffEvent(event, context=self.get_serializer_context()).data)


class UpdateAttEventDataOutAPI(generics.UpdateAPIView):
    serializer_class = getEventCheckOut
    queryset = staff_event_checkout.objects.all()
# check out cua sinh vien


class getAttDataOut(serializers.ModelSerializer):

    class Meta:
        model = attendance
        fields = ['id', 'id_diemdanh', 'id_sinhvien', 'diemdanh']


class getAttOut(serializers.ModelSerializer):
    attdetails = getAttData(many=True, read_only=True)

    class Meta:
        model = diemdanh
        fields = ['id', 'ngay_diem_danh', 'attdetailsout']


class AttDetailOutSerializer(serializers.Serializer):
    mssv = serializers.IntegerField()
    id_diemdanh = serializers.IntegerField()

    def validate(self, data):
        a = UserBackend.authenticate_att_data_out(self, **data)
        if a:
            return a
        raise serializers.ValidationError("Error")


class getAttDetailAPIOut(generics.GenericAPIView):
    serializer_class = AttDetailOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attDetailOut = serializer.validated_data
        return Response(getAttDataOut(attDetailOut, context=self.get_serializer_context()).data)


class UpdateAttDataOutAPI(generics.UpdateAPIView):
    serializer_class = getAttDataOut
    queryset = attendance_out.objects.all()

# @api_view(['GET'])
# def historystaffapi(request,pk):
#     try:
#         c = staffDo_att_in.objects.all(pk=pk)
#     except staffDo_att_in.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
