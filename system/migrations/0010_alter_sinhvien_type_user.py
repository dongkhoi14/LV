# Generated by Django 3.2 on 2021-11-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_sinhvien_type_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sinhvien',
            name='type_user',
            field=models.IntegerField(default='1'),
        ),
    ]
