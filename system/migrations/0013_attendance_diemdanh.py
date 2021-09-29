# Generated by Django 3.2.6 on 2021-09-10 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_auto_20210910_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='diemdanh',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_diem_danh', models.DateField()),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('ngay_cap_nhat', models.DateTimeField(auto_now=True)),
                ('id_hocphan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.hocphan')),
            ],
        ),
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('ngay_cap_nhat', models.DateTimeField(auto_now=True)),
                ('diemdanh', models.BooleanField(default=False)),
                ('id_diemdanh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.diemdanh')),
                ('id_sinhvien', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='system.sinhvien')),
            ],
        ),
    ]
