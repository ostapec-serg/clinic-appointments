from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doctors/', include('doctors.urls')),
    path('api/appointments/', include('appointment.urls')),
    path('api/schedules/', include('schedule.urls')),
    # path('api/doctor/schedules/', include('schedule.urls')),
]
