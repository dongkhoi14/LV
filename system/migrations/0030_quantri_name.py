# Generated by Django 3.2 on 2021-12-08 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0029_alter_staff_event_id_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantri',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
    ]
