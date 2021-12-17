import json
from django.http import response
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import attendance, attendance_out, lop, giangvien, hocphan, sinhvien, diemdanh
from rest_framework import viewsets
from django.http import request
from django.core.serializers.json import DjangoJSONEncoder
import qrcode
from django.http import FileResponse
from django.core.checks import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def giangvienViews(request):
    g = giangvien.objects.get(perm=request.user.id)

    return render(request, 'templates/giangvien.html', {'giangvien': g})

@login_required(login_url='login')
def giangvien_Lop(request):
    lops = lop.objects.all()
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    list_data = []
    for h in hocphans:
        slsv = sinhvien.objects.filter(id_lop=h.id_lop_id).count()
        data = {"tenhocphan":h.ten_hoc_phan,"tenlop":lop.objects.get(id = h.id_lop_id).ten_lop,"slsv":slsv}
        
        list_data.append(data)
    return render(request, 'templates/giangvien_Lop.html', {"list_data":json.dumps(list_data)})
@login_required(login_url='login')
def lopgiangvien(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    list_data = []
    for h in hocphans:
        slsv = sinhvien.objects.filter(id_lop=h.id_lop_id).count()
        data = {"tenhocphan":h.ten_hoc_phan,"tenlop":lop.objects.get(id = h.id_lop_id).ten_lop,"slsv":slsv}
        
        list_data.append(data)
    return JsonResponse(json.dumps(list_data),content_type = 'application/json',safe=False)
@login_required(login_url='login')
def giangvien_diemdanh(request):
    lops = lop.objects.all()
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, "templates/giangvien_diemdanh.html", {"lops": lops, "hocphans": hocphans})

@login_required(login_url='login')
def giangvienNoti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, 'templates/giangvienNoti.html', {'hocphans': hocphans})

@login_required(login_url='login')
def addNoti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, "templates/giangvien_addNoti.html", {'hocphans': hocphans})

@login_required(login_url='login')
def noti(request):
    g = giangvien.objects.get(perm=request.user.id)
    hocphans = hocphan.objects.filter(id_giangvien=g.mscb)
    return render(request, 'templates/noti.html', {'hocphans': hocphans})

@login_required(login_url='login')
def thongke(request):

    return render(request, "templates/thongke_diemdanh.html")

@login_required(login_url='login')
@csrf_exempt
def onload_thongke(request):
    try:
        g = giangvien.objects.get(perm=request.user.id)
        hocphans = hocphan.objects.filter(id_giangvien_id=g.mscb)
        list_data = []
        print(hocphans)
        for h in hocphans:
            ds = diemdanh.objects.filter(id_hocphan_id=h.id)
            tong_diemdanh = diemdanh.objects.filter(id_hocphan_id=h.id).count()
            tong = 0
            vang = 0
            comat = 0
            slsv = sinhvien.objects.filter(id_lop_id = h.id_lop).count()
            for d in ds:
                atts = attendance.objects.filter(id_diemdanh_id=d.id)
                tong += attendance.objects.filter(id_diemdanh_id=d.id).count()
                
                for att in atts:

                    if att.diemdanh == False:
                        vang += 1
                    else:
                        comat += 1
            tylecomat = int((comat/tong)*100)
            data = {"id_hocphan": h.id, "ten_hocphan": h.ten_hoc_phan,
                    "so_buoi_diem_danh": tong_diemdanh, "soluongsinhvien": slsv, "tylecomat": tylecomat}
            list_data.append(data)
            print(list_data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    except:
        return HttpResponse("Error")

@login_required(login_url='login')
@csrf_exempt
def details_thongke(request):
    if request.method == "POST":
        id_hocphan = request.POST.get("id_hocphan")
    try:
        h = hocphan.objects.get(pk=id_hocphan)
        l = lop.objects.get(pk=h.id_lop_id)
        ss = sinhvien.objects.filter(id_lop_id=l.id)  # Lay danh sach sinh vien
        ds = diemdanh.objects.filter(id_hocphan_id=id_hocphan)  # lay diem danh
        list_data = []
        for s in ss:
            count = 0
            for d in ds:
                count += attendance.objects.filter(
                    id_sinhvien=s.mssv, id_diemdanh=d.id, diemdanh=False).count()
            data = {"name": s.perm.first_name + " " +
                    s.perm.last_name, "mssv": s.mssv, "solanvang": count}

            list_data.append(data)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    except:
        return HttpResponse("Error")

@login_required(login_url='login')
@csrf_exempt
def danhsach_sinhvien(request):
    id_hocphan = request.POST.get("id_hocphan")
    lops = hocphan.objects.get(id=id_hocphan)
    sinhviens = sinhvien.objects.filter(id_lop=lops.id_lop)
    diemdanhs = diemdanh.objects.filter(id_hocphan_id=id_hocphan)
    for d in diemdanhs:
        if d.is_disabled != True and timezone.now() > (d.ngay_tao + timedelta(days=2)):
            d.is_disabled = True
            d.save()
        
    list_data = []
    for s in sinhviens:
        if s.perm.is_active == True:
            data = {"id": s.mssv, "name": s.perm.first_name +
                    " " + s.perm.last_name, "lop": s.id_lop.ten_lop}
            list_data.append(data)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@login_required(login_url='login')
@csrf_exempt
def historyAtt(request):
    id_hocphan = request.POST.get("id_hocphan")
    ngay_diem_danhh = request.POST.get("ngay_diem_danh")
    atts = diemdanh.objects.filter(
        id_hocphan_id=id_hocphan)
    list_data = []
    tong = 0
    for data in atts:

        att_in = attendance.objects.filter(id_diemdanh_id=data.id)
        count = 0
        s = attendance_out.objects.filter(id_diemdanh_id=data.id)

        for att in att_in:
            
            try:
                s = sinhvien.objects.get(mssv = att.id_sinhvien_id)
                print(s)
                if s.perm.is_active == True:
                    att_out = attendance_out.objects.get(id_diemdanh_id=att.id_diemdanh, id_sinhvien_id=att.id_sinhvien)
                    tong +=1
                    if att.diemdanh == True and att_out.diemdanh == True:
                        count += 1
            except :
                s = sinhvien.objects.get(mssv = att.id_sinhvien_id)
                print(s)
                if s.perm.is_active == True:
                    tong+=1
                    if att.diemdanh == True :
                        count += 1


        if data.is_disabled == True:
            trangthai = "disabled"
        else:
            trangthai = "enabled"
        data = {"id": data.id, "ngay_diem_danh": data.ngay_diem_danh,
                "ten_lop": data.id_hocphan.ten_hoc_phan, "dadiemdanh": count, "tong": tong, "trangthai": trangthai}
        list_data.append(data)
        list_data.reverse()
    return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)

@login_required(login_url='login')
@csrf_exempt
def deleteAtt(request):
    id_diemdanh = request.POST.get("id_diemdanh")

    try:

        d = diemdanh.objects.get(id=id_diemdanh)
        d.delete()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

@login_required(login_url='login')
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
        data = {"id": currentAtt.id, "ngay_diem_danh": currentAtt.ngay_diem_danh,
                "tenlop": currentAtt.id_hocphan.ten_hoc_phan}
        list_data.append(data)

        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)
    except:
        return HttpResponse("ERR")

@login_required(login_url='login')
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
        img = qrcode.QRCode(
            version=1,
            box_size=40,
            border=4,
        )
        img = qrcode.make(id_diemdanh+ngay_diem_danh+"0")
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")

@login_required(login_url='login')
@csrf_exempt
def historyAttData(request):
    id_diemdanh = request.POST.get("id_diemdanh")
    context = {"id_diemdanh": "",
                    "mssv": "",
                    "ho": "",
                    "ten": "",
                    "trangthai_in": "",
                    "trangthai_out": "",
                    "id_att_in": "",
                    "id_att_out":"",
                    "ngay_diem_danh": "",
                    
                    }
    try:
        d = diemdanh.objects.get(pk=id_diemdanh)
        att = attendance.objects.filter(id_diemdanh_id=id_diemdanh)
        l = hocphan.objects.get(id = d.id_hocphan_id)
        list_data = []
        try:
            att_out = attendance.objects.filter(id_diemdanh_id=id_diemdanh)
            
            data = {"cocheckout":True,"is_disabled": d.is_disabled,"ten_hocphan":l.ten_hoc_phan,"ngay_diemdanh":d.ngay_diem_danh,"id":d.id}
            
            print(att)
            list_data.append(data)
            for a in att:
                
                s = sinhvien.objects.get(mssv=a.id_sinhvien_id)
                print(a.mssv)
                if s.perm.is_active == True:
                    out =attendance_out.objects.get(id_diemdanh_id = id_diemdanh,id_sinhvien_id = s.mssv)
                    context['id_diemdanh'] = d.id
                    context['mssv'] = s.mssv 
                    context['ho'] = s.perm.first_name
                    context['ten'] = s.perm.last_name
                    context['trangthai_in'] = a.diemdanh
                    context['trangthai_out'] = out.diemdanh
                    context['id_att_in'] = a.id
                    context['id_att_out'] = out.id
                    context['ngay_diem_danh'] = d.ngay_diem_danh
                        
                
                    print(context)
                    list_data.append(context)
        except  : 
            list_data[0]["cocheckout"] = False
            list_data[0]['is_disabled'] = d.is_disabled
            print(list_data)
            for a in att:
                s = sinhvien.objects.get(mssv=a.id_sinhvien_id)
                print(a)
                if s.perm.is_active == True:
                    if d.is_disabled == False:

                        context = {"id_diemdanh": d.id, "mssv": s.mssv, "ho": s.perm.first_name, "ten": s.perm.last_name,
                                "trangthai": a.diemdanh, "id_att": a.id, "ngay_diem_danh": d.ngay_diem_danh, "is_disabled": False}
                    else:
                        context = {"id_diemdanh": d.id, "mssv": s.mssv, "ho": s.perm.first_name, "ten": s.perm.last_name,
                                "trangthai": a.diemdanh, "id_att": a.id, "ngay_diem_danh": d.ngay_diem_danh, "is_disabled": True}

                    list_data.append(context)
        print(list_data)
        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)

    except:
        return HttpResponse("Not ok")

@login_required(login_url='login')
@csrf_exempt
def reAtt(request):
    id_att = request.POST.get("id_att")
    try:
        a = attendance.objects.get(pk=id_att)
        a.diemdanh = True
        a.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
@login_required(login_url='login')
@csrf_exempt
def reAttIn(request):
    id_att_in = request.POST.get("id_att_in")
    try:
        a = attendance.objects.get(pk=id_att_in)
        a.diemdanh=True
        a.save()
        return HttpResponse("OK")
    except :
        return HttpResponse("Error")
@login_required(login_url='login')
@csrf_exempt
def reAttOut(request):
    id_att_out = request.POST.get("id_att_out")
    try:
        a = attendance_out.objects.get(pk=id_att_out)
        a.diemdanh=True
        a.save()
        return HttpResponse("OK")
    except :
        return HttpResponse("Error")
@login_required(login_url='login')
@csrf_exempt
def createAttInOut(request):
    id_hocphan = request.POST.get("id_hocphan")
    ngay_diem_danh = request.POST.get("ngay_diem_danh")
    list_data = []
    print(type(ngay_diem_danh))
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
            attout = attendance_out.objects.create(
                id_sinhvien_id=student.mssv, id_diemdanh_id=currentAtt.id)
            att.save()
            attout.save()
        print(students)
        data = {"id": currentAtt.id, "ngay_diem_danh": currentAtt.ngay_diem_danh,
                "tenlop": currentAtt.id_hocphan.ten_hoc_phan}
        list_data.append(data)
        print(list_data)

        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder), content_type="application/json", safe=False)
    except:
        return HttpResponse("ERR")

@login_required(login_url='login')
@csrf_exempt
def createQRcheckin(request):
    id_diemdanh = request.POST.get("id_diemdanh")
    ngay_diem_danh = request.POST.get("ngay_diem_danh")
    filename = "static/images/qrcodes/checkin/" + \
        id_diemdanh+ngay_diem_danh+"6"+".png"
    url = "/static/images/qrcodes/checkin/"+id_diemdanh+ngay_diem_danh+"6"+".png"

    response_data = {
        'url': url
    }
    try:
        img = qrcode.QRCode(
            version=1,
            box_size=40,
            border=4,
        )
        img = qrcode.make(id_diemdanh+ngay_diem_danh+'6')
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")

@login_required(login_url='login')
@csrf_exempt
def createQRcheckout(request):
    id_diemdanh = request.POST.get("id_diemdanh")
    ngay_diem_danh = request.POST.get("ngay_diem_danh")
    filename = "static/images/qrcodes/checkin/" + \
        id_diemdanh+ngay_diem_danh+"6"+".png"
    url = "/static/images/qrcodes/checkin/"+id_diemdanh+ngay_diem_danh+"6"+".png"

    response_data = {
        'url': url
    }
    try:
        img = qrcode.QRCode(
            version=1,
            box_size=40,
            border=4,
        )
        img = qrcode.make(id_diemdanh+ngay_diem_danh+'6')
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")
