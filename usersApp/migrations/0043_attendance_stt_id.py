# Generated by Django 5.0.7 on 2024-10-13 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0042_remove_attendance_class_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='stt_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='usersApp.timetable'),
        ),
    ]
