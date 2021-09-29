from django.core.checks import messages
from django.db.models.signals import post_save
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import phanquyen, giangvien, lop,hocphan, sinhvien
from django.shortcuts import render


def themGiangvien(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = phanquyen.objects.create_user(username = username, first_name = first_name, last_name  =last_name,password = password,email = email, user_type = 2 )
            user.save()
            return HttpResponseRedirect('adminGiangvien')
        except:
            messages.Error("Khoong the them Giang vien")
            return HttpResponseRedirect("/")

def toanbogiangvien(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/toanbogiangvien.html', {'giangviens':giangviens})


def themlop(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else :
        ten_lop = request.POST.get('ten_lop')
        try :
            i = lop.objects.create(ten_lop=ten_lop)
            i.save()
            return HttpResponseRedirect('adminLop')
        except:
            return HttpResponseRedirect("/")
        
def themhocphan(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        ten_hoc_phan = request.POST.get('ten_mon_hoc')
        id_lop = request.POST.get('id_lop')
        id_giangvien = request.POST.get('mscb')
        try:
            i = hocphan.objects.create(ten_hoc_phan = ten_hoc_phan,id_giangvien_id = id_giangvien, id_lop_id = id_lop)
            i.save()
            return HttpResponseRedirect("adminLop")
        except:
            return HttpResponseRedirect("/")


def themsinhvien(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        id_lop = request.POST.get('id')
        try:
            user = phanquyen.objects.create_user(username = username, first_name = first_name, last_name  =last_name,password = password,email = email,user_type = 3 )
            user.sinhvien.id_lop_id = id_lop
            user.save()      
            return HttpResponseRedirect("adminSinhvien")
        except:
            return HttpResponseRedirect("/")


