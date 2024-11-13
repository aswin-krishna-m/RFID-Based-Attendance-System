from django.urls import path
from . import views

urlpatterns = [
    
    # Student URLs
    path('studentLogin/',views.studentLogin,name='studentLogin'),
    path('studentGetClass/<course_id>/',views.studentGetClass,name='studentGetClass'),
    path('studentRegister/',views.studentRegister,name='studentRegister'),
    path('studentHome/',views.studentHome,name='studentHome'),
    path('studentProfile/',views.studentProfile,name='studentProfile'),
    path('studentPassword/',views.studentPassword,name='studentPassword'),
    path('studentLogout/',views.studentLogout,name='studentLogout'),
    path('studentAttendance/',views.studentAttendance,name='studentAttendance'),
    
    
    # Teacher URLs
    path('teacherLogin/',views.teacherLogin,name='teacherLogin'),
    path('teacherRegister/',views.teacherRegister,name='teacherRegister'),
    path('teacherHome/',views.teacherHome,name='teacherHome'),
    path('teacherProfile/',views.teacherProfile,name='teacherProfile'),
    path('teacherPassword/',views.teacherPassword,name='teacherPassword'),
    path('teacherLogout/',views.teacherLogout,name='teacherLogout'),
    path('teacherSubList/<int:tid>',views.teacherSubList,name='teacherSubList'),
    path('teacherMySubList/<int:cid>',views.teacherMySubList,name='teacherMySubList'),
    path('teacherSubInfo/<int:cid>/<int:sid>',views.teacherSubInfo,name='teacherSubInfo'),
    path('teacherEditAssignSub/<int:class_id>/<int:sem_no>/<int:aid>',views.teacherEditAssignSub,name='teacherEditAssignSub'),
    path('teacherSubDel/<int:cid>/<int:sid>',views.teacherSubDel,name='teacherSubDel'),
    path('teacherClassInfo/<int:tid>',views.teacherClassInfo,name='teacherClassInfo'),
    path('teacherClassList/<int:tid>',views.teacherClassList,name='teacherClassList'),
    path('teacherClassStudentList/<int:id>',views.teacherClassStudentList,name='teacherClassStudentList'),
    path('teacherMyClassStudentReqList/<int:id>',views.teacherMyClassStudentReqList,name='teacherMyClassStudentReqList'),
    path('teacherStudentInfo/<int:id>',views.teacherStudentInfo,name='teacherStudentInfo'),
    path('teacherMyClass/',views.teacherMyClass,name='teacherMyClass'),
    path('teacherMyClassStudentList/<int:id>',views.teacherMyClassStudentList,name='teacherMyClassStudentList'),
    path('teacherSetUpSem/<int:class_id>',views.teacherSetUpSem,name='teacherSetUpSem'),
    path('teacherDelAssigned/<int:id>',views.teacherDelAssigned,name='teacherDelAssigned'),
    path('teacherAssignSub/<int:class_id>/<int:sem_no>/',views.teacherAssignSub,name='teacherAssignSub'),
    path('teacherTimetableGen/<int:class_id>/<int:sem_no>/', views.teacherTimetableGen, name='teacherTimetableGen'),
    path('teacherTimetableViewEdit/<int:class_id>/<int:sem_no>/', views.teacherTimetableViewEdit, name='teacherTimetableViewEdit'),
    path('teacherSpTimetableCreate/<int:class_id>/<int:sem_no>/', views.teacherSpTimetableCreate, name='teacherSpTimetableCreate'),
    path('teacherSpTimetableView/<int:class_id>/<int:sem_no>/<str:date>/', views.teacherSpTimetableView, name='teacherSpTimetableView'),
    path('teachersetTimetable/<int:class_id>/<int:sem_no>/', views.teachersetTimetable, name='teachersetTimetable'),    
    path('teacherSubSelection/', views.teacherSubSelection, name='teacherSubSelection'),    
    path('teacherDaySelection/<int:class_id>/<int:sem_no>/<int:sub_id>', views.teacherDaySelection, name='teacherDaySelection'),    
    path('teacherHourSelection/<int:class_id>/<int:sem_no>/<int:sub_id>/<str:date>/', views.teacherHourSelection, name='teacherHourSelection'),    
    path('teacherMarkAttendance/<int:class_id>/<int:sem_no>/<int:sub_id>/<str:date>/<int:tt_id>/', views.teacherMarkAttendance, name='teacherMarkAttendance'),    
    path('teacherClassAttendanceList/', views.teacherClassAttendanceList, name='teacherClassAttendanceList'),    
    path('teacherAttendanceSub/<int:class_id>/', views.teacherAttendanceSub, name='teacherAttendanceSub'), 
    path('teacherAttendanceStud/<int:class_id>/<int:sub_id>/', views.teacherAttendanceStud, name='teacherAttendanceStud'), 
    
]
