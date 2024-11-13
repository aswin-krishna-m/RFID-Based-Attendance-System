from django.db import models
from datetime import datetime

# Student model
class StudentAPI(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    rfid = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Attendance model
class AttendanceAPI(models.Model):
    student = models.ForeignKey(StudentAPI, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {'Present' if self.present else 'Absent'}"
