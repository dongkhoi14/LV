from system.models import giangvien, hocphan , lop, sinhvien,quantri
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import request
from .UserBackend import UserBackend
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
import datetime

def adminLogin(request):
    return render(request, 'templates/loginadmin.html')



def adminViews(request):
    return render(request, 'templates/admin.html')
    
@login_required(login_url='loginAdmin')
def adminGiangvien(request):
    sl = giangvien.objects.all().count()
    return render(request, 'templates/adminGiangvien.html',{'sl':sl})


def adminThemgiangvien(request):
    return render(request,'templates/adminThemgiangvien.html')




def adminLop(request):
    sl = lop.objects.all().count()
    return render(request, 'templates/adminLop.html',{'sl':sl})



def adminThemlop(request):
    return render(request,'templates/adminThemlop.html')




def adminThemhocphan(request):
    giangviens = giangvien.objects.all()
    lops = lop.objects.all()
    return render(request,'templates/adminThemhocphan.html',{'giangviens':giangviens, 'lops':lops})

def adminSinhvien(request):
    sl = sinhvien.objects.all().count()
    return render(request, 'templates/adminSinhvien.html', {'sl':sl})
def adminThemsinhvien(request):
    
    lops = lop.objects.all()
    return render(request, 'templates/adminThemsinhvien.html', {'lops':lops})

@csrf_exempt
def loginAdmin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = UserBackend.authenticate(request,username = username, password = password )
    if user is not None :
        login(request,user)
        if user.user_type == '1':
            a= quantri.objects.get(perm = user.id)
            if   a.type == "1":
                return HttpResponseRedirect('/adminGiangvien')
            elif a.type  == "2":
                return HttpResponseRedirect('/adminEnterprise')
        if user.user_type == '2':
            return HttpResponseRedirect('/giangvien')
        if user.user_type == '3':
            return HttpResponseRedirect('/sinhvien')
    else :
        return HttpResponseRedirect('/')

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/')

def adminEnterprise(request):
    staffs = sinhvien.objects.filter(owner = request.user.username).count()
    departments = lop.objects.filter(create_by = request.user.username).count()
    return render(request,"templates/adminEnterprise.html",{"staff":staffs,"departments":departments})