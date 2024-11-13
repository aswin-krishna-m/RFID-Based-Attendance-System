from django.urls import path
from .views import MarkAttendanceAPIView

urlpatterns = [
    path('api/attendance/', MarkAttendanceAPIView.as_view(), name='mark-attendance'),
]
