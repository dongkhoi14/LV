from django.forms.widgets import PasswordInput
from system.models import giangvien, hocphan , lop, phanquyen, sinhvien,quantri
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout,password_validation
from django.http import request
from .UserBackend import UserBackend
from django.contrib.auth.decorators import login_required
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError

def adminLogin(request):
    return render(request, 'templates/loginadmin.html')


@login_required(login_url='login')
def adminViews(request):
    return render(request, 'templates/admin.html')
    
@login_required(login_url='login')
def adminGiangvien(request):
    sl = giangvien.objects.all().count()
    return render(request, 'templates/adminGiangvien.html',{'sl':sl})

@login_required(login_url='login')
def adminThemgiangvien(request):
    return render(request,'templates/adminThemgiangvien.html')



@login_required(login_url='login')
def adminLop(request):
    sl = lop.objects.filter(create_by=request.user.username).count()
    return render(request, 'templates/adminLop.html',{'sl':sl})


@login_required(login_url='login')
def adminThemlop(request):
    return render(request,'templates/adminThemlop.html')



@login_required(login_url='login')
def adminThemhocphan(request):
    giangviens = giangvien.objects.all()
    lops = lop.objects.filter(create_by=request.user.username)
    return render(request,'templates/adminThemhocphan.html',{'giangviens':giangviens, 'lops':lops})
@login_required(login_url='login')
def adminSinhvien(request):
    sl = sinhvien.objects.filter(owner = request.user.username).count()
    return render(request, 'templates/adminSinhvien.html', {'sl':sl})
@login_required(login_url='login')
def adminThemsinhvien(request):
    
    lops = lop.objects.filter(create_by=request.user.username)
    return render(request, 'templates/adminThemsinhvien.html', {'lops':lops})
def change_password(request):
    return render(request,"templates/change_password.html")
@csrf_exempt
def changePassword(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    print(password)
    user = UserBackend.authenticate(request,username = username, password = password )
    print(user)
    if user is not None and password1==password2:
        print(user.password)
        print(password1)
        user.set_password(password1)
        print(user.password)

        user.save()
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
    else:
        messages.error(request,"Kh??ng th??nh c??ng")
        return HttpResponseRedirect("/change_password")
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
            return HttpResponseRedirect('/thongke')
        if user.user_type == '3':
            return HttpResponseRedirect('/sinhvien')
    else :
        messages.error(request,"Sai t??i kho???n ho??c m???t kh???u")
        return HttpResponseRedirect('/')

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/')
@login_required(login_url='login')
def adminEnterprise(request):
    staffs = sinhvien.objects.filter(owner = request.user.username)
    coutstaff = 0
    for staff in staffs:
        if staff.perm.is_active == True:
            coutstaff += 1
    departments = lop.objects.filter(create_by = request.user.username).count()
    return render(request,"templates/adminEnterprise.html",{"coutstaff":coutstaff,"departments":departments})


#Dang ki
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UsernameField


    

class registerForm(forms.ModelForm):
    CHOICES = [('1', 'Tr?????ng h???c'), ('2', 'Doanh nghi???p')]
    name = forms.CharField(max_length=254,label="T??n t??? ch???c",widget=forms.TextInput(attrs={'class':'form-control'}))
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label="????n v???")
    password1 = forms.CharField(label="M???t kh???u",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
    password2 = forms.CharField(label="Nh???p l???i m???t kh???u",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
    
    class Meta:
        model = phanquyen
        fields = ('username',)
        field_classes = {'username': UsernameField}
        widgets={
            'username' : forms.TextInput(attrs={'class':'form-control'})
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password2:
            raise forms.ValidationError("B???n c???n x??c nh???n m???t kh???u!")
        if not password1:
            raise forms.ValidationError("B???n c???n nh??p m???t kh???u")
        if password1 != password2:
            raise forms.ValidationError("M???t kh???u kh??ng ch??nh x??c")
        return password2
    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        print(username)
        try:
            c = phanquyen.objects.get(username=username)
            raise forms.ValidationError("Vui l??ng ch???n l???i username")

        except phanquyen.DoesNotExist:
            return username

    def save(self, commit=True):
        print(self.errors)
        try:
            user = phanquyen.objects.create_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'])
            return user
        except:
            raise forms.ValidationError("T???o th???t b???i")

        
def signup_view(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            print("ok")

            user = form.save()
            user.quantri.name  = form.cleaned_data.get('name')
            user.quantri.type  = form.cleaned_data.get('type')
            user.save()
            return redirect('/loginAdmin')
        
    
    formObjects = registerForm()
    print(form.errors)
    f ={'form': form}
    return render(request, 'templates/register.html',context = f )
