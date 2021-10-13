from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel
from system.models import *
class UserBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def authenticate_student(self, id=None,**kwargs):
        
        try:
            user = sinhvien.objects.get(perm_id=id)
        except  sinhvien.DoesNotExist:
            return None
        else:
            return user
    

    def authenticate_subject(self, id=None,**kwargs):

        try :
            c = lop.objects.get(pk=id)
            
        except  lop.DoesNotExist :
            return None
        else:
            
            return c

        