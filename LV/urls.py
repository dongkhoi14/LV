
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from system import views, adminViews
from system.adminViews import *
from system.giangvienViews import  *
from system.sinhvienViews import *
from system.enterpriseViews import *
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path
from system.api import *
from system.serializer import *
from knox import views as knox_views


urlpatterns = [
    path('', views.adminLogin),
    path('admin/', admin.site.urls),
    path('adminHomeSchool',adminHomeSchool,name="adminHomeSchool"),
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
    path('noti',noti),
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
    path('reAtt',reAtt,name='reAtt'),
    path('thongke',thongke,name='thongke'),
    path('onload_thongke',onload_thongke,name='onload_thongke'),
    path('details_thongke',details_thongke,name='details_thongke'),
    path('adminDiemdanh',adminDiemdanh,name='adminDiemdanh'),
    path('onload_thongkeadmin',onload_thongkeadmin,name='onload_thongkeadmin'),
    path('createAttInOut',createAttInOut,name='createAttInOut'),
    path('createQRcheckin',createQRcheckin,name='createQRcheckin'),
    path('createQRcheckin',createQRcheckin,name='createQRcheckin'),
    path('createQRcheckout',createQRcheckout,name='createQRcheckout'),
    path('reAttIn',reAttIn,name='reAttIn'),
    path('reAttOut',reAttOut,name='reAttOut'),
    #path('danhsach', danhsach, name='danhsach'),
    #Đăng nhập
    path('loginAdmin', views.loginAdmin),
    path('logout', views.logOut),
    path('change_password',views.change_password),
    path('changePassword',views.changePassword),
    #api
    path("api/auth", include('knox.urls')),
    path('api/auth/login',loginAPI.as_view()),
    path('api/auth/mssv',getStudnetIDAPI.as_view()),
    path('api/auth/subject',getSubjectAPI.as_view()),
    path('api/auth/att',getAttAPI.as_view()),
    path('api/auth/update/<int:pk>',UpdateAttDataAPI.as_view()),
    path('api/auth/attdetails',getAttDetailAPI.as_view()),
    path('api/auth/updatestaffin/<int:pk>',UpdateAttDataStaffInAPI.as_view()),
    path('api/auth/attdetailsstaffin',getAttDetailStaffInAPI.as_view()),
    path('api/auth/updatestaffout/<int:pk>',UpdateAttDataStaffOutAPI.as_view()),
    path('api/auth/attdetailsstaffout',getAttDetailStaffOutAPI.as_view()),
    path('api/auth/attstudent',getAttStudentAPI.as_view()),
    path('api/event/checkin',AttStaffEventAPICheckin.as_view()),
    path('api/att/attsvout',getAttDetailAPIOut.as_view()),
    path('api/att/attsvout/update/<int:pk>',UpdateAttDataOutAPI.as_view()),
    path('api/event/update/in/<int:pk>',UpdateAttEventDataInAPI.as_view()),
    path('api/event/detailin',AttStaffEventDetailInAPI.as_view()),

    path('api/event/checkout',AttStaffEventAPICheckout.as_view()),
    path('api/event/update/out/<int:pk>',UpdateAttEventDataOutAPI.as_view()),
    path('api/event/detailout',AttStaffEventDetailOutAPI.as_view()),


    #Enterprise
    path('adminEnterprise',views.adminEnterprise,name='adminEnterprise'),
    path('adminEnterpriseManager',adminEnterpriseManager,name="adminEnterpriseManager"),
    path('staff',staff,name='staff'),
    path('department',department,name='department'),
    path('getListDepartment',getListDepartment,name="getListDepartment"),
    path('addDepartment',addDepartment,name="addDepartment"),
    path('staffAtt',staffAtt,name='staffAtt'),
    path('createStaffAtt',createStaffAtt,name='createStaffAtt'),
    path('historyStaffAtt',historyStaffAtt,name='historyStaffAtt'),
    path('detailsatt',detailsatt,name='detailsatt'),
    path('addStaff',addStaff,name='addStaff'),
    path('createStaff',createStaff,name='createStaff'),
    path('QRcheckin',QRcheckin,name='QRcheckin'),
    path('QRcheckout',QRcheckout,name='QRcheckout'),
    path('deleteStaff',deleteStaff,name='deleteStaff'),
    path('staffEvent',staffEvent,name='staffEvent'),
    path('staffHistory',staffHistory,name='staffHistory'),
    path('staffEventAtt',staffEventAtt,name="staffEventAtt"),
    path('historystaffattevent',historystaffattevent,name='historystaffattevent'),
    path('deleteEvent',deleteEvent,name='deleteEvent'),
    path('deltailstaffevennt',deltailstaffevennt,name='deltailstaffevennt'),
    path('chart_draw',chart_draw,name='chart_draw'),
    path('chart_staff_att',chart_staff_att,name='chart_staff_att'),
]
