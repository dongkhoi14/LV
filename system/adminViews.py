from django.core.checks import messages
from django.db.models.signals import post_save
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from system.giangvienViews import giangvienViews
from .models import phanquyen, giangvien, lop, hocphan, sinhvien,diemdanh,attendance
from django.shortcuts import render

@csrf_exempt
def themGiangvien(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        ls_province = request.POST.get("ls_province")
        ls_district = request.POST.get("ls_district")
        ls_ward = request.POST.get("ls_ward")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        diachi = request.POST.get('diachi')
        sodienthoai = request.POST.get('sodienthoai')
        diachi = str(ls_province) + " " + str(ls_district) + " " + str(ls_ward)
        hocvan = request.POST.get('hocvan')
        
        try:
            print("ok")
            u = phanquyen.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email, user_type=2)
            u.save()
            a = giangvien.objects.create(perm= phanquyen.objects.get(pk=u.id))
            
            print("Toi day")
            a.so_dien_thoai = int(sodienthoai)
            a.dia_chi=diachi
            a.owner=request.user.username
            a.tentochuc= request.user.quantri.name
            a.hocvan = hocvan
            print("Toi day")
            
            a.save()
            return HttpResponseRedirect('adminGiangvien')
        except:
            return HttpResponseRedirect("adminThemgiangvien")
def adminHomeSchool(request):
    soluongsinhvien = sinhvien.objects.filter(owner=request.user.username).count()
    soluonggiangvien = giangvien.objects.filter(owner=request.user.username).count()
    soluonglop = lop.objects.filter(create_by= request.user.username).count()
    ls =lop.objects.filter(create_by= request.user.username)
    soluonghocphan = 0
    for l in ls :
        soluonghocphan += hocphan.objects.filter(id_lop_id=l.id).count()
    return render(request,"templates/adminHomeSchool.html",{'soluonglop':soluonglop,'soluonghocphan':soluonghocphan,'soluongsinhvien':soluongsinhvien,'soluonggiangvien':soluonggiangvien,})
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
            print("ok")
            u = phanquyen.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password, email=email, user_type=3)
            u.sinhvien.id_lop_id = id_lop
            u.sinhvien.diachi = diachi
            u.sinhvien.so_dien_thoai = sodienthoai
            u.sinhvien.owner = request.user.username
            u.sinhvien.tentochuc = request.user.quantri.name
            u.save()
            return HttpResponseRedirect("adminSinhvien")
        except:
            return HttpResponseRedirect("/")
def toanbogiangvien(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/toanbogiangvien.html', {'giangviens': giangviens})
def adminDiemdanh(request):
    return render(request,"templates/adminDiemdanh.html")
def toanbosinhvien(request):
    sinhviens = sinhvien.objects.filter(owner=request.user.username)
    return render(request,"templates/toanbosinhvien.html",{"sinhviens":sinhviens})
def change_teacher_info(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/change-teacher.html', {"giangviens": giangviens})

def change_student(request):
    sinhviens = sinhvien.objects.filter(owner=request.user.username)
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
            i = lop.objects.create(ten_lop=ten_lop,create_by=request.user.username)
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



@csrf_exempt
def onload_thongkeadmin(request):
    try:
        gs = giangvien.objects.filter(owner=request.user.username)
        list_data= []
        for g in gs:
            hocphans = hocphan.objects.filter(id_giangvien_id=g.mscb)
            
            for h in hocphans:
                ds = diemdanh.objects.filter(id_hocphan_id = h.id)
                tong_diemdanh = diemdanh.objects.filter(id_hocphan_id = h.id).count()
                tong = 0
                vang = 0
                comat= 0
                
                for d in ds:
                    atts = attendance.objects.filter(id_diemdanh_id=d.id)
                    tong += attendance.objects.filter(id_diemdanh_id=d.id).count()
                    slsv = attendance.objects.filter(id_diemdanh_id=d.id).count()
                    for att in atts:
                        
                        if att.diemdanh == False :
                            vang +=1
                        else : 
                            comat +=1
                tylecomat = int((comat/tong)*100)
                data = {"id_hocphan":h.id,"ten_hocphan":h.ten_hoc_phan,"so_buoi_diem_danh":tong_diemdanh,"soluongsinhvien":slsv,"tylecomat":tylecomat}
                list_data.append(data)
        print(list_data) 
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    except :
        return HttpResponse("Error")