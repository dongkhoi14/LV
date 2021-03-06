# Generated by Django 3.2 on 2021-11-24 13:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0013_alter_attendance_id_diemdanh'),
    ]

    operations = [
        migrations.CreateModel(
            name='staff_event',
            fields=[
                ('id_event', models.AutoField(primary_key=True, serialize=False)),
                ('time_create', models.DateField(default=django.utils.timezone.now)),
                ('name', models.CharField(default='', max_length=254)),
                ('time_start', models.DateField()),
                ('time_end', models.DateField()),
                ('id_diemdanh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.staff_att')),
            ],
        ),
        migrations.CreateModel(
            name='staff_event_checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('checkout', models.BooleanField(default=False)),
                ('timecheckin', models.DateField(auto_now_add=True)),
                ('id_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.staff_event')),
            ],
        ),
        migrations.CreateModel(
            name='staff_event_checkin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('checkin', models.BooleanField(default=False)),
                ('timecheckin', models.DateField()),
                ('id_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.staff_event')),
            ],
        ),
    ]
