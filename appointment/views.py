from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from appointment.filters import AppointmentsFilter
from appointment.models import Appointment
from appointment.serializers import AppointmentsSerializer
from doctors.models import Doctor
from doctors.permissions import IsStaffReadOnly, IsAuthenticatedWriteOnly
from schedule.models import Schedule


class BaseAppointmentsAPIView(GenericAPIView):
    queryset = Appointment.objects.all().order_by('-date')
    serializer_class = AppointmentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AppointmentsFilter


class CheckAppointmentData:
    data = None
    error_message = {'message': 'Wrong data input'}
    delta = timedelta(seconds=1)

    def validate_appointment_data(self, request, *args, **kwargs):
        """
        Method for checking data for appointment
        """
        if self.update_data_attribute():
            date = self.check_date_schedule(request)
            time = self.check_time(request)
            location = self.check_location(request)
            if date and time and location:
                return self.data

    def update_data_attribute(self, *args, **kwargs):
        """
        Method for updating the 'self.data' attribute
        that will be used to check the appointment
        """
        if self.data:
            start = datetime.strptime(self.data['start'], "%H:%M") + self.delta
            end = datetime.strptime(self.data['end'], "%H:%M") - self.delta
            date = datetime.strptime(self.data['date'], '%Y-%m-%d').date()
            self.data['start'] = start.time()
            self.data['end'] = end.time()
            self.data['date'] = date
            if date >= datetime.today().date():
                return self.data
            self.error_message = {
                'message': f"Appointment on {date} "
                f"not allow. Date must be: "
                f" (your date) >= {datetime.today().date()}"}

    def check_date_schedule(self, request, *args, **kwargs):
        """
        Method for checking the date of appointment
        """
        date = self.data['date']
        doctor = self.data['doctor']
        try:
            schedule = Schedule.objects.get(doctor_id=doctor, date=date)
            self.data['schedule'] = schedule
            return schedule
        except Schedule.DoesNotExist:
            doctor = Doctor.objects.filter(pk=doctor)
            self.error_message = {
                'message': f"Doctor {doctor[0].name} {doctor[0].last_name}"
                           f" dont work at {date}"
            }
        self.error_message = {'message': "Wrong date!"}

    def check_time(self, request, *args, **kwargs):
        """
        Method for checking appointment time
        """
        start = self.data['start']
        end = self.data['end']
        checked_time = []
        if self.data['schedule']:
            schedule = self.data['schedule']
            for time in [start, end]:
                if schedule.start < time < schedule.end:
                    if not schedule.lunch_start < time < schedule.lunch_end:
                        checked_time.append(time)
        if checked_time and start < end:
            return checked_time
        self.error_message = {'message': "Wrong time!"}

    def check_location(self, request, *args, **kwargs):
        """
        Method of checking the location of reception
        on the specified date and time
        """
        location = self.data['location']
        appointments = Appointment.objects.filter(
            location=location, date=self.data['date']
        )
        if appointments:
            appointments_time = appointments.values_list('start', 'end')
            appointments_time_list = [t for time in appointments_time for t in time]
            for appointment_time in appointments_time_list:
                if self.data['start'] <= appointment_time <= self.data['end']:
                    self.error_message = {
                        'message': "This time is already taken. "
                                   "Choose another time to make an appointment"}
                    return
        return location


class ListAppointmentsAPIView(ListAPIView, BaseAppointmentsAPIView):
    """
    A viewset class for viewing Appointments instances list.
    """
    permission_classes = (IsStaffReadOnly,)

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        today_date = datetime.today()
        self.queryset = self.get_queryset().exclude(date__lt=today_date)
        return self.list(request, *args, **kwargs)


class CreateAppointmentAPIView(CreateAPIView, CheckAppointmentData,
                               BaseAppointmentsAPIView):
    """
    A view class for validation POST.data before
    creating Appointment instance.
    """
    permission_classes = (IsAuthenticatedWriteOnly,)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        self.data = self.request.POST.dict()
        serializer = self.get_serializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            if self.validate_appointment_data(request):
                return self.create(request, *args, **kwargs)
        return Response(self.error_message)
