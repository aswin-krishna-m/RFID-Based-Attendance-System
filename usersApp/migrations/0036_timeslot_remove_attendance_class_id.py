# Generated by Django 5.0.7 on 2024-10-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0035_attendance_class_id_alter_attendance_time_and_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='class_id',
        ),
    ]
