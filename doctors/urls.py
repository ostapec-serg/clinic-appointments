from django.urls import path

from doctors.views import DoctorsAPIView


urlpatterns = [
    path('', DoctorsAPIView.as_view(), name='doctors-list'),
]
