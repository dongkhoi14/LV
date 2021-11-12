from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.signals import *
from django.dispatch import receiver
from django.db.models.fields import related
from datetime import datetime,timedelta
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
        
class giangvien(models.Model):
    hocvan_choice = ((1,"Dai Hoc"),(2,"Thac Si"),(3,"Tien Si"),(4,"Giao Su"))
    mscb = models.AutoField(primary_key=True)
    gioitinh = models.BooleanField(default=True)

    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    perm = models.OneToOneField(phanquyen, on_delete=models.CASCADE,related_name="teacher")
    dia_chi = models.CharField(max_length=255,blank=True,null=True)
    so_dien_thoai = models.IntegerField(null=True)
    hocvan = models.CharField(max_length=255)
    owner = models.CharField(max_length=255,blank=True,null=True)
    objects=models.Manager()






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
    def __str__(self):
        return "MSSV : " +str(self.mssv) + ", Tên : " + self.perm.first_name + " " + self.perm.last_name 
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
    id_diemdanh = models.ForeignKey(diemdanh, on_delete=CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)

class attendance_out(models.Model):
    id = models.AutoField(primary_key=True)
    id_sinhvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING,related_name='attendance_out')
    id_diemdanh = models.ForeignKey(diemdanh, on_delete=CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)



class notifications(models.Model):
    id = models.AutoField(primary_key=True)
    id_giangvien = models.ForeignKey(giangvien,on_delete=models.CASCADE)
    noti_content = models.TextField()
    noti_title = models.CharField(max_length=255,blank=True)
    id_hocphan = models.ForeignKey(hocphan, on_delete=models.CASCADE,default="1")
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)



    
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
@receiver(post_save,sender=phanquyen)
def tao_nguoi_dung(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            quantri.objects.create(perm=instance,type=1)
        if instance.user_type==2:
            giangvien.objects.create(perm=instance,hocvan="1")
        if instance.user_type==3:
            sinhvien.objects.create(perm=instance, id_lop=lop.objects.get(id=2))
        

@receiver(post_save,sender=phanquyen)
def them_nguoi_dung(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.quantri.save()
    if instance.user_type==2:
        instance.giangvien.save()
    if instance.user_type==3:
        instance.sinhvien.save()
    
