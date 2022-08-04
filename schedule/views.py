from datetime import datetime

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer
from clinic.settings import WEEK_DAYS


class DoctorScheduleAPIView(GenericAPIView):
    """
    A view for viewing Schedule instance.
    """

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    message = {'message': 'Wrong data'}
    filter_name = None
    today_date = datetime.today().date()

    def schedule_filter(self, *args, **kwargs):
        """
        The method of filtering the work schedule
        according to the specified parameters ('filter_name')
        """
        schedule = None
        if self.filter_name_validate():
            pk = self.kwargs.get('pk', '')
            field = self.kwargs.get(self.filter_name, '')
            if pk and field:
                if self.filter_name == 'day':
                    schedule = self.get_day_schedule()
                elif self.filter_name == 'date':
                    schedule = self.get_date_schedule()
            if not schedule:
                self.message = {'message': "Schedule Don't exist!"}
            self.queryset = schedule
            return schedule
        self.message = {'message': "Wrong pk or date/day-name!"}

    def get_day_schedule(self, *args, **kwargs):
        """
        Method for filtering the work schedule by day name
        !!! It is necessary to rewrite the method !!!
        """
        return None

    def get_date_schedule(self, *args, **kwargs):
        """
        Method for filtering the work schedule by date
        !!! It is necessary to rewrite the method !!!
        """
        return None

    def filter_name_validate(self, *args, **kwargs):
        """
        Method of validation the 'filter_name' by  which will be filtered
        !!! It is necessary to rewrite the method !!!
        """
        return


class DateDoctorScheduleView(RetrieveAPIView, DoctorScheduleAPIView):
    filter_name = 'date'

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if self.schedule_filter():
            return self.retrieve(request, *args, **kwargs)
        return Response(self.message)

    def get_date_schedule(self, **kwargs):
        """
        Method for filtering the work schedule by date
        """
        schedule = self.get_queryset().filter(
                doctor=self.kwargs['pk'], date=self.kwargs['date']
            ).exclude(date__lt=self.today_date)
        self.kwargs['pk'] = schedule[0].pk
        return schedule

    def filter_name_validate(self, *args, **kwargs):
        """
        Method of validation the 'filter_name' attr
        """
        date = self.kwargs[self.filter_name]
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            return date
        except ValueError:
            return


class DayDoctorScheduleView(ListAPIView, DoctorScheduleAPIView):
    filter_name = 'day'

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if self.schedule_filter():
            return self.list(request, *args, **kwargs)
        return Response(self.message)

    def get_day_schedule(self, **kwargs):
        """
        Method for filtering the work schedule by day name
        """
        schedule = self.get_queryset().filter(
                doctor=self.kwargs['pk'], day_name=self.kwargs['day']
            ).exclude(date__lt=self.today_date)[:4]
        return schedule

    def filter_name_validate(self, *args, **kwargs):
        """
        Method of validation the 'filter_name' attr
        """
        day_name = self.kwargs[self.filter_name].lower()
        if day_name in WEEK_DAYS:
            return day_name
