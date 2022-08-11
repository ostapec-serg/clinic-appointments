import calendar
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from doctors.models import Doctor
from location.models import Location


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='schedule', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_DEFAULT, default=1)
    date = models.DateField(null=True)
    day_name = models.CharField(max_length=10, auto_created=True, editable=False)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.last_name} - {self.day_name} - {self.date}"

    def save(self, *args, **kwargs):
        """Auto save day_name"""
        self.day_name = self.get_day_name().lower()
        super(Schedule, self).save(*args, **kwargs)

    def clean(self):
        """
        A method for checking the start and end of a work schedule.
        """
        if self.date < datetime.today().date():
            raise ValidationError({'date': _("Wrong date!")})
        delta = timedelta(seconds=1)
        start = (datetime.combine(self.date, self.start) + delta).time()
        end = (datetime.combine(self.date, self.end) - delta).time()

        #  checking free time in the specified location
        message = _(f"The time of the new schedule overlaps with the"
                    f" already existing schedule(s).")
        location_schedules = Schedule.objects.filter(
            date=self.date, location_id=self.location
        ).values_list('start', 'end')
        for time in location_schedules:
            if time[0] < start < time[1] or start < (time[0] or time[1]) < end:
                raise ValidationError({'start': message, 'end': message}, )

        #  checking the working schedule of the specified doctor
        doctor_schedules = Schedule.objects.filter(
            doctor_id=self.doctor, date=self.date,
        ).values_list('start', 'end')
        for time in doctor_schedules:
            if time[0] < start < time[1] or start < (time[0] or time[1]) < end:
                raise ValidationError(_(
                    f"Doctor {self.doctor.name} {self.doctor.last_name} works"
                    f" in office №{self.location.name} in the specified time!"
                    f" Choose another time"
                ))

    def get_day_name(self):
        return calendar.day_name[self.date.weekday()]
