# Generated by Django 5.0.7 on 2024-10-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0045_alter_attendance_stt_id_specialtimetable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rfid',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
