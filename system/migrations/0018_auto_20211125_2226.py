# Generated by Django 3.2 on 2021-11-25 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_remove_staff_event_id_diemdanh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_event',
            name='time_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='staff_event',
            name='time_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='staff_event_checkin',
            name='timecheckin',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='staff_event_checkout',
            name='timecheckout',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
