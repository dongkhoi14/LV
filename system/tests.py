from system.models import *
from system.serializer import *
from datetime import timedelta,datetime
from django.utils import timezone
# ii = staff_event.objects.values('name','time_create','time_start','time_end').distinct()
# print(ii)
# for i in ii:
#     print(i['name'])
# s= staff_event.objects.create(name="Test",time_start = timezone.now(),time_end=timezone.now(),id_diemdanh_id=69,id_department_id=2 )
# s.save()
# ss = staff_event_checkout.objects.all()
# for s in ss:
#     s.checkout=True
#     s.save()
# ss = staff_event_checkin.objects.all()
# # for s in ss:
# #     s.checkout=True
# #     s.save()

# data = [{"1":2},{"ok":{"a":1,"b":2,"c":3}}]
# print(data[1]['ok']['a'])

# class a():
#     def b(self):
#         print("ok")
# c = a()
# c.b
# c = phanquyen.objects.get(pk=79)
# c.set_password("123")
# c.save()
c= phanquyen.objects.get(pk=15)
print(c)
c.delete()
