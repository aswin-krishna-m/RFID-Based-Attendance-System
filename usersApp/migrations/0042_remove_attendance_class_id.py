# Generated by Django 5.0.7 on 2024-10-13 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0041_remove_attendance_time_and_date_attendance_class_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='class_id',
        ),
    ]
