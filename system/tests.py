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

c = staff_event.objects.filter(name="xzczxczx",time_create = datetime.strptime("20211201","%Y%m%d"))

for a in c:
    print(getStaffEvent(a).data)

