from system.models import *
from system.serializer import *
from datetime import timedelta
from django.utils import timezone
# ii = staff_event.objects.values('name','time_create','time_start','time_end').distinct()
# print(ii)
# for i in ii:
#     print(i['name'])
# s= staff_event.objects.create(name="Test",time_start = timezone.now(),time_end=timezone.now(),id_diemdanh_id=69,id_department_id=2 )
# s.save()
import qrcode

import hashlib
a = "dsadasdasd"
hash_object = hashlib.md5()
print(hash_object.hexdigest())

