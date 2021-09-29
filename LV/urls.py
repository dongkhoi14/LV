
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from system import views, adminViews
from system.adminViews import themGiangvien, themhocphan, themlop, themsinhvien
from system.giangvienViews import  *
from system.sinhvienViews import sinhvienViews
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()
router.register('system',danhsachsinhvien )
urlpatterns = [
    path('', views.adminLogin),
    path('admin/', admin.site.urls),
    # Giảng viên
    path('adminGiangvien/',views.adminGiangvien),
    path('adminThemgiangvien',views.adminThemgiangvien),
    path('toanbogiangvien', adminViews.toanbogiangvien),
    path('themgiangvien', themGiangvien),
    path('giangvien/',giangvienViews),
    path('giangvien_Lop',giangvien_Lop ),

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
    #Điểm danh
    path('giangvien_Diemdanh', giangvien_diemdanh),
    path('danhsachsinhvien', include(router.urls)),
    path('danhsach_sinhvien',danhsach_sinhvien, name='danhsach_sinhvien'),
    path('historyAtt', historyAtt, name='historyAtt'),
    path('deleteAtt',deleteAtt,name="deleteAtt"),
    path('createAtt',createAtt,name='createAtt'),

    #path('danhsach', danhsach, name='danhsach'),
    #Đăng nhập
    path('loginAdmin', views.loginAdmin),
    path('logout', views.logOut),

]
