from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel
from system.models import *
from datetime import timedelta,datetime

class UserBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def authenticate_student(self, id=None,**kwargs):
        
        try:
            user = sinhvien.objects.get(perm_id=id)
        except  sinhvien.DoesNotExist:
            return None
        else:
            return user
    

    def authenticate_subject(self, id=None,**kwargs):

        try :
            c = lop.objects.get(pk=id)
            
        except  lop.DoesNotExist :
            return None
        else:
            
            return c
    def authenticate_att(self,id=None,**kwargs):
        
        try :
            h = hocphan.objects.get(pk=id)
            
        except  hocphan.DoesNotExist :
            return None
        else:
            
            return h
    def authenticate_att_student(self,id=None,**kwargs):
        try:
            a = attendance.objects.get(pk=id)
            print(a)
        except attendance.DoesNotExist:
            return None
        else:
            return a
    def authenticate_att_data(self,mssv=None,id_diemdanh=None,**kwargs):
        try:
            a = attendance.objects.get(id_sinhvien=mssv,id_diemdanh=id_diemdanh)
        except  attendance.DoesNotExist :
            return None
        else:
            return a
    def authenticate_att_data_out(self,mssv = None,id_diemdanh=None,**kwargs):
        try:
            a=attendance_out.objects.get(id_sinhvien = mssv,id_diemdanh=id_diemdanh)
        except attendance_out.DoesNotExist:
            return None
        else:
            return a
    def authenticate_att_staff_in(self,id_nhanvien = None,id_diemdanh =None,id_department = None,**kwargs):
        try:
            a = staffDo_att_in.objects.get(id_nhanvien=id_nhanvien,id_diemdanh=id_diemdanh,id_department=id_department)
        except staffDo_att_in.DoesNotExist :
            return None
        else:
            return a
    def authenticate_att_staff_out(self,id_nhanvien = None,id_diemdanh =None,id_department = None,**kwargs):
        try:
            a = staffDo_att_out.objects.get(id_nhanvien=id_nhanvien,id_diemdanh=id_diemdanh,id_department=id_department)
        except staffDo_att_out.DoesNotExist :
            return None
        else:
            return a
    def authenticatie_att_event_checkin(self,name=None,time_create=None,time_start = None,id_department=None,**kwargs):
        try:
            a = staff_event.objects.get(name= name,time_create =time_create,id_department = id_department )
            
        except staff_event.DoesNotExist:
            return None
        else:
            return a
        
    
    def authenticatie_att_event_detail_checkin(self, id_event = None,id_nhanvien = None,**kwargs):
        try:
            a = staff_event_checkin.objects.get(id_event_id = id_event,id_nhanvien_id = id_nhanvien)
        except staff_event_checkin.DoesNotExist:
            return None
        else:
            return a
    def authenticatie_att_event_detail_checkout(self, id_event = None,id_nhanvien = None,**kwargs):
        try:
            a = staff_event_checkout.objects.get(id_event_id = id_event,id_nhanvien_id = id_nhanvien)
        except staff_event_checkout.DoesNotExist:
            return None
        else:
            return a

