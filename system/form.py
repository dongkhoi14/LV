from django import forms
from .models import lop
class themsinhvien(forms.Form):
    first_name = forms.CharField(label="Họ")
    last_name = forms.CharField(label="Ten")
    username= forms.CharField(label="Username")
    email=forms.EmailField(label="Email")
    password = forms.PasswordInput(label="Mật khẩu")
    lops = lop.objects.all()
    lop_list  = []
    for lop in lops:
        lop_list.append(lop.id, lop.ten_lop)
    
    lop  = forms.ChoiceField(label="Lớp" , choices=lop_list)
