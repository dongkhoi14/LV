# Generated by Django 3.2 on 2021-11-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0027_alter_giangvien_perm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giangvien',
            name='hocvan',
            field=models.CharField(max_length=255),
        ),
    ]
