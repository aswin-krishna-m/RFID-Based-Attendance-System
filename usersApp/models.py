from django.db import models
from django.core.exceptions import ValidationError

class Department(models.Model):
    dept_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=150,default=dept_name)
    created_on = models.DateField(default='2001-01-01')
    def __str__(self):
        return self.dept_name
    
class Courses(models.Model):
    department_id = models.ForeignKey(Department,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    course_title = models.CharField(max_length=150)
    short_name = models.CharField(max_length=150,default=course_title)
    sem_count = models.IntegerField(default=1)
    created_on = models.DateField(default='2001-01-01')
    def __str__(self):
        return self.course_title

class Teacher(models.Model):
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    email = models.EmailField( max_length=150,unique=True)
    phone = models.CharField(max_length=15,unique=True,null=True,blank=True)
    dob = models.DateField(default='2001-01-01')
    gender = models.CharField(max_length=20,default=None,null=True,blank=True)
    password = models.CharField(max_length=150)
    department_id = models.ForeignKey(Department,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    stts = models.IntegerField(default=0)
    isIncharge = models.BooleanField(default=False)
    created_on = models.DateField(default='2001-01-01')
    def __str__(self):
        return f"{self.fname} {self.lname}"
    
class Classes(models.Model):
    course_id = models.ForeignKey(Courses,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    start_year = models.IntegerField(default=2010)
    end_year = models.IntegerField(default=2010)
    sem_number = models.IntegerField(default=1)
    class_in_charge = models.ForeignKey(Teacher,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    division_name = models.CharField(default=None, max_length=255, null=True,blank=True)
    created_on = models.DateField(default='2001-01-01')
    passed_out= models.BooleanField(default=False)
    def __str__(self):
        return f"S{self.sem_number} - {self.course_id.short_name} - {self.division_name}"

class Subjects(models.Model):
    course_id = models.ForeignKey(Courses,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    code = models.CharField(max_length=15,default='0000')
    sub_title = models.CharField(max_length=150)
    
    def __str__(self):
        return self.sub_title

class Student(models.Model):
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    course_id = models.ForeignKey(Courses,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    class_id = models.ForeignKey(Classes,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    # roll = models.IntegerField(null=True,blank=True)
    dob = models.DateField(default='2001-01-01')
    gender = models.CharField(max_length=20,default=None,null=True,blank=True)
    email = models.EmailField( max_length=150,unique=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    password = models.CharField(max_length=150)
    stts = models.IntegerField(default=0)
    created_on = models.DateField(default='2001-01-01')
    rfid = models.CharField(max_length=250,blank=True,null=True)
    def __str__(self):
        return f"{self.fname} {self.lname} ({self.course_id})"
    
    
class AssignSub(models.Model):
    class_id = models.ForeignKey(Classes,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    sub_id = models.ForeignKey(Subjects,on_delete=models.SET_DEFAULT,default=None,blank=True,null=True)
    teacher_id = models.ForeignKey(Teacher,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    sem = models.IntegerField(default=1)
    def __str__(self):
        return f"SEM{self.sem}-{self.class_id} {self.sub_id}"
    
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self) -> str:
        return str(self.start_time) + " " + str(self.end_time)

class TimetableClass(models.Model):
    class_id = models.ForeignKey(Classes,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    sem = models.IntegerField(default=1) 
    start = models.DateField(default='2019-10-13')
    end = models.DateField(default='2019-10-13')
    def __str__(self):
        return f"S{self.sem} - {self.class_id.course_id.short_name} - {self.class_id.start_year}- {self.class_id.end_year}"
    
class Timetable(models.Model):
    days_of_week=(('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'))
    day_of_week = models.CharField(max_length=20,choices=days_of_week)
    tt_id = models.ForeignKey(TimetableClass,on_delete=models.CASCADE,default = None,blank=True,null=True)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    assigned = models.ForeignKey(AssignSub, on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)

    def __str__(self):
        return f"{self.day_of_week} - {self.time_slot} - {self.assigned} - {self.tt_id}"
    
class SpecialTimetable(models.Model):
    date = models.DateField(default='2019-10-13')
    tt_id = models.ForeignKey(TimetableClass,on_delete=models.CASCADE,default = None,blank=True,null=True)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)
    assigned = models.ForeignKey(AssignSub, on_delete=models.SET_DEFAULT,default = None,blank=True,null=True)

    def __str__(self):
        return f"{self.date} - {self.time_slot} - {self.assigned} - {self.tt_id}"
    
    
class Attendance(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    stt_id = models.ForeignKey(Timetable, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    sptt_id = models.ForeignKey(SpecialTimetable, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    sub_id = models.ForeignKey(Subjects, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    sem_no = models.IntegerField(default=1)
    attendance_status = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.stud_id} - {self.sub_id} - {self.attendance_status} on {self.date} at {self.time}"
    def clean(self):
        if self.stt_id and self.sptt_id:
            raise ValidationError('Attendance can only be associated with either Timetable or SpecialTimetable, not both.')
        if not self.stt_id and not self.sptt_id:
            raise ValidationError('Attendance must be associated with either Timetable or SpecialTimetable.')