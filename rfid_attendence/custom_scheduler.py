from celery.schedules import crontab
from celery import Celery
from django.utils import timezone
from usersApp.models import TimeSlot
import datetime

class CustomScheduler:
    def __init__(self):
        self.celery_app = Celery('rfid_attendence')
        self.update_schedule()

    def update_schedule(self):
        # Clear existing schedules
        self.celery_app.conf.beat_schedule = {}

        # Get current date and time
        now = timezone.now()

        # Query all time slots
        time_slots = TimeSlot.objects.all()
        for slot in time_slots:
            # Get the end time of the time slot
            end_time = datetime.datetime.combine(now.date(), slot.end_time)

            # If the end time is in the future, schedule the task
            if end_time > now:
                self.celery_app.conf.beat_schedule[f'mark_absent_students_at_{slot.end_time}'] = {
                    'task': 'attendance.tasks.mark_absent_students',
                    'schedule': end_time,
                }

