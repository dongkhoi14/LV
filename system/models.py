from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.signals import *
from django.dispatch import receiver
from django.db.models.fields import related
from datetime import datetime, time,timedelta
from django.utils import timezone
class phanquyen(AbstractUser):
    user_data = ((1,'quantri'), (2,'giangvien'), (3,'sinhvien'),(4,'staff'))
    user_type = models.CharField(choices= user_data, max_length=8,default=1 )

class quantri(models.Model):
    id = models.AutoField(primary_key=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    perm = models.OneToOneField(phanquyen,on_delete=models.CASCADE)
    objects=models.Manager()
    type_data = ((1,'school'),(2,'company'))
    gioitinh = models.BooleanField(default=True)
    type = models.CharField(choices=type_data,max_length=255,default=1)
    name = models.CharField(max_length=254,default="")
        
class giangvien(models.Model):
    mscb = models.AutoField(primary_key=True)
    gioitinh = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    perm = models.OneToOneField(phanquyen, on_delete=models.CASCADE,related_name="teacher")
    dia_chi = models.CharField(max_length=255,blank=True,null=True)
    so_dien_thoai = models.IntegerField(null=True)
    hocvan = models.CharField(max_length=255,default=1)
    owner = models.CharField(max_length=255,blank=True,null=True)
    objects=models.Manager()
    tentochuc = models.CharField(max_length=254,default="")







class lop(models.Model):
    id = models.AutoField(primary_key=True)
    ten_lop = models.CharField(max_length=255)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=255,default=None)

class hocphan(models.Model):
    id = models.AutoField(primary_key=True)
    ten_hoc_phan =models.CharField(max_length=255)
    id_lop = models.ForeignKey(lop, on_delete=models.CASCADE, default="", related_name='subject')
    id_giangvien = models.ForeignKey(giangvien, on_delete=models.CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%d : %s ' % (self.id,self.ten_hoc_phan)


class sinhvien(models.Model):

    mssv = models.AutoField(primary_key=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    gioitinh = models.BooleanField(default=True)
    perm = models.OneToOneField(phanquyen,  on_delete=models.CASCADE)
    id_lop = models.ForeignKey(lop, on_delete=models.DO_NOTHING)
    diachi = models.CharField(max_length=255,null=True,blank=True)
    so_dien_thoai = models.IntegerField(null=True)
    owner = models.CharField(max_length=255,blank=True,null=True)
    objects=models.Manager()
    tentochuc = models.CharField(max_length=254,default="")

    def __str__(self):
        return "MSSV : " +str(self.mssv) + ", T??n : " + self.perm.first_name + " " + self.perm.last_name 
    class Meta:
        ordering =["id_lop"]

class diemdanh(models.Model):
    id = models.AutoField(primary_key=True)
    id_hocphan = models.ForeignKey(hocphan, on_delete=CASCADE,related_name="att")
    ngay_diem_danh =  models.DateField()
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)
    
    
        



class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    id_sinhvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING,related_name='attdata')
    id_diemdanh = models.ForeignKey(diemdanh, on_delete=CASCADE,related_name="attdetails")
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)

class attendance_out(models.Model):
    id = models.AutoField(primary_key=True)
    id_sinhvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING,related_name='attdataout')
    id_diemdanh = models.ForeignKey(diemdanh, on_delete=CASCADE,related_name="attdetailsout")
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)









    
class staff_att(models.Model):
    id = models.AutoField(primary_key=True)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)

class staffDo_att_in(models.Model):
    id = models.AutoField(primary_key=True)
    id_nhanvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING)
    id_diemdanh = models.ForeignKey(staff_att, on_delete=CASCADE)
    id_department = models.ForeignKey(lop, on_delete=CASCADE,default=1)

    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)
class staffDo_att_out(models.Model):
    id = models.AutoField(primary_key=True)
    id_nhanvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING)
    id_diemdanh = models.ForeignKey(staff_att, on_delete=CASCADE)
    id_department = models.ForeignKey(lop, on_delete=CASCADE,default=1)
    ngay_tao = models.DateTimeField(default=timezone.now)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)

class staff_event(models.Model):
    id_event = models.AutoField(primary_key=True)
    time_create = models.DateField(default=timezone.now)
    name = models.CharField(max_length=254,default="")
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    id_department = models.ForeignKey(lop, on_delete=CASCADE,default=1,related_name="departmentatt")
    is_disabled = models.BooleanField(default=False)

class staff_event_checkin(models.Model):
    id = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(staff_event,on_delete=CASCADE,related_name="eventcheckin")
    checkin = models.BooleanField(default=False)
    timecheckin = models.DateTimeField(auto_now=True)
    id_nhanvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING,default=None,related_name="staffcheckin")

class staff_event_checkout(models.Model):
    id = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(staff_event,on_delete=CASCADE,related_name="eventcheckout")
    checkout = models.BooleanField(default=False)
    timecheckout = models.DateTimeField(auto_now=True)
    id_nhanvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING,default=None,related_name="staffcheckout")

@receiver(post_save,sender=staff_event)
def createevent(sender,instance,created,**kwargs):
    if created:
        ss = sinhvien.objects.filter(id_lop_id = instance.id_department)
        for s in ss:
            i = staff_event_checkin.objects.create(id_event = instance,id_nhanvien_id=s.mssv)
            i.save()
            o = staff_event_checkout.objects.create(id_event = instance,id_nhanvien_id=s.mssv)
            o.save()
    
@receiver(post_save,sender=phanquyen)
def tao_nguoi_dung(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            quantri.objects.create(perm=instance,type=1)
        if instance.user_type==3:
            sinhvien.objects.create(perm=instance, id_lop=lop.objects.get(id=1))
        

@receiver(post_save,sender=phanquyen)
def them_nguoi_dung(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.quantri.save()
    if instance.user_type==3:
        instance.sinhvien.save()
    
    
