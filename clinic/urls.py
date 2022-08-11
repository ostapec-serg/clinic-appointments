from django.contrib import admin
from django.urls import path, include
# from wagtail.documents import urls as wagtailadmin_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('api/doctors/', include('doctors.urls')),
    path('api/appointments/', include('appointment.urls')),
    path('api/schedules/', include('schedule.urls')),
]
