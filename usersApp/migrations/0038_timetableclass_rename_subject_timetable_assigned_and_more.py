# Generated by Django 5.0.7 on 2024-10-13 02:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0037_timetable'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimetableClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(default='2019-10-13')),
                ('end', models.DateField(default='2019-10-13')),
            ],
        ),
        migrations.RenameField(
            model_name='timetable',
            old_name='subject',
            new_name='assigned',
        ),
        migrations.AlterField(
            model_name='timetable',
            name='day_of_week',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=20),
        ),
        migrations.AddField(
            model_name='timetable',
            name='tt_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='usersApp.timetableclass'),
        ),
    ]
