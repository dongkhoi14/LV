# Generated by Django 3.2.6 on 2021-09-12 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_alter_diemdanh_ngay_diem_danh'),
    ]

    operations = [
        migrations.AddField(
            model_name='diemdanh',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
