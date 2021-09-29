from django.contrib import admin
from .models import phanquyen

from django.contrib.auth.admin import UserAdmin

class usermodel(UserAdmin):
    pass

admin.site.register(phanquyen,usermodel)


