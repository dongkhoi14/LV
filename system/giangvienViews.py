import json
from django.http import response
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import attendance, lop, giangvien, hocphan, notifications, sinhvien, diemdanh
from rest_framework import viewsets
from django.http import request
from django.core.serializers.json import DjangoJSONEncoder
import qrcode
from django.http import FileResponse
from django.core.checks import messages


def giangvienViews(request):
    g = giangvien.objects.get(perm=request.user.id)

    return render(request, 'templates/giangvien.html', {'giangvien': g})


def giangvien_Lop(request):
    lops = lop.objects.all()
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, 'templates/giangvien_Lop.html', {'lops': lops, 'hocphans': hocphans})


def giangvien_diemdanh(request):
    lops = lop.objects.all()
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, "templates/giangvien_diemdanh.html", {"lops": lops, "hocphans": hocphans})


def giangvienNoti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, 'templates/giangvienNoti.html', {'hocphans': hocphans})


def addNoti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, "templates/giangvien_addNoti.html", {'hocphans': hocphans})


def noti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, 'templates/noti.html', {'hocphans': hocphans})


def addNotifications(request):
    if request.method != "POST":
        return HttpResponse("<h2>Lỗi</h2>")
    else:
        notiTitle = request.POST.get("notiTitle")
        notiContent = request.POST.get('notiContent')
        g = giangvien.objects.get(perm=request.user.id)
        id_giangviens = g.mscb
        id = request.POST.get('id')
        try:
            print("den day la duoc")
            noti = notifications.objects.create(
                id_giangvien_id=id_giangviens, noti_content=notiContent, noti_title=notiTitle, id_hocphan_id=id)
            noti.save()
            return HttpResponseRedirect('thongbao')
        except:
            messages.Error("Khoong the them thong bao")
            return HttpResponseRedirect('addNoti')


@csrf_exempt
def danhsach_sinhvien(request):
    id_hocphan = request.POST.get("id_hocphan")
    lops = hocphan.objects.get(id=id_hocphan)
    sinhviens = sinhvien.objects.filter(id_lop=lops.id_lop)
    list_data = []
    for s in sinhviens:
        data = {"id": s.mssv, "name": s.perm.first_name +
                " " + s.perm.last_name, "lop": s.id_lop.ten_lop}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def historyAtt(request):
    id_hocphan = request.POST.get("id_hocphan")
    ngay_diem_danhh = request.POST.get("ngay_diem_danh")
    atts = diemdanh.objects.filter(
        id_hocphan_id=id_hocphan, ngay_diem_danh=ngay_diem_danhh)
    list_data = []

    for data in atts:
        data = {"id": data.id, "ngay_diem_danh": data.ngay_diem_danh,
                "ten_lop": data.id_hocphan.ten_hoc_phan}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)


@csrf_exempt
def deleteAtt(request):
    id_diemdanh = request.POST.get("id_diemdanh")

    print(id_diemdanh)
    try:

        d = diemdanh.objects.get(id=id_diemdanh)
        print(id_diemdanh)
        d.delete()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


@csrf_exempt
def createAtt(request):
    id_hocphan = request.POST.get("id_hocphan")
    ngay_diem_danh = request.POST.get("ngay_diem_danh")
    list_data = []
    try:
        c = diemdanh.objects.create(
            id_hocphan_id=id_hocphan, ngay_diem_danh=ngay_diem_danh)
        c.save()
        currentAtt = diemdanh.objects.filter(
            id_hocphan=id_hocphan, ngay_diem_danh=ngay_diem_danh).latest('ngay_tao')
        s = hocphan.objects.get(id=id_hocphan)
        l = lop.objects.get(id=s.id_lop_id)
        students = sinhvien.objects.filter(id_lop_id=l.id)
        for student in students:
            att = attendance.objects.create(
                id_sinhvien_id=student.mssv, id_diemdanh_id=currentAtt.id)
            att.save()
        print(students)
        data = {"id": currentAtt.id, "ngay_diem_danh": currentAtt.ngay_diem_danh,
                "tenlop": currentAtt.id_hocphan.ten_hoc_phan}
        list_data.append(data)
        print(list_data)

        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)
    except:
        return HttpResponse("ERR")


@csrf_exempt
def createQR(request):
    id_diemdanh = request.POST.get("id_diemdanh")
    ngay_diem_danh = request.POST.get("ngay_diem_danh")
    filename = "static/images/qrcodes/"+id_diemdanh+ngay_diem_danh+".png"
    url = "/static/images/qrcodes/"+id_diemdanh+ngay_diem_danh+".png"

    response_data = {
        'url': url
    }
    try:
        img = qrcode.make(id_diemdanh+ngay_diem_danh)
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")
@csrf_exempt
def historyAttData(request):
    id_diemdanh = request.POST.get("id_diemdanh")
    print(id_diemdanh)
    try:
        att = attendance.objects.filter(id_diemdanh_id=id_diemdanh)
        list_data = []
        for a in att:
            s = sinhvien.objects.get(mssv = a.id_sinhvien_id)
            print(a)
            context = {"mssv" : s.mssv,"ho":s.perm.first_name,"ten":s.perm.last_name,"trangthai":a.diemdanh,"id_att":a.id}
            list_data.append(context)
        return JsonResponse(json.dumps(list_data),content_type="application/json", safe=False)
        
    except :
        return HttpResponse("Not ok")

@csrf_exempt
def allnoti(request):
    id_hocphans = request.POST.get("id_hocphan")
    g = giangvien.objects.get(perm=request.user.id)
    id_giangviens = g.mscb
    try:
        notis = notifications.objects.filter(
            id_hocphan_id=id_hocphans, id_giangvien_id=id_giangviens)
        list_data = []
        for noti in notis:
            data = {"id": noti.id, "noti_title": noti.noti_title,
                    "noti_content": noti.noti_content, "ngay_tao": noti.ngay_tao}
            list_data.append(data)
        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)
    except:
        return HttpResponse("Error")


@csrf_exempt
def deleteNoti(request):
    id_noti = request.POST.get("id")
    id_noti = int(id_noti)
    try:
        noti = notifications.objects.get(pk=id_noti)
        noti.delete()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
