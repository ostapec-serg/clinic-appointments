from django.urls import path

from appointment import views


app_name = "appointment"

urlpatterns = [
    path('create/', views.CreateAppointmentAPIView.as_view(), name='add-appointment'),
    path('', views.ListAppointmentsAPIView.as_view(), name='appointments'),
]
