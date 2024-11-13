from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('admin/',views.adminHome,name='adminHome'),
    path('adminLogin/',views.adminLogin,name='adminLogin'),
    path('adminProfile/',views.adminProfile,name='adminProfile'),
    path('adminPassword/',views.adminPassword,name='adminPassword'),
    path('adminLogout/',views.adminLogout,name='adminLogout'),
    
    path('adminStudentList/',views.adminStudentList,name='adminStudentList'),
    path('adminStudentReqList/',views.adminStudentReqList,name='adminStudentReqList'),
    path('adminStudentInfo/<int:id>/',views.adminStudentInfo,name='adminStudentInfo'),
    path('adminStudentReqInfo/<int:id>/',views.adminStudentReqInfo,name='adminStudentReqInfo'),
    
    path('adminTeacherList/',views.adminTeacherList,name='adminTeacherList'),
    path('adminTeacherReqList/',views.adminTeacherReqList,name='adminTeacherReqList'),
    path('adminTeacherInfo/<int:id>/',views.adminTeacherInfo,name='adminTeacherInfo'),
    path('adminTeacherReqInfo/<int:id>/',views.adminTeacherReqInfo,name='adminTeacherReqInfo'),
    
    path('adminDeptList/',views.adminDeptList,name='adminDeptList'),
    path('adminDeptTeacherList/<int:did>',views.adminDeptTeacherList,name='adminDeptTeacherList'),
    path('adminDeptInfo/<int:id>',views.adminDeptInfo,name='adminDeptInfo'),
    path('adminDeptDel/<int:id>',views.adminDeptDel,name='adminDeptDel'),
    
    path('adminCourseList/',views.adminCourseList,name='adminCourseList'),
    path('adminCourseInfo/<int:id>',views.adminCourseInfo,name='adminCourseInfo'),
    path('adminCourseDel/<int:id>',views.adminCourseDel,name='adminCourseDel'),
    
    path('adminClassList/',views.adminClassList,name='adminClassList'),
    path('adminClassListPassed/',views.adminClassListPassed,name='adminClassListPassed'),
    path('adminClassStudentList/<int:cid>',views.adminClassStudentList,name='adminClassStudentList'),
    path('adminClassStudentAdd/<int:sid>',views.adminClassStudentAdd,name='adminClassStudentAdd'),
    path('adminClassInfo/<int:id>',views.adminClassInfo,name='adminClassInfo'),
    path('adminClassInfoPassed/<int:id>',views.adminClassInfoPassed,name='adminClassInfoPassed'),
    path('adminClassDel/<int:id>',views.adminClassDel,name='adminClassDel'),
    path('adminClassAttendance/<int:class_id>',views.adminClassAttendance,name='adminClassAttendance'),
    
    path('adminSubList/',views.adminSubList,name='adminSubList'),
    path('adminSubInfo/<int:id>',views.adminSubInfo,name='adminSubInfo'),
    path('adminSubDel/<int:id>',views.adminSubDel,name='adminSubDel'),
    
    
    ]