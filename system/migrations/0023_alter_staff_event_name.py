# Generated by Django 3.2 on 2021-12-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0022_auto_20211130_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_event',
            name='name',
            field=models.CharField(default='', max_length=254, unique=True),
        ),
    ]
