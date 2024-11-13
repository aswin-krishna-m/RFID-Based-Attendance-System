from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from usersApp.models import Student, Attendance, Timetable, SpecialTimetable

class MarkAttendanceAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Get the RFID from the request
            rfid_id = request.data.get('rfid_id')
            if not rfid_id:
                return Response({"error": "RFID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Find the student by RFID
            try:
                student = Student.objects.get(rfid=rfid_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

            # Get current day, date, and time
            current_time = timezone.now().replace(microsecond=0)
            current_time = current_time + timedelta(hours=5, minutes=30)
            print(current_time)
            current_day = current_time.strftime('%A')
            current_time_only = current_time.time()

            # Get the timetable or special timetable based on the current day
            # If today is Saturday, check the SpecialTimetable
            if current_day == 'Saturday':
                timetable_entry = SpecialTimetable.objects.filter(
                    date=current_time.date(),
                    time_slot__start_time__lte=current_time_only,
                    time_slot__end_time__gte=current_time_only
                ).first()
                timetable_type = 'special'
            else:
                timetable_entry = Timetable.objects.filter(
                    day_of_week=current_day,
                    time_slot__start_time__lte=current_time_only,
                    time_slot__end_time__gte=current_time_only
                ).first()
                timetable_type = 'regular'

            # Check if a timetable entry was found for the current time
            if not timetable_entry:
                return Response({"error": "No timetable entry found for the current time."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the subject is assigned in the timetable
            subject = timetable_entry.assigned.sub_id if timetable_entry else None
            if not subject:
                return Response({"error": "No subject assigned in the current time slot."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the student has already been marked for attendance in the current timetable
            attendance, created = Attendance.objects.update_or_create(
                stud_id=student,
                date=current_time.date(),
                defaults={
                    'attendance_status': True,  # Mark as present
                    'time': current_time_only,
                    'sub_id': subject,
                    'sem_no': timetable_entry.assigned.sem,
                    'stt_id': timetable_entry if timetable_type == 'regular' else None,
                    'sptt_id': timetable_entry if timetable_type == 'special' else None
                }
            )

            return Response({"success": "Attendance marked successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MarkAbsentStudentsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Get current day, date, and time
            current_time = timezone.now().replace(microsecond=0)
            current_time = current_time + timedelta(hours=5, minutes=30)
            current_day = current_time.strftime('%A')

            # Check if today is Saturday for SpecialTimetable
            timetable_type = 'special' if current_day == 'Saturday' else 'regular'

            # Get timetable entry based on timetable type
            timetable_entries = SpecialTimetable.objects.filter(date=current_time.date()) if timetable_type == 'special' else Timetable.objects.filter(day_of_week=current_day)

            if not timetable_entries.exists():
                return Response({"error": "No timetable found for today."}, status=status.HTTP_404_NOT_FOUND)

            for timetable_entry in timetable_entries:
                subject = timetable_entry.assigned.sub_id if timetable_entry else None
                if not subject:
                    return Response({"error": "No subject assigned for the current day."}, status=status.HTTP_404_NOT_FOUND)

                # Get all students for the class and semester from timetable
                class_id = timetable_entry.assigned.class_id
                sem_no = timetable_entry.assigned.sem
                students = Student.objects.filter(class_id=class_id)

                # Get students who have already been marked as present
                present_students = Attendance.objects.filter(
                    date=current_time.date(),
                    stt_id=timetable_entry if timetable_type == 'regular' else None,
                    sptt_id=timetable_entry if timetable_type == 'special' else None,
                    sub_id=subject,
                    attendance_status=True
                ).values_list('stud_id', flat=True)

                # Get the students who have not been marked present (i.e., absent students)
                absent_students = students.exclude(id__in=present_students)

                # Mark all absent students
                for student in absent_students:
                    Attendance.objects.update_or_create(
                        stud_id=student,
                        date=current_time.date(),
                        defaults={
                            'attendance_status': False,  # Mark as absent
                            'time': timetable_entry.time_slot.start_time,
                            'sub_id': subject,
                            'sem_no': sem_no,
                            'stt_id': timetable_entry if timetable_type == 'regular' else None,
                            'sptt_id': timetable_entry if timetable_type == 'special' else None
                        }
                    )

            return Response({"success": "Absent students marked successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
