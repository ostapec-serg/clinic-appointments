from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import serializers

from appointment.models import Appointment
from schedule.models import Schedule


class AppointmentsSerializer(serializers.ModelSerializer):
    verification_data = None
    error_message = {}
    delta = timedelta(seconds=1)

    class Meta:
        model = Appointment
        fields = (
            'doctor',
            'first_name', 'last_name',
            'date', 'start', 'end',
        )

    def validate_appointment_data(self, *args, **kwargs):
        """Method for checking data for appointment"""
        if self.update_data_for_verification():
            if self.check_date_schedule():
                return self.verification_data

    def update_data_for_verification(self, *args, **kwargs):
        """
        Method for updating the 'self.data' attribute
        that will be used to check the appointment
        """
        self.verification_data = self.data
        start = datetime.strptime(self.data['start'],
                                  "%H:%M:%S") + self.delta
        end = datetime.strptime(self.data['end'],
                                "%H:%M:%S") - self.delta
        date = datetime.strptime(self.data['date'],
                                 '%Y-%m-%d').date()
        today = datetime.today().date()
        self.verification_data['start'] = start.time()
        self.verification_data['end'] = end.time()
        self.verification_data['date'] = date

        if date >= today and start < end:
            return self.verification_data
        self.error_message = {
            'message': f"Appointment on {date} "
            f"not allow. Date must be: "
            f" (your date) >= {datetime.today().date()}. "
                       f"time start < time end"}

    def check_date_schedule(self, *args, **kwargs):
        """Method for checking the date_schedule of appointment"""
        date = self.verification_data['date']
        doctor = self.verification_data['doctor']
        start = self.verification_data['start']
        end = self.verification_data['end']
        schedule = Schedule.objects.filter(
            doctor_id=doctor, date=date,
            start__lte=start, end__gte=end
            ).exclude(Q(break_start__lte=start) & Q(break_end__gte=start) |
                      Q(break_start__lte=end) & Q(break_end__gte=end))

        if schedule.exists():
            return self.check_time()
        self.error_message = {
            'message': f"Schedule dont exist. "
                       f"Check appointment date and time!"}

    def check_time(self, *args, **kwargs):
        """Method for checking appointment time"""
        start = self.verification_data['start']
        end = self.verification_data['end']
        appointments = Appointment.objects.filter(
            date=self.data['date'], doctor_id=self.data['doctor']
        ).values_list('start', 'end')
        for time in appointments:
            if time[0] < start < time[1] or start < (time[0] or time[1]) < end:
                self.error_message = {
                    'message': "This time is already taken. "
                    "Choose another time to make an appointment"
                }
                return
        return self.data
