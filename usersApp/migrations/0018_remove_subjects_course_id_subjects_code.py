# Generated by Django 5.0.7 on 2024-09-22 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0017_teacher_isincharge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='course_id',
        ),
        migrations.AddField(
            model_name='subjects',
            name='code',
            field=models.CharField(default=0, max_length=15),
        ),
    ]
