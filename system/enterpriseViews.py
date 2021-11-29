from django.db.models.signals import post_save
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from system.giangvienViews import giangvienViews
from .models import *
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta,datetime
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
import qrcode
import hashlib
import unidecode
from django.contrib import messages
def adminEnterpriseManager(request):
    
    return render(request,"templates/adminEnterpriseManager.html")
def staff(request):
    staffs = sinhvien.objects.filter(owner = request.user.username)
    return render(request,"templates/staff.html",{'staffs':staffs})
def department(request):
    departments = lop.objects.filter(create_by = request.user.username)
    
    return render(request,"templates/department.html",{"departments":departments})
def staffAtt(request):
    return render(request,"templates/staffAtt.html")
def staffEvent(request):
    departments = lop.objects.filter(create_by = request.user.username)
    return render(request,"templates/staffAttEvent.html",{"departments":departments})
def staffHistory(request):
    return render(request,"templates/staffHistory.html")

@csrf_exempt
def deleteStaff(request):
    staffID = request.POST.get('staffID')
    print(staffID)
    try:
        staffObject = sinhvien.objects.get(pk=staffID)
        staffUser = phanquyen.objects.get(id=staffObject.perm_id)
        print(staffUser)

        staffUser.is_active = False
        staffUser.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
@csrf_exempt
def getListDepartment(request):
    departments = lop.objects.filter(create_by = request.user.username)
    print(departments)
    try:
        list_data= []
        for d in departments:
            
            counts = 0
            for s in sinhvien.objects.filter(id_lop_id=d.id):
                if staff.perm.is_active == True:
                    counts +=1
            data = {"ten_bophan": d.ten_lop,"soluongnhanvien":counts}
            list_data.append(data)
        print(list_data)
        return JsonResponse(json.dumps(list_data),content_type="application/json", safe=False)
    except:
        return HttpResponse("Error")

@csrf_exempt
def addDepartment(request):
    departmentName =request.POST.get("departmentName")
    print(departmentName)
    try:
        a = lop.objects.create(ten_lop = departmentName, create_by = request.user.username)
        a.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
    
@csrf_exempt
def createStaffAtt(request):
    try:
        departments = lop.objects.filter(create_by = request.user.username)
        day = timezone.now().date()
        print(departments)
        
        if  staff_att is not None and staff_att.objects.latest("ngay_tao").ngay_tao.date() < day :
            s = staff_att.objects.create()
            s.save()
            for department in departments:
                
                staffs = sinhvien.objects.filter(id_lop_id = department.id)
                for staff in staffs :
                    a= staffDo_att_in.objects.create(id_diemdanh_id = s.id,id_nhanvien_id= staff.mssv,id_department_id = department.id)
                    b= staffDo_att_out.objects.create(id_diemdanh_id = s.id,id_nhanvien_id= staff.mssv,id_department_id = department.id)
                    a.save()
                    b.save()
                    print("OK")

            return HttpResponse("OK")
        else : 
            return HttpResponse("Day ValueError")
    except:
        return HttpResponse("Error")
    
@csrf_exempt
def historyStaffAtt(request):
    try:

        departments = lop.objects.filter(create_by = request.user.username)
        list_data = []
        print(departments)
        atts = staff_att.objects.all()
        for att in atts:
            for department in departments:
            
                countstaff = sinhvien.objects.filter(id_lop_id=department.id).count()
                count = 0
                staffs = sinhvien.objects.filter(id_lop_id=department.id)
                print(staffs)
                for staff in staffs:
                    try:
                        
                        attin = staffDo_att_in.objects.get(id_diemdanh_id=att.id,id_nhanvien_id=staff.mssv,id_department=department.id)
                    
                        attout = staffDo_att_out.objects.get(id_diemdanh_id=att.id,id_nhanvien_id=staff.mssv,id_department=department.id)
                        if attin.diemdanh == True and attout.diemdanh == True:
                            if attout.ngay_cap_nhat - attin.ngay_cap_nhat > timedelta(hours=8):
                                count += 1
                    
                            

                        attdatas  = staffDo_att_in.objects.filter(id_diemdanh_id=att.id,diemdanh=True).count()
                        data = {"id_diemdanh":att.id,"bophan":department.ten_lop,"id_department":department.id,"soluongnhanvien":countstaff,"ngay_tao":att.ngay_tao.date(),"soluongdiemdanh":count}

                    except:
                        print("Khong co su lieu")
                list_data.append(data)
        
        list_data.reverse()
        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder),content_type= "application/json",safe=False)
    except :
        return HttpResponse("Error")

@csrf_exempt
def detailsatt(request):
    try:
        info = request.POST.get('info')
        id_att = "".join(info.split("_")[:1])
        department = "".join(info.split("_")[1:])
        att = staff_att.objects.get(pk=id_att)
        d = lop.objects.get(id = department)
        staffs = sinhvien.objects.filter(id_lop_id = d.id)
        list_data = []
        for staff in staffs :
            
            attin = staffDo_att_in.objects.get(id_diemdanh_id= id_att,id_nhanvien_id = staff.mssv,id_department_id=d.id)
            attout = staffDo_att_out.objects.get(id_diemdanh_id= id_att,id_nhanvien_id = staff.mssv,id_department_id=d.id)
            
            if  attin.diemdanh==True and attout.diemdanh == True :
                print(str(attout.ngay_cap_nhat -attin.ngay_cap_nhat))

                data = {"hoten":staff.perm.first_name + " " + staff.perm.last_name,"checkin":True,"thoigiancheckin":attin.ngay_cap_nhat.ctime(),"checkout":True,"thoigiancheckout":attout.ngay_cap_nhat.ctime(),"phongban":staff.id_lop.ten_lop,"comat" : True,"thoigianlamviec":str(attout.ngay_cap_nhat -attin.ngay_cap_nhat)}
            else:
                if attin.diemdanh==True and attout.diemdanh == False :
                    data = {"hoten":staff.perm.first_name + " " + staff.perm.last_name,"checkin":True,"thoigiancheckin":attin.ngay_cap_nhat.ctime(),"checkout":False,"thoigiancheckout":"","phongban":staff.id_lop.ten_lop,"comat" : False,"thoigianlamviec":""}
                elif attin.diemdanh == False and attout.diemdanh == False :
                    data = {"hoten":staff.perm.first_name + " " + staff.perm.last_name,"checkin":False,"thoigiancheckin":"","checkout":False,"thoigiancheckout":"","phongban":staff.id_lop.ten_lop,"comat" : False,"thoigianlamviec":""}

            list_data.append(data)
        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder),content_type="application/json",safe=False)
    except :
        return HttpResponse("Error")

@csrf_exempt
def QRcheckin(request):
    day = timezone.now().date()
    a = staff_att.objects.latest('ngay_tao')
    if a.ngay_tao.date() != day:
        return HttpResponse("creaeatterror")
    elif a.ngay_tao.date() == day :
        date_time = a.ngay_tao.date().strftime("%d%m%Y")
        id_diemdanh = a.id
        filename = "static/images/qrcodes/"+str(id_diemdanh)+date_time+"1.png"
        url = "/static/images/qrcodes/"+str(id_diemdanh)+date_time+"1.png"

        response_data = {
            'url': url
        }
    try:
        img = qrcode.QRCode(
            version=1,
            box_size=40,
            border=4,
        )
        img = qrcode.make(str(id_diemdanh)+date_time+"1") # 1 = checkin
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")

@csrf_exempt
def QRcheckout(request):
    day = timezone.now().date()
    a = staff_att.objects.latest('ngay_tao')
    if a.ngay_tao.date() != day:
        return HttpResponse("creaeatterror")
    elif a.ngay_tao.date() == day :
        date_time = a.ngay_tao.date().strftime("%d%m%Y")
        id_diemdanh = a.id
        filename = "static/images/qrcodes/"+str(id_diemdanh)+date_time+"2.png"
        url = "/static/images/qrcodes/"+str(id_diemdanh)+date_time+"2.png"

        response_data = {
            'url': url
        }
    try:
        img = qrcode.QRCode(
            version=1,
            box_size=40,
            border=4,
        )
        img = qrcode.make(str(id_diemdanh)+date_time+"2") # 2 = checkout
        img.save(filename)
        return HttpResponse(json.dumps(response_data))
    except:
        return HttpResponse("deo' OK")

@csrf_exempt
def addStaff(request):
    departments = lop.objects.filter(create_by=request.user.username)
    return render(request,"templates/addStaff.html",{"departments":departments})

def createStaff(request):
    global data_address
    if request.method == "POST":
        username = request.POST.get("username")
        ls_province = request.POST.get("ls_province")
        ls_district = request.POST.get("ls_district")
        ls_ward = request.POST.get("ls_ward")
        
        diachi = str(ls_province) + " " + str(ls_district) + " " + str(ls_ward)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        id_lop = request.POST.get('id')
        sodienthoai = request.POST.get('sodienthoai')
        id_department = request.POST.get('id_department')
        try:
            print("ok")
            user = phanquyen.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password, email=email, user_type=3)
            user.user_type = 4
            a = sinhvien.objects.get(perm = user.id)

            a.id_lop_id = id_department
            a.diachi = diachi
            a.so_dien_thoai = sodienthoai
            a.owner = request.user.username
            a.save()
            user.save()
            return HttpResponseRedirect("adminEnterprise")
        except:
            return HttpResponseRedirect("/")



    
@csrf_exempt
def staffEventAtt(request):
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        checkintime = request.POST.get("checkintime")
        checkouttime = request.POST.get("checkouttime")
        event_name = request.POST.get("event_name")
        checkintime_obj = datetime.strptime(checkintime, '%d/%m/%Y %H:%M')
        checkouttime_obj = datetime.strptime(checkouttime, '%d/%m/%Y %H:%M')
        a = event_name + checkintime
        
        time_create = datetime.strftime(timezone.now(),"%Y%m%d")
        print(datetime.strftime(checkouttime_obj,"%H|%M|%S"))
        data = event_name +"|"+time_create+"|"+datetime.strftime(checkintime_obj,"%H|%M|%S")+"3"
        data2 = event_name +"|"+time_create+"|"+datetime.strftime(checkouttime_obj,"%H|%M|%S")+"4"

        try:
            if department_id == "0":
                ds = lop.objects.filter(create_by=request.user.username)
                for d in ds:
                    a = staff_event.objects.create(name=event_name,time_start = checkintime_obj,time_end=checkouttime_obj,id_department_id = d.id)
                    a.save()
                img = qrcode.QRCode(
                version=1,
                box_size=40,
                border=4,
                )
                img = qrcode.make(data) 
                img.save("static/images/qrcodes/event/"+unidecode.unidecode(event_name) +time_create+datetime.strftime(checkintime_obj,"%H%M%S")+"3"+".png")
                img = qrcode.make(data2) 
                img.save("static/images/qrcodes/event/"+unidecode.unidecode(event_name) +time_create+datetime.strftime(checkouttime_obj,"%H%M%S")+"4"+".png")
            else:
                a = staff_event.objects.create(name=event_name,time_start = checkintime_obj,time_end=checkouttime_obj,id_department_id = department_id)
                a.save()
                img = qrcode.QRCode(
                version=1,
                box_size=40,
                border=4,
                )
                img = qrcode.make(data) 
                img.save("static/images/qrcodes/event/"+unidecode.unidecode(event_name) +time_create+datetime.strftime(checkintime_obj,"%H%M%S")+"3"+".png")
                img = qrcode.make(data2) 
                img.save("static/images/qrcodes/event/"+unidecode.unidecode(event_name) +time_create+datetime.strftime(checkouttime_obj,"%H%M%S")+"4"+".png")
            

            messages.success(request, 'Tạo thành công')
            return HttpResponse("OK")
        except Exception:
            messages.error(request, 'Tạo thất bai')
            return HttpResponse("Eror")

@csrf_exempt
def historystaffattevent(request):
    try:
        ss = staff_event.objects.filter(is_disabled = False)
        for s in ss:
            if timezone.now() >= s.time_end:
                s.is_disabled = True
                s.save()
        list_data=[]
        ii = staff_event.objects.values('name','time_create','time_start','time_end','is_disabled').distinct()
        for i in ii:
            i['time_start'] = datetime.strftime(i['time_start'], '%d/%m/%Y %H:%M')
            i['time_end'] = datetime.strftime(i['time_end'], '%d/%m/%Y %H:%M')
            i['time_create'] = datetime.strftime(i['time_create'], '%d/%m/%Y')
            print(unidecode.unidecode(i['name']))
            list_data.append(i)
        list_data.reverse()
        for i in list_data:
            time_start = datetime.strptime(i['time_start'], '%d/%m/%Y %H:%M')
            time_end = datetime.strptime(i['time_end'], '%d/%m/%Y %H:%M')
            time_create = datetime.strptime(i['time_create'], '%d/%m/%Y')
            i['url_checkin'] = "/static/images/qrcodes/event/"+unidecode.unidecode(i['name'])+datetime.strftime(time_create,"%Y%m%d")+datetime.strftime(time_start,"%H%M%S")+"3.png"
            i['url_checkout'] = "/static/images/qrcodes/event/"+unidecode.unidecode(i['name'])+datetime.strftime(time_create,"%Y%m%d")+datetime.strftime(time_end,"%H%M%S")+"4.png"

            print(i)
        return JsonResponse(json.dumps(list_data, cls=DjangoJSONEncoder),content_type="application/json",safe=False)
    except:
        return HttpResponse("ERROR")

@csrf_exempt
def deleteEvent(request):
    if request.method == "POST":
        name = request.POST.get('name')
    try:
        name = name.split("_")
        time_create = datetime.strptime(name[2],"%d/%m/%Y")
        ss = staff_event.objects.filter(name=name[0],time_create=time_create)
        for s in ss :
            s.delete()
        data = [{"id":name[1]}]
        return JsonResponse(json.dumps(data, cls=DjangoJSONEncoder),content_type="application/json",safe=False)
    except:
        return HttpResponse("ERROR")
    
def deltailstaffevennt(request):
    pass




