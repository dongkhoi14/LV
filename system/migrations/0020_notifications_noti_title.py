# Generated by Django 3.2 on 2021-10-21 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0019_auto_20211020_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='noti_title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]