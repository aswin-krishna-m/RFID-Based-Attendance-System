# Generated by Django 5.0.7 on 2024-10-13 03:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0039_timetableclass_class_id_timetableclass_sem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='tt_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersApp.timetableclass'),
        ),
    ]
