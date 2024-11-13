# Generated by Django 5.0.7 on 2024-09-10 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0009_remove_student_course_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='course_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='usersApp.courses'),
        ),
    ]
