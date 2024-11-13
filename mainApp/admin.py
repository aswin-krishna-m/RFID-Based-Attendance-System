from django.contrib import admin
from .models import *
from usersApp.models import *

admin.site.register((Admin,Teacher,Student,))
admin.site.register((Department,Courses,Classes,Subjects,Attendance,AssignSub,TimeSlot,Timetable,TimetableClass,SpecialTimetable))
