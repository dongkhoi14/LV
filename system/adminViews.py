from django.core.checks import messages
from django.db.models.signals import post_save
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from system.giangvienViews import giangvienViews
from .models import phanquyen, giangvien, lop, hocphan, sinhvien
from django.shortcuts import render

@csrf_exempt
def themGiangvien(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        diachi = request.POST.get('diachi')
        sodienthoai = request.POST.get('sodienthoai')
        print(sodienthoai)
        try:
            user = phanquyen.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password, email=email, user_type=2)
            print("Toi day")
            user.giangvien.so_dien_thoai = sodienthoai
            user.giangvien.dia_chi=diachi
            user.save()
            return HttpResponseRedirect('adminGiangvien')
        except:
            return HttpResponseRedirect("adminThemgiangvien")


def toanbogiangvien(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/toanbogiangvien.html', {'giangviens': giangviens})

def toanbosinhvien(request):
    sinhviens = sinhvien.objects.all()
    return render(request,"templates/toanbosinhvien.html",{"sinhviens":sinhviens})
def change_teacher_info(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/change-teacher.html', {"giangviens": giangviens})

def change_student(request):
    sinhviens = sinhvien.objects.all()
    return render(request,"templates/change_student.html",{"sinhviens":sinhviens})
@csrf_exempt
def deleteTeacher(request):
    teacherID = request.POST.get("teacherID")
    try:
        teacherObject = giangvien.objects.get(pk=teacherID)
        teacherUser = phanquyen.objects.get(username=teacherObject.perm)
        teacherUser.delete()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
@csrf_exempt
def getupdateTeacher(request):
    teacherID  = request.POST.get("teacherID")
    try:
        teacherObject = giangvien.objects.get(mscb=teacherID)

        data = {"mscb":teacherObject.mscb,"ho":teacherObject.perm.first_name,"ten":teacherObject.perm.last_name,"diachi":teacherObject.dia_chi,"hocvan":teacherObject.hocvan,"sodienthoai":teacherObject.so_dien_thoai}
        return HttpResponse(json.dumps(data))
    except:
        return HttpResponse("Error")
@csrf_exempt
def updateTeacher(request):
    teacherID  = request.POST.get("teacherID")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    diachi = request.POST.get("diachi")
    sodienthoai = request.POST.get("sodienthoai")
    hocvan = request.POST.get("hocvan")
    print(type(hocvan))
    try:
        print(teacherID)
        
        g = giangvien.objects.get(pk=teacherID)
        u = phanquyen.objects.get(id= g.perm_id)
        if diachi != "":
            g.dia_chi = diachi
            g.save()

        if u.first_name != first_name:
            u.first_name = first_name
            u.save()
        if u.last_name != last_name:
            u.last_name = last_name
            u.save()
        if g.so_dien_thoai != sodienthoai:
            g.so_dien_thoai = sodienthoai
            g.save()
        g.hocvan = hocvan
        g.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
def themlop(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        ten_lop = request.POST.get('ten_lop')
        try:
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
            i = hocphan.objects.create(
                ten_hoc_phan=ten_hoc_phan, id_giangvien_id=id_giangvien, id_lop_id=id_lop)
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
        diachi = request.POST.get('diachi')
        sodienthoai = request.POST.get('sodienthoai')
        try:
            user = phanquyen.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password, email=email, user_type=3)
            user.sinhvien.id_lop_id = id_lop
            user.sinhvien.diachi = diachi
            user.sinhvien.so_dien_thoai = sodienthoai
            user.save()
            return HttpResponseRedirect("adminSinhvien")
        except:
            return HttpResponseRedirect("/")
