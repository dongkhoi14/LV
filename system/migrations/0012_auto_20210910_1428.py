# Generated by Django 3.2.6 on 2021-09-10 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_danhsach'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='id_diemdanh',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='id_sinhvien',
        ),
        migrations.DeleteModel(
            name='danhsach',
        ),
        migrations.RemoveField(
            model_name='diemdanh',
            name='id_hocphan',
        ),
        migrations.AlterModelOptions(
            name='sinhvien',
            options={'ordering': ['id_lop']},
        ),
        migrations.DeleteModel(
            name='attendance',
        ),
        migrations.DeleteModel(
            name='diemdanh',
        ),
    ]
