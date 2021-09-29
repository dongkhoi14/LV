from system.serializer import ListStudent

from system.models import sinhvien

sinhviens = sinhvien.objects.all()

for s in sinhviens:
    s.data