from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.signals import *
from django.dispatch import receiver
from django.db.models.fields import related

class phanquyen(AbstractUser):
    user_data = ((1,'quantri'), (2,'giangvien'), (3,'sinhvien'))
    user_type = models.CharField(choices= user_data, max_length=8,default=1 )


class quantri(models.Model):
    id = models.AutoField(primary_key=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    perm = models.OneToOneField(phanquyen,on_delete=models.CASCADE)
    objects=models.Manager()


        
class giangvien(models.Model):
    mscb = models.AutoField(primary_key=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    perm = models.OneToOneField(phanquyen, on_delete=models.CASCADE)
    objects=models.Manager()






class lop(models.Model):
    id = models.AutoField(primary_key=True)
    ten_lop = models.CharField(max_length=255)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)


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
    perm = models.OneToOneField(phanquyen,  on_delete=models.CASCADE)
    id_lop = models.ForeignKey(lop, on_delete=models.DO_NOTHING)
    objects=models.Manager()
    def __str__(self):
        return "MSSV : " +str(self.mssv) + ", Tên : " + self.perm.first_name + " " + self.perm.last_name 
    class Meta:
        ordering =["id_lop"]

class diemdanh(models.Model):
    id = models.AutoField(primary_key=True)
    id_hocphan = models.ForeignKey(hocphan, on_delete=CASCADE,related_name="att")
    ngay_diem_danh =  models.DateField()
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)



class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    id_sinhvien = models.ForeignKey(sinhvien, on_delete=DO_NOTHING)
    id_diemdanh = models.ForeignKey(diemdanh, on_delete=CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    diemdanh = models.BooleanField(default=False)








@receiver(post_save,sender=phanquyen)
def tao_nguoi_dung(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            quantri.objects.create(perm=instance)
        if instance.user_type==2:
            giangvien.objects.create(perm=instance)
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

