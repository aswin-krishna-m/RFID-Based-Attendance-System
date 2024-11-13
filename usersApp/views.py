from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from mainApp.views import currentDate,index
from django.db.models import F
from datetime import datetime
from django.utils.dateparse import parse_date
from django.db.models import Count, Q, Sum
from django.http import JsonResponse



logout_msg = "You have to be logged in first!"



# Student Function Views 

def studentLogin(request):
    if request.method=="POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = Student.objects.get(email=email)
            if user.password == password:
                if user.stts == 1:
                    request.session['student'] = user.id
                    messages.success(request,'Login Success!')
                    return redirect(studentHome)
                else:
                    messages.error(request,'Wait until teacher verifies your login')
                    return redirect(studentLogin)
            else:
                messages.error(request,'Incorrect Password!')
                return redirect(studentLogin)
        except:
            messages.error(request,'Incorrect email!')
            return redirect(studentLogin)
    elif 'student' in request.session:
        return redirect(studentHome)
    else:
        return render(request,'student/login.html')


def studentGetClass(request, course_id):
    classes = Classes.objects.filter(course_id=course_id,passed_out=False).values('id', 'sem_number', 'division_name', 'course_id__short_name')
    class_list = list(classes)
    return JsonResponse(class_list, safe=False)
    
def studentRegister(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        course_id = Courses.objects.get(id=request.POST['course'])
        class_id = Classes.objects.get(id=request.POST['class'])
        email = request.POST['email'].lower()
        phone = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        created_on = currentDate()
        email_exists = Student.objects.filter(email=email)
        phone_exists = Student.objects.filter(phone=phone)
        if email_exists:
            messages.error(request,"Email already exists")
        elif phone_exists:
            messages.error(request,"Phone already exists")
        elif password!=cpassword:
            messages.error(request,"Passwords do not match!")
        else:
            query = Student.objects.create(fname=fname,lname=lname,course_id=course_id,email=email,gender=gender,dob=dob,phone=phone,password=password,created_on=created_on,class_id=class_id)
            query.save()
            messages.success(request,f"Student registration successful")
            return redirect(index)
    course_list = Courses.objects.all()
    class_list = Classes.objects.all()
    return render(request,'student/register.html',{'dept_list':'dept_list','course_list':course_list,'class_list':class_list})

def studentHome(request):
    if 'student' in request.session:
        student_info = Student.objects.get(id=request.session['student'])
        return render(request,'student/index.html',{'student_info':student_info})
    else:
        messages.error(request,logout_msg)
        return redirect(index)


def studentProfile(request):
    if 'student' in request.session:
        student_info = Student.objects.get(id=request.session['student'])
        if request.method=="POST":
            student_info = Student.objects.get(id=request.session['student'])
            email = request.POST['email'].lower()
            phone = request.POST['phone']
            email_exists = Student.objects.filter(email=email)
            phone_exists = Student.objects.filter(phone=phone)
            if email_exists.count()>1:
                messages.error(request,"Email already exists")
            elif phone_exists.count()>1:
                messages.error(request,"Phone already exists")
            else:
                student_info.email =email
                student_info.phone = phone
                student_info.save()
                messages.success(request,"Profile Updated Successfully")
            return redirect(studentProfile)
        else:
            return render(request,'student/profile.html',{'student_info':student_info})
    else:
        messages.error(request,logout_msg)
        return redirect(index)

def studentPassword(request):
    if 'student' in request.session:
        student_info = Student.objects.get(id=request.session['student'])
        if request.method=="POST":
            cpass = request.POST['cpass']
            npass = request.POST['npass']
            cpsw = request.POST['cpsw']
            if cpass != student_info.password:
                messages.error(request,"Current Password is wrong!")
            elif cpsw!= npass:
                messages.error(request,"Passwords do not match!")
            else:
                student_info.password =npass
                student_info.save()
                messages.success(request,"Password Updated Successfully!")
            return redirect(studentProfile)
        return redirect(studentProfile)
    else:
        messages.error(request,logout_msg)
        return redirect(index)


def studentLogout(request):
    if 'student' in request.session:
        del request.session['student']
        messages.success(request,'Logged out successfully')
        return redirect(index)
    else:
        messages.error(request,logout_msg)
        return redirect(index)

def studentAttendance(request):
    if 'student' in request.session:
        # Get the logged-in student from the session
        student = get_object_or_404(Student, id=request.session['student'])

        # Get the range of semesters based on the student's course
        semesters = range(1, student.class_id.course_id.sem_count + 1)

        attendance_list = []
        if request.method == 'POST':
            sem = int(request.POST.get('sem'))

            # Get all subjects for the student's class and the selected semester
            assigned_subjects = AssignSub.objects.filter(
                class_id=student.class_id,
                sem=sem
            ).select_related('sub_id')

            # Loop through all assigned subjects and check attendance
            for assigned in assigned_subjects:
                subject = assigned.sub_id
                attendance_records = Attendance.objects.filter(
                    stud_id=student,
                    sub_id=subject,
                    sem_no=sem
                )

                if attendance_records.exists():
                    # Calculate attendance percentage
                    total_classes = attendance_records.count()
                    attended_classes = attendance_records.filter(attendance_status=True).count()
                    attendance_percentage = (attended_classes / total_classes) * 100  if total_classes > 0 else 0
                else:
                    # No attendance recorded for this subject
                    attendance_percentage = 0

                # Add to the list to pass to the template
                attendance_list.append({
                    'subject': subject.sub_title,
                    'attendance_percentage': attendance_percentage,
                })

        context = {
            'student': student,
            'attendance_list': attendance_list,
            'sem_count': semesters,
        }
        return render(request, 'student/sub-attendance.html', context)
    else:
        messages.error(request, 'You need to log in to view attendance.')
        return redirect('index')





# Teacher Function Views


def teacherLogin(request):
    if request.method=="POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = Teacher.objects.get(email=email)
            if user.password == password:
                if user.stts == 1:
                    request.session['teacher'] = user.id
                    messages.success(request,'Login Success!')
                    return redirect(teacherHome)
                else:
                    messages.error(request,'Wait until admin verifies your login')
                    return redirect(teacherLogin)
            else:
                messages.error(request,'Incorrect Password!')
                return redirect(teacherLogin)
        except:
            messages.error(request,'Incorrect email!')
            return redirect(teacherLogin)
    elif 'teacher' in request.session:
        return redirect(teacherHome)
    else:
        return render(request,'teacher/login.html')


def teacherRegister(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dept_id = Department.objects.get(id=request.POST['dept'])
        email = request.POST['email'].lower()
        phone = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        created_on = currentDate()
        email_exists = Teacher.objects.filter(email=email)
        phone_exists = Teacher.objects.filter(phone=phone)
        if email_exists:
            messages.error(request,"Email already exists")
        elif phone_exists:
            messages.error(request,"Phone already exists")
        elif password!=cpassword:
            messages.error(request,"Passwords do not match!")
        else:
            query = Teacher.objects.create(fname=fname,lname=lname,department_id=dept_id,email=email,phone=phone,dob=dob,gender=gender,password=password,created_on=created_on)
            query.save()
            messages.success(request,f"Teacher registration successful")
            return redirect(index)
    dept_list = Department.objects.all()
    return render(request,'teacher/register.html',{'dept_list':dept_list})

def teacherHome(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        return render(request,'teacher/index.html',{'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect(index)
    
def teacherProfile(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        if request.method=="POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email'].lower()
            phone = request.POST['phone']
            email_exists = Teacher.objects.filter(email=email)
            phone_exists = Teacher.objects.filter(phone=phone)
            if email_exists.count()>1:
                messages.error(request,"Email already exists")
            elif phone_exists.count()>1:
                messages.error(request,"Phone already exists")
            else:
                teacher_info.fname =fname
                teacher_info.lname =lname
                teacher_info.email =email
                teacher_info.phone = phone
                teacher_info.save()
                messages.success(request,"Profile Updated Successfully")
            return redirect(teacherProfile)
        else:
            return render(request,'teacher/profile.html',{'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect(index)

def teacherPassword(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        if request.method=="POST":
            cpass = request.POST['cpass']
            npass = request.POST['npass']
            cpsw = request.POST['cpsw']
            if cpass != teacher_info.password:
                messages.error(request,"Current Password is wrong!")
            elif cpsw!= npass:
                messages.error(request,"Passwords do not match!")
            else:
                teacher_info.password =npass
                teacher_info.save()
                messages.success(request,"Password Updated Successfully!")
            return redirect(teacherProfile)
        return redirect(teacherProfile)
    else:
        messages.error(request,logout_msg)
        return redirect(index)
    
def teacherLogout(request):
    if 'teacher' in request.session:
        del request.session['teacher']
        messages.success(request,'Logged out successfully')
        return redirect(index)
    else:
        messages.error(request,logout_msg)
        return redirect(index)
    
    
def teacherSubList(request,tid):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        sub_list = AssignSub.objects.filter(teacher_id=tid,class_id__passed_out=False).order_by('class_id')
        return render(request,'teacher/list-sub.html',{'sub_list':sub_list,'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherClassList(request,tid):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        class_list = AssignSub.objects.filter(teacher_id=tid,class_id__passed_out=False).distinct()
        distinct_class_ids = AssignSub.objects.filter(
        teacher_id=tid, 
        class_id__passed_out=False).values_list('class_id', flat=True).distinct()
        # Now retrieve the full Classes objects
        class_list = Classes.objects.filter(id__in=distinct_class_ids)
        
        return render(request,'teacher/list-class.html',{'class_list':class_list,'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherClassStudentList(request,id):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        student_list = Student.objects.filter(class_id=id).order_by('fname')
        return render(request,'teacher/list-class-student.html',{'student_list':student_list,'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherMyClass(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        class_info = Classes.objects.get(class_in_charge=teacher_info)
        count = Student.objects.filter(stts=0,class_id=class_info).count()
        return render(request,'teacher/my-class.html',{'count':count,'teacher_info':teacher_info,'class_info':class_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherMyClassStudentList(request,id):
    if 'teacher' in request.session:
        if request.method=="POST":
            sid = request.POST['id']
            del_obj = Student.objects.get(id=sid)
            del_obj.delete()
            messages.success(request,"Student removed!")
            return redirect('teacherMyClassStudentList',id=id)
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        student_list = Student.objects.filter(class_id=id).order_by('fname')
        return render(request,'teacher/my-students.html',{'student_list':student_list,'teacher_info':teacher_info,})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherMyClassStudentReqList(request,id):
    if 'teacher' in request.session:
        if request.method == "POST":
            student_ids = request.POST.getlist('student_ids')
            action = request.POST.get('action')
            if action== 'deleteOne':
                deleteOne = request.POST.get('deleteId')
                del_obj = Student.objects.get(id=deleteOne)
                del_obj.delete()
                messages.success(request,"Student removed!")
            elif student_ids:
                students = Student.objects.filter(id__in=student_ids)

                if action == 'verify':
                    students.update(stts=1) 
                    messages.success(request, 'Selected students have been verified successfully.')

                elif action == 'delete':
                    student_names = [f"{student.fname} {student.lname}" for student in students]  # Get student names for message
                    students.delete()
                    messages.success(request, f'Students {", ".join(student_names)} have been deleted successfully.')

            else:
                messages.error(request, 'No students selected.')
                return redirect('teacherMyClass')

        # Get all students with pending status
        student_list = Student.objects.filter(stts=0,class_id=id).order_by('fname')
        return render(request, 'teacher/my-student-req.html', {'student_list': student_list})

    else:
        messages.error(request, 'You must be logged in as admin to access this page.')
        return redirect('index')
    
def teacherStudentInfo(request,id):
    if 'teacher' in request.session:
        student_info = Student.objects.get(id=id)
        
        if request.method=="POST":
            action = request.POST['action']
            print(action)
            if action == 'update_rfid':
                rfid=request.POST['rfid']
                if Student.objects.filter(rfid=rfid).exists() and rfid != student_info.rfid:
                    messages.error(request,"This rfid is already added")
                    return redirect('teacherStudentInfo',id=id)
                else:
                    student_info.rfid = rfid
            else:
                student_info.fname = request.POST['fname']
                student_info.lname = request.POST['lname']
                student_info.gender = request.POST['gender']
                student_info.roll = request.POST['roll']
                student_info.dob = request.POST['dob']
                student_info.email = request.POST['email']
                student_info.phone = request.POST['phone']
                student_info.password = request.POST['password']
                student_info.stts = request.POST['stts']
            student_info.save()
            messages.success(request,"Student Profile Updated successfully")
            return redirect('teacherStudentInfo',id=id)
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        return render(request,'teacher/view-student.html',{'teacher_info':teacher_info,'student':student_info,})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherMySubList(request,cid):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        if request.method=="POST":
            course_id = Courses.objects.get(id=cid)
            title = request.POST['title'].upper()
            code = request.POST['code'].upper()
            subject_exists = Subjects.objects.filter(course_id=course_id,code=code).exists()        
            if subject_exists:
                messages.error(request,"This subject is already added")
                return redirect('teacherMySubList',cid=cid)
            else:
                query = Subjects.objects.create(course_id=course_id,code=code,sub_title=title)
                query.save()
                messages.success(request,f"Subject Added Successfully")
                return redirect('teacherMySubList',cid=cid)
        sub_list = Subjects.objects.filter(course_id=cid).order_by('sub_title')
        return render(request,'teacher/my-subs.html',{'cid':cid,'teacher_info':teacher_info,'sub_list':sub_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherSubInfo(request, cid,sid):
    if 'teacher' in request.session:
        sub_info = Subjects.objects.get(id=sid)
        if request.method == "POST":
            sub_info.code = request.POST['code'].upper()
            sub = request.POST['title'].upper()
            sub_exists = Subjects.objects.filter(course_id=sub_info.course_id,code=sub_info.code,sub_title=sub).exists()
            if sub_exists and sub != sub_info.sub_title:
                messages.error(request, "This subject is already Added")
                return redirect('teacherSubInfo', cid=cid, sid=sid)
            else:
                sub_info.sub_title = sub          
            sub_info.save()
            messages.success(request, "Class info updated successfully")
            return redirect('teacherSubInfo', cid=cid, sid=sid)
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        teacher_list = Teacher.objects.filter(stts=1).order_by('fname')
        class_list = Classes.objects.filter(course_id = sub_info.course_id).order_by('sem_number')
        course_list = Courses.objects.get(id=cid)
        try:
            assigned = AssignSub.objects.get(sub_id = sub_info)
        except AssignSub.DoesNotExist:
            assigned = None
        return render(request, 'teacher/view-sub.html', {'teacher_list': teacher_list,'teacher_info':teacher_info, 'class_list': class_list, 'course_list': course_list,'assigned': assigned,'cid': id, 'sub': sub_info})
    else:
        messages.error(request, logout_msg)
        return redirect('index')

def teacherSetUpSem(request,class_id):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        sem_count = range(1,Classes.objects.get(id=class_id).course_id.sem_count+1)
        return render(request,'teacher/my-sem.html',{'class_id':class_id,'teacher_info':teacher_info,'sem_count':sem_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherAssignSub(request,class_id,sem_no):
    if 'teacher' in request.session:
        if request.method=="POST":
            sub_obj = Subjects.objects.get(id=request.POST['sid'])
            teacher_obj = Teacher.objects.get(id=request.POST['tid'])
            class_obj = Classes.objects.get(id=class_id)
            sem = sem_no
            sub_exists = AssignSub.objects.filter(class_id=class_obj,sub_id=sub_obj,teacher_id=teacher_obj,sem=sem).exists()
            if sub_exists:
                messages.error(request, "This data is already Added to this class")
                return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
            else:
                messages.error(request, "Subject added to class")
                query = AssignSub.objects.create(class_id=class_obj,sub_id=sub_obj,teacher_id=teacher_obj,sem=sem)
                query.save()
        class_obj = Classes.objects.get(id=class_id)
        try:
            tt_obj = TimetableClass.objects.get(class_id=class_obj,sem=sem_no)
            tt_exists = Timetable.objects.filter(tt_id=tt_obj).exists()
        except TimetableClass.DoesNotExist:
            tt_exists = False
            tt_obj =None
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        assigned_list = AssignSub.objects.filter(class_id=class_id,sem=sem_no)
        teacher_list = Teacher.objects.filter(stts=1).order_by('fname')
        sub_list =  Subjects.objects.filter(course_id=(Classes.objects.get(id=class_id).course_id.id))
        return render(request,'teacher/my-class-assign.html',{'class_id':class_id, 'sem_no':sem_no,'teacher_list':teacher_list,'sub_list':sub_list,'assigned_list':assigned_list,'teacher_info':teacher_info,'tt_set':tt_obj,'tt_exists':tt_exists})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherEditAssignSub(request,class_id,sem_no,aid):
    if 'teacher' in request.session:
        sub_obj = Subjects.objects.get(id=request.POST['sid'])
        teacher_obj = Teacher.objects.get(id=request.POST['tid'])
        sub_exists = AssignSub.objects.filter(class_id=class_id,sub_id=sub_obj,teacher_id=teacher_obj,sem=sem_no).exists()
        if sub_exists:
            messages.error(request, "This data is already Added to this class")
            return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
        else:
            as_obj = AssignSub.objects.get(id=aid)
            as_obj.sub_id = sub_obj
            as_obj.teacher_id = teacher_obj
            as_obj.save()
        messages.error(request, "Data Updated")
        return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherDelAssigned(request,id):
    del_obj = AssignSub.objects.get(id=id)
    clss = del_obj.class_id.id
    sem = del_obj.sem
    del_obj.delete()
    messages.success(request,"Removed assigned subject!")
    return redirect('teacherAssignSub',class_id=clss,sem_no=sem)

    
def teacherSubDel(request,cid,sid):
    if 'teacher' in request.session:
        del_obj = Subjects.objects.get(id=sid)
        del_obj.delete()
        messages.success(request,"Subject removed!")
        return redirect('teacherMySubList',cid=cid)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teachersetTimetable(request,class_id,sem_no):
    if 'teacher' in request.session:
        start = request.POST['start']
        end = request.POST['end']
        tt_exists = TimetableClass.objects.filter(class_id=class_id,sem=sem_no).exists()
        if tt_exists:
            messages.error(request, "This data is already Added to this class")
            return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
        else:
            class_obj = Classes.objects.get(id=class_id)
            query = TimetableClass.objects.create(class_id=class_obj,sem = sem_no,start=start,end=end)
            query.save()
            messages.success(request, "Time table dates set succesfully")
            return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherTimetableGen(request,class_id,sem_no):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        time_slots = TimeSlot.objects.all()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        assigned_list = AssignSub.objects.filter(class_id__passed_out=False,class_id=class_id,sem=sem_no)
        if request.method == 'POST':
            tt_class = TimetableClass.objects.get(class_id=class_id,sem=sem_no)  # Assuming class is passed
            for time_slot in time_slots:
                for day in days_of_week:
                    subject_key = f'{day}_{time_slot.id}_subject'
                    selected_assigned_id = request.POST.get(subject_key)
                    if selected_assigned_id:
                        assigned = AssignSub.objects.get(pk=selected_assigned_id)
                        # Save the timetable entry
                        Timetable.objects.create(
                            day_of_week=day,
                            tt_id=tt_class,
                            time_slot=time_slot,
                            assigned=assigned
                        )
            messages.success(request,'Timetable added succesfully')
            return redirect('teacherAssignSub', class_id=class_id,sem_no= sem_no)
        context = {
            'time_slots': time_slots,
            'days_of_week': days_of_week,
            'assigned_list': assigned_list,
            'teacher_info':teacher_info ,
        }
        
        return render(request, 'teacher/my-class-timetable.html', context)
    else:
        messages.error(request,logout_msg)
        return redirect('index')


def teacherTimetableViewEdit(request,class_id,sem_no):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        time_slots = TimeSlot.objects.all()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        assigned_list = AssignSub.objects.filter(class_id__passed_out=False,class_id=class_id,sem=sem_no)
        tt_class = TimetableClass.objects.get(class_id=class_id,sem=sem_no)  # Assuming class is passed
        tt_periods = Timetable.objects.filter(tt_id=tt_class) 
        if request.method == 'POST':
            action = request.POST.get('action')
            if action=='datedit':
                tt_class.start = request.POST.get('start')
                tt_class.end = request.POST.get('end')
                tt_class.save()
                messages.success(request,'Dates edited succesfully')
                
            elif action == 'ttedit':
                for time_slot in time_slots:
                    for day in days_of_week:
                        subject_key = f'{day}_{time_slot.id}_subject'
                        selected_assigned_id = request.POST.get(subject_key)
                        if selected_assigned_id:
                            assigned = AssignSub.objects.get(pk=selected_assigned_id)

                            try:
                                # Fetch the existing timetable entry
                                timetable_entry = Timetable.objects.get(
                                    day_of_week=day,
                                    time_slot=time_slot,
                                    tt_id=tt_class
                                )

                                # Update the existing entry
                                timetable_entry.assigned = assigned
                                timetable_entry.save()
                            except Timetable.DoesNotExist:
                                # Optionally, you can handle the case where no entry exists
                                # For example, log a message or raise an error
                                messages.error(request, f"No timetable entry exists for {day} - {time_slot}.")
                messages.success(request,'Timetable edited succesfully')
            return redirect('teacherTimetableViewEdit', class_id=class_id,sem_no= sem_no)
        context = {
            'time_slots': time_slots,
            'days_of_week': days_of_week,
            'assigned_list': assigned_list,
            'teacher_info':teacher_info ,
            "sem_no":sem_no,
            'tt_class':tt_class,
            'tt_periods':tt_periods,
        }
        
        return render(request, 'teacher/my-class-timetable-view.html', context)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherSpTimetableCreate(request, class_id, sem_no):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        time_slots = TimeSlot.objects.all()
        assigned_list = AssignSub.objects.filter(class_id__passed_out=False, class_id=class_id, sem=sem_no)
        tt_class = TimetableClass.objects.get(class_id=class_id, sem=sem_no)

        if request.method == 'POST':
            date = request.POST.get('date')
            selected_date = parse_date(date)

            if selected_date.weekday() != 5:  # Ensure selected date is Saturday
                messages.error(request, 'The selected date must be a Saturday.')
                return redirect('teacherSpTimetableCreate', class_id=class_id, sem_no=sem_no)

            # Check if a timetable already exists for the selected date
            existing_timetable = SpecialTimetable.objects.filter(tt_id=tt_class, date=selected_date).exists()
            if existing_timetable:
                messages.error(request, 'A timetable for this date already exists.')
                return redirect('teacherSpTimetableCreate', class_id=class_id, sem_no=sem_no)

            # Proceed to save new timetable entries
            for time_slot in time_slots:
                subject_key = f'{time_slot.id}_subject'
                selected_assigned_id = request.POST.get(subject_key)
                if selected_assigned_id:
                    assigned = AssignSub.objects.get(pk=selected_assigned_id)
                    SpecialTimetable.objects.create(
                        date=selected_date,
                        tt_id=tt_class,
                        time_slot=time_slot,
                        assigned=assigned
                    )

            messages.success(request, 'Special timetable added successfully.')
            return redirect('teacherSpTimetableCreate', class_id=class_id, sem_no=sem_no)

        # Fetch all timetables and get unique dates manually
        all_tt = SpecialTimetable.objects.filter(tt_id=tt_class).order_by('date')
        unique_dates = []
        seen_dates = set()
        
        for tt in all_tt:
            if tt.date not in seen_dates:
                unique_dates.append(tt)
                seen_dates.add(tt.date)

        context = {
            'time_slots': time_slots,
            'assigned_list': assigned_list,
            'teacher_info': teacher_info,
            'tt_class':tt_class,
            'tt_list': unique_dates  # Only unique dates
        }
        return render(request, 'teacher/my-class-sp-timetable.html', context)
    else:
        messages.error(request, 'You need to be logged in as a teacher to access this page.')
        return redirect('index')


def teacherSpTimetableView(request,class_id,sem_no,date):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        time_slots = TimeSlot.objects.all()
        assigned_list = AssignSub.objects.filter(class_id__passed_out=False,class_id=class_id,sem=sem_no)
        tt_class = TimetableClass.objects.get(class_id=class_id,sem=sem_no)  # Assuming class is passed
        tt_periods = SpecialTimetable.objects.filter(tt_id=tt_class,date=date)    
        context = {
            'time_slots': time_slots,
            'assigned_list': assigned_list,
            'teacher_info':teacher_info ,
            "sem_no":sem_no,
            'tt_class':tt_class,
            'tt_periods':tt_periods,
            'date': datetime.strptime(date, '%Y-%m-%d'),
        }
        
        return render(request, 'teacher/my-class-sp-timetable-view.html', context)
    else:
        messages.error(request,logout_msg)
        return redirect('index')

    
def teacherSubSelection(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        sub_list = AssignSub.objects.filter(teacher_id=teacher_info.id,class_id__passed_out=False,class_id__sem_number=F('sem')).order_by('class_id')
        return render(request,'teacher/select-sub.html',{'sub_list':sub_list,'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherDaySelection(request,class_id,sem_no,sub_id):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        try:
            ttc_info = TimetableClass.objects.get(class_id=class_id,sem=sem_no)
            start_date = ttc_info.start  
            end_date = ttc_info.end
        except Exception:
            ttc_info = None
            tt_t = None
            start_date = None
            end_date =None
        if not ttc_info:
            messages.error(request,'Timetable not added')
            return redirect('teacherSubSelection')
        context={
                 'sub_id':sub_id,
                 'ttc_info':ttc_info,
                 'teacher_info':teacher_info,
                 'start_date': start_date,
                 'end_date': end_date
                 }
        return render(request,'teacher/select-day.html',context)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherHourSelection(request, class_id, sem_no, sub_id, date):
    if 'teacher' in request.session:
        # Convert the date from the URL into a Python date object
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        day_of_week  = date_obj.strftime('%A')  # Get the day of the week (e.g., 'Monday')

        # Get the timetable entries for the specified class, semester, and day of the week
        timetables = Timetable.objects.filter(tt_id__class_id=class_id, tt_id__sem=sem_no, day_of_week=day_of_week)
        if not timetables.exists():
            timetables = SpecialTimetable.objects.filter(tt_id__class_id=class_id, tt_id__sem=sem_no,date=date)
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        context = {
            'class_id':class_id,
            'sem_no':sem_no,
            'sub_id':sub_id,
            'day_of_week': day_of_week,
            'timetables': timetables,
            'date' : date_obj,
            'teacher_info':teacher_info,
        }

        return render(request, 'teacher/select-daily-timetable.html', context)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherMarkAttendance(request, class_id, sem_no, sub_id, date, tt_id):
    if 'teacher' in request.session:
        # Get the list of students for the class
        student_list = Student.objects.filter(stts=1, class_id=class_id)
        subject = Subjects.objects.get(id=sub_id)
        date_obj = datetime.strptime(date, '%Y-%m-%d')  # Convert string date to date object
        try:
            stt_obj = SpecialTimetable.objects.get(id=tt_id,date=date_obj)
            time_slot = stt_obj.time_slot.start_time
            tt_obj = None
        except:
            stt_obj = None
            tt_obj = Timetable.objects.get(id=tt_id)
            time_slot = tt_obj.time_slot.start_time
                
          # Get the time slot for the timetable
        
        # Fetch existing attendance records for the specified date and time slot
        existing_attendance = Attendance.objects.filter(
            date=date_obj,
            stt_id=tt_obj,
            sptt_id=stt_obj,# Ensure to filter by the timetable ID as well
            sub_id=subject
        ).select_related('stud_id')  # Optimize related student fetching

        # Create a dictionary to hold the attendance status
        attendance_status_dict = {
            attendance.stud_id.id: attendance.attendance_status for attendance in existing_attendance
        }

        if request.method == "POST":
            for student in student_list:
                # Check if their attendance status is submitted
                attendance_status = request.POST.get(f'attendance_{student.id}') == 'present'
                # Update or create attendance record
                Attendance.objects.update_or_create(
                    stud_id=student,
                    stt_id=tt_obj,
                    sptt_id=stt_obj,
                    sub_id=subject,
                    sem_no=sem_no,
                    date=date_obj,
                    defaults={
                        'attendance_status': attendance_status,
                        'time': time_slot
                    }
                )

            messages.success(request, "Attendance updated successfully")
            return redirect('teacherMarkAttendance', class_id=class_id, sem_no=sem_no, sub_id=sub_id, date=date, tt_id=tt_id)

        # Get teacher information
        teacher_info = Teacher.objects.get(id=request.session['teacher'])

        context = {
            'student_list': student_list,
            'class_id': class_id,
            'sem_no': sem_no,
            'sub_id': sub_id,
            'date': date_obj,
            'teacher_info': teacher_info,
            'attendance_status_dict': attendance_status_dict,  # Pass the attendance status to the template
        }

        return render(request, 'teacher/select-attendance-list.html', context)
    else:
        messages.error(request, "Please log in as a teacher to access this page.")
        return redirect('index')




def teacherClassInfo(request, tid):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        class_info = Classes.objects.get(id=tid)
        if request.method == "POST":
            class_info.sem_number = int(request.POST['sem'])
            try:
                passed_out = request.POST['passed']
            except Exception:
                passed_out = 'n'
            if passed_out=='y' and class_info.passed_out == False:
                teacher_info.isIncharge = False
                teacher_info.save()
                class_info.passed_out = True
                class_info.save()
                messages.success(request, "Class set as passed out successfully")
                return redirect('teacherHome')
            class_info.save()
            messages.success(request, "Class info updated successfully")
            return redirect('teacherClassInfo', tid=tid)
        teacher_list = Teacher.objects.filter(isIncharge=False,stts=1,department_id=class_info.course_id.department_id.id).order_by('fname')
        course_list = Courses.objects.all().order_by('course_title')
        return render(request, 'teacher/edit-class.html', {'teacher_list': teacher_list, 'course_list': course_list, 'class': class_info,'teacher_info': teacher_info})
    else:
        messages.error(request, logout_msg)
        return redirect('index')
    
    
def teacherClassAttendanceList(request):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        class_list = AssignSub.objects.filter(teacher_id=teacher_info.id,class_id__passed_out=False).distinct()
        distinct_class_ids = AssignSub.objects.filter(
        teacher_id=teacher_info.id, 
        class_id__passed_out=False).values_list('class_id', flat=True).distinct()
        class_list = Classes.objects.filter(id__in=distinct_class_ids)
        
        return render(request,'teacher/list-attendance-class.html',{'class_list':class_list,'teacher_info':teacher_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def teacherAttendanceSub(request,class_id):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        semesters = range(1, Classes.objects.get(id=class_id).course_id.sem_count+1)
        sub_list={}
        if request.method == "POST":
            sem = request.POST['sem']
            sub_list = AssignSub.objects.filter(class_id=class_id,sem=sem)
        return render(request,'teacher/list-attendance-sub.html',{'sub_list':sub_list,'teacher_info':teacher_info,'sem_count':semesters})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def teacherAttendanceStud(request, class_id, sub_id):
    if 'teacher' in request.session:
        teacher_info = Teacher.objects.get(id=request.session['teacher'])
        
        # Get the class and subject
        class_info = Classes.objects.get(id=class_id)
        subject = Subjects.objects.get(id=sub_id)

        # Get the list of students in the class
        students = Student.objects.filter(class_id=class_info)
        
        # Create a list to store attendance information for each student
        attendance_list = []

        for student in students:
            # Get all attendance records for this student and subject
            total_classes = Attendance.objects.filter(stud_id=student, sub_id=subject).count()

            # Get attended classes (where attendance_status is True)
            attended_classes = Attendance.objects.filter(stud_id=student, sub_id=subject, attendance_status=True).count()

            # Calculate attendance percentage
            if total_classes > 0:
                attendance_percentage = (attended_classes / total_classes) * 100
            else:
                attendance_percentage = 0  # If no classes found, set percentage to 0

            # Add the data to the list
            attendance_list.append({
                'student': student,
                'attended_classes': attended_classes,
                'total_classes': total_classes,
                'attendance_percentage': attendance_percentage
            })

        # Pass the attendance data to the template
        context = {
            'teacher_info': teacher_info,
            'class_info': class_info,
            'subject': subject,
            'attendance_list': attendance_list,
        }
        
        return render(request, 'teacher/list-attendance-stud.html', context)
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('index')

