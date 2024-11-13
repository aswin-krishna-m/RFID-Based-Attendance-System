from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from usersApp.models import *
from django.contrib import messages
from datetime import date

def currentDate():
    return date.today()

logout_msg = 'You have to be logged in first!'

# COMMON VIEW

def index(request):
    return render(request,'index.html')

# ADMIN VIEWS

def adminLogin(request):
    if request.method=="POST":
        uname = request.POST['uname']
        password = request.POST['password']
        try:
            user = Admin.objects.get(username=uname)
            if user.password == password:
                request.session['admin'] = user.id
                messages.success(request,'Login Success!')
                return redirect('adminHome')
            else:
                messages.error(request,'Incorrect Password!')
                return redirect('adminLogin')
        except:
            messages.error(request,'Incorrect Username!')
            return redirect('adminLogin')
    elif 'admin' in request.session:
        return redirect('adminHome')
    else:
        return render(request,'myAdmin/login.html')

def adminHome(request):
    if 'admin' in request.session:
        admin_info = Admin.objects.get(id=request.session['admin'])
        model_count ={
            'student': Student.objects.count(),
            'teacher': Teacher.objects.count(),
            'dept': Department.objects.count(),
            'course': Courses.objects.count(),
            'class': Classes.objects.count(),
            'sub': Subjects.objects.count(),
            } 
        return render(request,'myAdmin/index.html',{'total_count':model_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def adminProfile(request):
    if 'admin' in request.session:
        if request.method=="POST":
            uname = request.POST['username']
            email = request.POST['email']
            admin_info = Admin.objects.get(id=request.session['admin'])
            if Admin.objects.filter(username=uname).count()>1:
                messages.error(request, 'Username already taken!')
            elif Admin.objects.filter(email=email).count()>1:
                messages.error(request, 'Email already taken!')
            else:
                admin_info.username =uname
                admin_info.email = email
                admin_info.save()
                messages.success(request,"Profile Updated Successfully")
            return redirect('adminProfile')
        else:
            admin_info = Admin.objects.get(id=request.session['admin'])
            return render(request,'myAdmin/profile.html',{'admin_info':admin_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def adminPassword(request):
    if 'admin' in request.session:
        if request.method=="POST":
            cpass = request.POST['cpass']
            npass = request.POST['npass']
            cpsw = request.POST['cpsw']
            admin_info = Admin.objects.get(id=request.session['admin'])
            if cpass != admin_info.password:
                messages.error(request,"Current Password is wrong!")
            elif cpsw!= npass:
                messages.error(request,"Passwords do not match!")
            else:
                admin_info.password =npass
                admin_info.save()
                messages.success(request,"Password Updated Successfully!")
            return redirect('adminProfile')
        else:
            admin_info = Admin.objects.get(id=request.session['admin'])
            return render(request,'myAdmin/profile.html',{'admin_info':admin_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def adminLogout(request):
    if 'admin' in request.session:
        del request.session['admin']
        messages.success(request,'Logged out successfully')
        return redirect('index')
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminStudentList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            sid = request.POST['id']
            del_obj = Student.objects.get(id=sid)
            del_obj.delete()
            messages.success(request,"Student removed!")
            return redirect('adminStudentList')
        student_list = Student.objects.filter(stts=1).order_by('fname')
        req_count = Student.objects.filter(stts=0).count()
        return render(request,'myAdmin/list-student.html',{'student_list':student_list,'req_count':req_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminStudentReqList(request):
    if 'admin' in request.session:
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
                
            return redirect('adminStudentReqList')

        # Get all students with pending status
        student_list = Student.objects.filter(stts=0).order_by('fname')
        return render(request, 'myAdmin/list-student-req.html', {'student_list': student_list})

    else:
        messages.error(request, 'You must be logged in as admin to access this page.')
        return redirect('index')

    
def adminStudentInfo(request,id):
    if 'admin' in request.session:
        student_info = Student.objects.get(id=id)
        if request.method=="POST":
            student_info.fname = request.POST['fname']
            student_info.lname = request.POST['lname']
            student_info.roll = request.POST['roll']
            student_info.gender = request.POST['gender']
            student_info.dob = request.POST['dob']
            student_info.email = request.POST['email']
            student_info.phone = request.POST['phone']
            student_info.password = request.POST['password']
            student_info.course_id = Courses.objects.get(id=request.POST['course'])
            student_info.stts = request.POST['stts']
            student_info.save()
            messages.success(request,"Student Profile Updated successfully")
            return redirect('adminStudentInfo',id=id)
        course_list = Courses.objects.all().order_by('course_title')
        class_list = Classes.objects.filter(course_id=student_info.course_id).order_by('sem_number')
        return render(request,'myAdmin/view-student.html',{'student':student_info,'course_list':course_list,'class_list':class_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminStudentReqInfo(request,id):
    if 'admin' in request.session:
        student_info = Student.objects.get(id=id)
        if request.method=="POST":
            student_info.stts = request.POST['stts']
            student_info.save()
            messages.success(request,"Student Status Updated successfully")
            return redirect('adminStudentReqInfo',id=id)
        course_list = Courses.objects.all().order_by('course_title')
        return render(request,'myAdmin/view-student-req.html',{'student':student_info,'course_list':course_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminTeacherList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            tid = request.POST['id']
            del_obj = Teacher.objects.get(id=tid)
            del_obj.delete()
            messages.success(request,"Teacher removed!")
            return redirect('adminTeacherList')
        teacher_list = Teacher.objects.filter(stts=1).order_by('fname')
        req_count = Teacher.objects.filter(stts=0).count()
        return render(request,'myAdmin/list-teacher.html',{'teacher_list':teacher_list,'req_count':req_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminTeacherReqList(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            teacher_ids = request.POST.getlist('teacher_ids')
            action = request.POST.get('action')
            
            if action== 'deleteOne':
                    deleteOne = request.POST.get('deleteId')
                    del_obj = Teacher.objects.get(id=deleteOne)
                    del_obj.delete()
                    messages.success(request,"Teacher removed!")
            elif teacher_ids:
                teachers = Teacher.objects.filter(id__in=teacher_ids)
                if  action == 'verify':
                    # Verify the selected teachers
                    teachers.update(stts=1)  # Assuming '1' indicates verified status
                    messages.success(request, 'Selected teachers have been verified successfully.')

                elif action == 'delete':
                    # Delete the selected teachers
                    teachers.delete()
                    messages.success(request, 'Selected teachers have been deleted successfully.')
            else:
                messages.error(request, 'No teachers selected.')
        teacher_list = Teacher.objects.filter(stts=0).order_by('fname')
        return render(request,'myAdmin/list-teacher-req.html',{'teacher_list':teacher_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminTeacherInfo(request,id):
    if 'admin' in request.session:
        teacher_info = Teacher.objects.get(id=id)
        if request.method=="POST":
            teacher_info.fname = request.POST['fname']
            teacher_info.lname = request.POST['lname']
            teacher_info.email = request.POST['email']
            teacher_info.dob = request.POST['dob']
            teacher_info.gender = request.POST['gender']
            teacher_info.phone = request.POST['phone']
            teacher_info.password = request.POST['password']
            teacher_info.department_id = Department.objects.get(id=request.POST['dept'])
            teacher_info.stts = request.POST['stts']
            teacher_info.save()
            messages.success(request,"Teacher Profile Updated successfully")
            return redirect('adminTeacherInfo',id=id)
        try:
            class_id = Classes.objects.get(class_in_charge=teacher_info.id)
        except:
            class_id = None
        dept_list = Department.objects.all().order_by('dept_name')
        sub_list = AssignSub.objects.filter(teacher_id=id)
        return render(request,'myAdmin/view-teacher.html',{'cid':class_id,'teacher':teacher_info,'dept_list':dept_list,'sub_list':sub_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminTeacherReqInfo(request,id):
    if 'admin' in request.session:
        teacher_info = Teacher.objects.get(id=id)
        if request.method=="POST":
            teacher_info.stts = request.POST['stts']
            teacher_info.save()
            messages.success(request,"Teacher Status Updated successfully")
            return redirect('adminTeacherReqInfo',id=id)
        try:
            class_id = Classes.objects.get(class_in_charge=teacher_info.id)
        except:
            class_id = None
        dept_list = Department.objects.all().order_by('dept_name')
        return render(request,'myAdmin/view-teacher-req.html',{'cid':class_id,'teacher':teacher_info,'dept_list':dept_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')


def adminDeptList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            deptname = request.POST['deptname'].upper()
            shortname = request.POST['shortname'].upper()
            created_on = currentDate()
            dept_exists = Department.objects.filter(dept_name=deptname)
            if dept_exists:
                messages.error(request,"Department Already Added")
            else:
                query = Department.objects.create(dept_name= deptname, short_name=shortname,created_on=created_on)
                query.save()
                messages.success(request,"Department Added Successfully")
            return redirect('adminDeptList')
        dept_list = Department.objects.all().order_by('dept_name')
        return render(request,'myAdmin/list-department.html',{'dept_list':dept_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def adminDeptTeacherList(request,did):
    if 'admin' in request.session:
        if request.method=="POST":
            tid = request.POST['id']
            del_obj = Teacher.objects.get(id=tid)
            del_obj.delete()
            messages.success(request,"Teacher removed!")
            return redirect('adminDeptTeacherList',did=did)
        teacher_list = Teacher.objects.filter(stts=1,department_id=did).order_by('fname')
        req_count = Teacher.objects.filter(stts=0).count()
        return render(request,'myAdmin/list-dept-teacher.html',{'teacher_list':teacher_list,'req_count':req_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminDeptInfo(request,id):
    if 'admin' in request.session:
        dept_info = Department.objects.get(id=id)
        if request.method=="POST":
            dept_info.dept_name = request.POST['dept_name'].upper()
            dept_info.short_name = request.POST['short_name'].upper()
            dept_info.save()
            messages.success(request,"Department info updated successfully")
            return redirect('adminDeptInfo',id=id)
        return render(request,'myAdmin/view-dept.html',{'dept':dept_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')

def adminDeptDel(request,id):
    if 'admin' in request.session:
        del_obj = Department.objects.get(id=id)
        del_obj.delete()
        messages.success(request,"Department removed!")
        return redirect('adminDeptList')
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminCourseList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            dept_id = Department.objects.get(id=request.POST['dept'])
            coursename = request.POST['coursename'].upper()
            shortname = request.POST['shortname'].upper()
            semcount = request.POST['semcount']
            created_on = currentDate()
            dept_exists = Courses.objects.filter(course_title=coursename)
            if dept_exists:
                messages.error(request,"Course Already Added")
            else:
                query = Courses.objects.create(department_id=dept_id,course_title=coursename,short_name=shortname,sem_count=semcount,created_on=created_on)
                query.save()
                messages.success(request,f"Course Added Successfully")
            return redirect('adminCourseList')
        course_list = Courses.objects.all().order_by('course_title')
        dept_list = Department.objects.all().order_by('dept_name')
        return render(request,'myAdmin/list-course.html',{'dept_list':dept_list,'course_list':course_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminCourseInfo(request,id):
    if 'admin' in request.session:
        course_info = Courses.objects.get(id=id)
        if request.method=="POST":
            course_info.department_id = Department.objects.get(id=request.POST['dept'])
            course_info.course_title = request.POST['course_name'].upper()
            course_info.short_name = request.POST['short_name'].upper()
            course_info.sem_count = int(request.POST['sem_count'])
            course_info.save()
            messages.success(request,"Course info updated successfully")
            return redirect('adminCourseInfo',id=id)
        dept_list = Department.objects.all().order_by('dept_name')
        return render(request,'myAdmin/view-course.html',{'dept_list':dept_list,'course':course_info})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminCourseDel(request,id):
    if 'admin' in request.session:
        del_obj = Courses.objects.get(id=id)
        del_obj.delete()
        messages.success(request,"Course removed!")
        return redirect('adminCourseList')
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminClassList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            course_id = Courses.objects.get(id=request.POST['course'])
            startyear = int(request.POST['start'])
            if not request.POST['sem']:
                sem=1
            else:
                sem = int(request.POST['sem'])
            endyear= startyear+(course_id.sem_count//2)
            created_on = currentDate()
            division = request.POST['division'].upper()
            if division=="":
                division = "A"
            division_exists = Classes.objects.filter(course_id=course_id,sem_number=sem,start_year=startyear,passed_out=False,division_name=division).count()
            if division_exists>=1:
                messages.error(request,"This division is already Added, Add another division name")
                return redirect('adminClassList')
            else:
                query = Classes.objects.create(course_id=course_id,start_year=startyear,end_year=endyear,sem_number=sem,division_name=division,created_on=created_on)
                query.save()
                messages.success(request,f"Class Added Successfully")
                return redirect('adminClassList')
        class_list = Classes.objects.filter(passed_out=False).order_by('sem_number')[::-1]
        req_count = Classes.objects.filter(passed_out=True).count()
        course_list = Courses.objects.all().order_by('course_title')
        return render(request,'myAdmin/list-class.html',{'class_list':class_list,'course_list':course_list,'req_count':req_count})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminClassInfo(request, id):
    if 'admin' in request.session:
        class_info = Classes.objects.get(id=id)
        if request.method == "POST":
            class_info.course_id = Courses.objects.get(id=request.POST['course'])
            class_info.start_year = int(request.POST['start'])
            class_info.end_year = class_info.start_year + (class_info.course_id.sem_count)//2
            class_info.sem_number = int(request.POST['sem'])
            division = request.POST['division'].upper()
            inc = request.POST['incharge']
            
            division_exists = Classes.objects.filter(course_id=class_info.course_id, passed_out=False, division_name=division).exists()
            
            if division_exists and division != class_info.division_name:
                messages.error(request, "This division is already Added")
                return redirect('adminClassInfo', id=id)
            else:
                class_info.division_name = division
            if not inc:
                inc = None
            try:
                teacher_id = Teacher.objects.get(id=inc)
                if class_info.class_in_charge:
                    class_info.class_in_charge.isIncharge = False
                    class_info.class_in_charge.save()
                teacher_id.isIncharge = True
                class_info.class_in_charge = teacher_id
                teacher_id.save()
            except Teacher.DoesNotExist:
                class_info.class_in_charge = None
                messages.error(request, "Teacher not found.")
            
            class_info.save()
            messages.success(request, "Class info updated successfully")
            return redirect('adminClassInfo', id=id)

        teacher_list = Teacher.objects.filter(isIncharge=False,stts=1,department_id=class_info.course_id.department_id.id).order_by('fname')
        course_list = Courses.objects.all().order_by('course_title')
        return render(request, 'myAdmin/view-class.html', {'teacher_list': teacher_list, 'course_list': course_list, 'class': class_info})
    else:
        messages.error(request, logout_msg)
        return redirect('index')
    
def adminClassListPassed(request):
    if 'admin' in request.session:
        class_list = Classes.objects.filter(passed_out=True).order_by('created_on')[::-1]
        return render(request,'myAdmin/pass-out-list.html',{'class_list':class_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminClassInfoPassed(request, id):
    if 'admin' in request.session:
        class_info = Classes.objects.get(id=id)
        return render(request, 'myAdmin/pass-view-class.html', {'class': class_info})
    else:
        messages.error(request, logout_msg)
        return redirect('index')

def adminClassStudentList(request,cid):
    if 'admin' in request.session:
        if request.method=="POST":
            sid = request.POST['id']
            del_obj = Student.objects.get(id=sid)
            del_obj.delete()
            messages.success(request,"Student removed!")
            return redirect('adminClassStudentList',cid=cid)
        student_list = Student.objects.filter(stts=1,class_id=cid).order_by('fname')
        return render(request,'myAdmin/list-class-student.html',{'student_list':student_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminClassStudentAdd(request,sid):
    if 'admin' in request.session:
        cid = request.POST.get('class')
        class_obj = Classes.objects.get(id=cid)
        stud_obj = Student.objects.get(id=sid)
        stud_obj.class_id = class_obj
        stud_obj.save()
        messages.success(request,"Student added to class!")
        return redirect('adminStudentInfo',id=sid)
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminClassDel(request,id):
    if 'admin' in request.session:
        del_obj = Classes.objects.get(id=id)
        if del_obj.class_in_charge:
            del_obj.class_in_charge.isIncharge = False
            del_obj.class_in_charge.save()
        del_obj.delete()
        messages.success(request,"Class removed!")
        return redirect('adminClassList')
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminSubList(request):
    if 'admin' in request.session:
        if request.method=="POST":
            course_id = Courses.objects.get(id=request.POST['course'])
            title = request.POST['title'].upper()
            code = request.POST['code'].upper()
            subject_exists = Subjects.objects.filter(course_id=course_id,code=code).exists()        
            if subject_exists:
                messages.error(request,"This subject is already added")
                return redirect('adminSubList')
            else:
                query = Subjects.objects.create(course_id=course_id,code=code,sub_title=title)
                query.save()
                messages.success(request,f"Subject Added Successfully")
                return redirect('adminSubList')
        sub_list = Subjects.objects.all().order_by('sub_title')
        course_list = Courses.objects.all().order_by('course_title')
        return render(request,'myAdmin/list-sub.html',{'sub_list':sub_list,'course_list':course_list})
    else:
        messages.error(request,logout_msg)
        return redirect('index')
    
def adminSubInfo(request, id):
    if 'admin' in request.session:
        sub_info = Subjects.objects.get(id=id)
        if request.method == "POST":
            sub_info.course_id = Courses.objects.get(id=request.POST['course'])
            sub_info.code = request.POST['code'].upper()
            sub = request.POST['title'].upper()
            sub_exists = Subjects.objects.filter(course_id=sub_info.course_id,code=sub_info.code,sub_title=sub).exists()
            if sub_exists and sub != sub_info.sub_title:
                messages.error(request, "This subject is already Added")
                return redirect('adminSubInfo', id=id)
            else:
                sub_info.sub_title = sub          
            sub_info.save()
            messages.success(request, "Class info updated successfully")
            return redirect('adminSubInfo', id=id)

        teacher_list = Teacher.objects.filter(stts=1).order_by('fname')
        class_list = Classes.objects.filter(course_id = sub_info.course_id).order_by('sem_number')
        course_list = Courses.objects.all().order_by('course_title')
        try:
            assigned = AssignSub.objects.get(sub_id = sub_info)
        except AssignSub.DoesNotExist:
            assigned = None
        return render(request, 'myAdmin/view-sub.html', {'teacher_list': teacher_list, 'class_list': class_list, 'course_list': course_list,'assigned': assigned, 'sub': sub_info})
    else:
        messages.error(request, logout_msg)
        return redirect('index')

    
def adminSubDel(request,id):
    if 'admin' in request.session:
        del_obj = Subjects.objects.get(id=id)
        del_obj.delete()
        messages.success(request,"Subject removed!")
        return redirect('adminSubList')
    else:
        messages.error(request,logout_msg)
        return redirect('index')



def adminClassAttendance(request, class_id):
    if 'admin' in request.session:
        student_attendance_data = []
        subjects = []
        selected_sem = None
        class_obj = get_object_or_404(Classes, id=class_id)

        if request.method == "POST":
            # Get the selected semester from the form POST data
            selected_sem = request.POST.get('semester')

            if selected_sem:
                selected_sem = int(selected_sem)

                # Fetch all subjects for the class and selected semester
                subjects = AssignSub.objects.filter(
                    class_id=class_obj, sem=selected_sem
                )

                # Fetch all students in the class
                students = Student.objects.filter(class_id=class_obj)

                for student in students:
                    attendance_records = []
                    total_attendance = 0
                    total_classes = 0

                    for subject in subjects:
                        # Fetch attendance for each subject and student
                        attended_classes = Attendance.objects.filter(
                            stud_id=student,
                            sub_id=subject.sub_id,
                            sem_no=selected_sem,
                            attendance_status=True
                        ).count()

                        total_subject_classes = Attendance.objects.filter(
                            stud_id=student,
                            sub_id=subject.sub_id,
                            sem_no=selected_sem
                        ).count()

                        # Calculate attendance percentage for each subject
                        if total_subject_classes > 0:
                            attendance_percentage = (attended_classes / total_subject_classes) * 100
                        else:
                            attendance_percentage = 0

                        attendance_records.append(round(attendance_percentage, 2))
                        total_attendance += attended_classes
                        total_classes += total_subject_classes

                    # Calculate total attendance percentage for the student
                    if total_classes > 0:
                        total_attendance_percentage = (total_attendance / total_classes) * 100
                    else:
                        total_attendance_percentage = 0

                    student_attendance_data.append({
                        'fname': student.fname,
                        'lname': student.lname,
                        'attendance': attendance_records,
                        'total_attendance': round(total_attendance_percentage, 2)
                    })

        context = {
            'class_id': class_id,
            'students': student_attendance_data,
            'subjects': subjects,
            'semesters': range(1, class_obj.sem_number + 1),
            'selected_sem': selected_sem
        }
        return render(request, 'myAdmin/class_attendance.html', context)

    else:
        messages.error(request, 'You need to log in to access this page.')
        return redirect('index')

