# Generated by Django 3.2 on 2021-11-11 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_att',
            name='is_disabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='staffdo_att',
            name='diemdanh',
            field=models.BooleanField(default=True),
        ),
    ]
