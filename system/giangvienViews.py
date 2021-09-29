import json
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import lop, giangvien, hocphan, sinhvien,diemdanh
from rest_framework import viewsets
from system.serializer import ListStudent
from django.http import request
import qrcode
from django.core.serializers.json import DjangoJSONEncoder
class danhsachsinhvien(viewsets.ModelViewSet):
    def get(request):
        pass
    queryset = sinhvien.objects.all()
    serializer_class = ListStudent

def giangvienViews(request):
    giangviens = giangvien.objects.all()
    return render(request, 'templates/giangvien.html',{'giangviens':giangviens})

def giangvien_Lop(request):
    lops= lop.objects.all()
    hocphans = hocphan.objects.filter(id_giangvien = request.user.giangvien.mscb)
    sinhviens = sinhvien.objects.all()
    return render(request,'templates/giangvien_Lop.html',{'lops':lops,'hocphans':hocphans})

def info_lop(request):
    pass

def giangvien_diemdanh(request):
    lops= lop.objects.all()
    hocphans = hocphan.objects.filter(id_giangvien = request.user.giangvien.mscb)
    return render(request,"templates/giangvien_diemdanh.html",{"lops":lops,"hocphans":hocphans})

@csrf_exempt
def danhsach_sinhvien(request):
    id_hocphan = request.POST.get("id_hocphan")
    lops = hocphan.objects.get(id = id_hocphan)
    sinhviens = sinhvien.objects.filter(id_lop = lops.id_lop)
    list_data = []
    for s in sinhviens :
        data = {"id":s.mssv, "name" : s.perm.first_name + " " +s.perm.last_name, "lop":s.id_lop.ten_lop}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def historyAtt(request):
    id_hocphan = request.POST.get("id_hocphan")
    ngay_diem_danhh = request.POST.get("ngay_diem_danh")
    atts = diemdanh.objects.filter(id_hocphan_id=id_hocphan,ngay_diem_danh=ngay_diem_danhh)
    list_data =[]
    
    for data in atts:
        data = {"id":data.id, "ngay_diem_danh":data.ngay_diem_danh,"ten_lop":data.id_hocphan.ten_hoc_phan}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data,cls=DjangoJSONEncoder),content_type="application/json",safe=False) 

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
        c  = diemdanh.objects.create(id_hocphan_id=id_hocphan,ngay_diem_danh=ngay_diem_danh)
        c.save()
        currentAtt = diemdanh.objects.filter(id_hocphan=id_hocphan,ngay_diem_danh=ngay_diem_danh).latest('ngay_tao')
        data = {"id":currentAtt.id,"ngay_diem_danh":currentAtt.ngay_diem_danh}
        list_data.append(data)
        print(list_data)
        return JsonResponse(json.dumps(list_data,cls=DjangoJSONEncoder),content_type="application/json",safe=False)
    except:
        return HttpResponse("ERR")


    


        

        


    
    
