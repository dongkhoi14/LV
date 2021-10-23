# Generated by Django 3.2 on 2021-10-20 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_alter_hocphan_id_lop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diemdanh',
            name='id_hocphan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='att', to='system.hocphan'),
        ),
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('noti_content', models.TextField()),
                ('id_giangvien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.giangvien')),
                ('id_lop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.lop')),
            ],
        ),
    ]
