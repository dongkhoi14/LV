# Generated by Django 3.2 on 2021-11-11 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20211111_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_att',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='staffdo_att',
            name='diemdanh',
            field=models.BooleanField(default=False),
        ),
    ]