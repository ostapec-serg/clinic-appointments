from django_filters import rest_framework as drf_filter

from appointment.models import Appointment


class AppointmentsFilter(drf_filter.FilterSet):
    date = drf_filter.DateFilter(field_name='date')

    class Meta:
        model = Appointment
        fields = [
            'date'
        ]
        
