
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from system import views, adminViews
from system.adminViews import *
from system.giangvienViews import  *
from system.sinhvienViews import *
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path
from system.api import getSubjectAPI, loginAPI,getStudnetIDAPI,getAttAPI,UpdateAttDataAPI,getAttDetailAPI
from knox import views as knox_views


urlpatterns = [
    path('', views.adminLogin),
    path('admin/', admin.site.urls),
    # Giảng viên
    path('adminGiangvien/',views.adminGiangvien),
    path('adminThemgiangvien',views.adminThemgiangvien),
    path('change-teacher',change_teacher_info),
    path('toanbogiangvien', adminViews.toanbogiangvien),
    path('themgiangvien', themGiangvien,name="themgiangvien"),
    path('giangvien/',giangvienViews),
    path('giangvien_Lop',giangvien_Lop ),
    path('thongbao',giangvienNoti ),
    path('addNoti',addNoti),
    path('addNotifications',addNotifications),
    path('noti',noti),
    path('allnoti',allnoti, name='allnoti'),
    path('deleteNoti',deleteNoti,name="deleteNoti"),
    path('deleteTeacher',deleteTeacher,name="deleteTeacher"),
    path('getupdateTeacher',getupdateTeacher,name="getupdateTeacher"),
    path('updateTeacher',updateTeacher,name="updateTeacher"),
    path('toanbosinhvien',toanbosinhvien,name="toanbosinhvien"),
    path('change_student',change_student,name="change_student"),
    path('historyAttData',historyAttData,name="historyAttData"),
    # Lớp
    path('adminLop/', views.adminLop),
    path('adminThemlop', views.adminThemlop),
    path('adminThemhocphan', views.adminThemhocphan),
    path('themlop',themlop ),
    path('themhocphan', themhocphan),

    #Sinh viên
    path('adminSinhvien/',views.adminSinhvien),
    path('adminThemsinhvien', views.adminThemsinhvien),
    path('themsinhvien', themsinhvien),
    path('sinhvien/',sinhvienViews),
    path('student_att',student_att,name="student_att"),
    path('danhsach_diemdanh',danhsach_diemdanh,name="danhsach_diemdanh"),
    path('deleteStudent',deleteStudent,name="deleteStudent"),
    path('getupdateStudent',getupdateStudent,name="getupdateStudent"),
    path('updateStudent',updateStudent,name="updateStudent"),
    path('toanbosinhvien',toanbosinhvien,name="toanbosinhvien"),
    #Điểm danh
    path('giangvien_Diemdanh', giangvien_diemdanh),
    path('danhsach_sinhvien',danhsach_sinhvien, name='danhsach_sinhvien'),
    path('historyAtt', historyAtt, name='historyAtt'),
    path('deleteAtt',deleteAtt,name="deleteAtt"),
    path('createAtt',createAtt,name='createAtt'),
    path('createQR',createQR, name='createQR'),
    
    #path('danhsach', danhsach, name='danhsach'),
    #Đăng nhập
    path('loginAdmin', views.loginAdmin),
    path('logout', views.logOut),
    #api
    path("api/auth", include('knox.urls')),
    path('api/auth/login',loginAPI.as_view()),
    path('api/auth/mssv',getStudnetIDAPI.as_view()),
    path('api/auth/subject',getSubjectAPI.as_view()),
    path('api/auth/att',getAttAPI.as_view()),
    path('api/auth/update/<int:pk>',UpdateAttDataAPI.as_view()),
    path('api/auth/attdetails',getAttDetailAPI.as_view()),


    
]
