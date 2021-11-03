import json
from django.shortcuts import render
from system.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

def sinhvienViews(request):
    id_sinhvien = request.user.id
    s = sinhvien.objects.get(perm=id_sinhvien)
    return render(request,'templates/sinhvien.html',{"sinhvien":s})


    
def student_att(request):
    id_sinhvien = request.user.id
    s = sinhvien.objects.get(perm=id_sinhvien)
    hocphans = hocphan.objects.filter(id_lop=s.id_lop)
    return render(request,"templates/student_att.html",{"hocphans":hocphans})
@csrf_exempt
def danhsach_diemdanh(request):
    if request.method == "POST":
        id_hocphan = request.POST.get("id_hocphan")
    s = sinhvien.objects.get(perm=request.user.id)
    diemdanhs= diemdanh.objects.filter(id_hocphan=id_hocphan)
    print(id_hocphan)
    try:
        list_data = []
        for d in diemdanhs:
            a = attendance.objects.get(id_sinhvien_id = s.mssv,id_diemdanh_id = d.id)
            data = {"id":a.id,"id_diemdanh":d.id,"trangthai":a.diemdanh,"ngay_diem_danh":d.ngay_diem_danh}
            list_data.append(data)
        return HttpResponse(json.dumps(list_data,cls=DjangoJSONEncoder))
    except :
        return HttpResponse("Erorr")


@csrf_exempt
def deleteStudent(request):
    teacherID = request.POST.get("teacherID")
    try:
        studentObject = sinhvien.objects.get(pk=teacherID)
        studentUser = phanquyen.objects.get(username=teacherObject.perm)
        studentUser.delete()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
@csrf_exempt
def getupdateStudent(request):
    teacherID  = request.POST.get("teacherID")
    try:
        teacherObject = sinhvien.objects.get(mscb=teacherID)

        data = {"mscb":teacherObject.mscb,"ho":teacherObject.perm.first_name,"ten":teacherObject.perm.last_name,"diachi":teacherObject.dia_chi,"hocvan":teacherObject.hocvan,"sodienthoai":teacherObject.so_dien_thoai}
        return HttpResponse(json.dumps(data))
    except:
        return HttpResponse("Error")
@csrf_exempt
def updateStudent(request):
    teacherID  = request.POST.get("teacherID")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    diachi = request.POST.get("diachi")
    sodienthoai = request.POST.get("sodienthoai")
    try:
        print(teacherID)
        
        g = sinhvien.objects.get(pk=teacherID)
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
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")