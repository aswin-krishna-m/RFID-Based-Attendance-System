# attendance/tasks.py

from celery import shared_task
from django.utils import timezone
from usersApp.models import Attendance, Student, Timetable, SpecialTimetable

@shared_task
def mark_absent_students():
    current_time = timezone.now().replace(microsecond=0)
    current_day = current_time.strftime('%A')

    timetable_type = 'special' if current_day == 'Saturday' else 'regular'
    timetable_entries = SpecialTimetable.objects.filter(date=current_time.date()) if timetable_type == 'special' else Timetable.objects.filter(day_of_week=current_day)

    if not timetable_entries.exists():
        return {"error": "No timetable found for today."}

    for timetable_entry in timetable_entries:
        subject = timetable_entry.assigned.sub_id if timetable_entry else None
        if not subject:
            continue  # Skip if no subject assigned

        class_id = timetable_entry.assigned.class_id
        students = Student.objects.filter(class_id=class_id)

        present_students = Attendance.objects.filter(
            date=current_time.date(),
            stt_id=timetable_entry,
            sub_id=subject,
            attendance_status=True
        ).values_list('stud_id', flat=True)

        if not present_students:
            continue  # Skip if no students marked present

        absent_students = students.exclude(id__in=present_students)

        for student in absent_students:
            Attendance.objects.update_or_create(
                stud_id=student,
                date=current_time.date(),
                defaults={
                    'attendance_status': False,  # Mark as absent
                    'time': timetable_entry.time_slot.end_time,
                    'sub_id': subject,
                    'sem_no': timetable_entry.assigned.sem,
                    'stt_id': timetable_entry
                }
            )

    return {"success": "Absent students marked successfully"}
