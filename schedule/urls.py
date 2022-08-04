from django.urls import path

from schedule.views import DateDoctorScheduleView, DayDoctorScheduleView


app_name = 'schedule'

urlpatterns = [
    path('<pk>/day/<day>/', DayDoctorScheduleView.as_view(), name='day-schedule'),
    path('<pk>/date/<date>/', DateDoctorScheduleView.as_view(), name='date-schedule'),
]
