from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from appointment.filters import AppointmentsFilter
from appointment.models import Appointment
from appointment.serializers import AppointmentsSerializer
from doctors.permissions import IsStaffReadOnly, IsAuthenticatedWriteOnly


class BaseAppointmentsAPIView(GenericAPIView):
    queryset = Appointment.objects.all().order_by('-date')
    serializer_class = AppointmentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AppointmentsFilter


class ListAppointmentsAPIView(ListAPIView, BaseAppointmentsAPIView):
    """
    A viewset class for viewing Appointments instances list.
    """
    # permission_classes = (IsStaffReadOnly,)

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        today_date = datetime.today()
        self.queryset = self.get_queryset().exclude(date__lt=today_date)
        return self.list(request, *args, **kwargs)


class CreateAppointmentAPIView(CreateAPIView,
                               BaseAppointmentsAPIView):
    """
    A view class for validation POST.data before
    creating Appointment instance.
    """
    # permission_classes = (IsAuthenticatedWriteOnly,)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        data = self.request.POST.dict()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validate_appointment_data():
                return self.create(request, *args, **kwargs)
        return Response(serializer.error_message)
