# Generated by Django 5.0.7 on 2024-09-21 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0016_alter_classes_end_year_alter_classes_start_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='isIncharge',
            field=models.BooleanField(default=False),
        ),
    ]
