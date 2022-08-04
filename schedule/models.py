import calendar
from django.db import models

from doctors.models import Doctor


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='schedule', on_delete=models.CASCADE)
    date = models.DateField(null=True)
    day_name = models.CharField(max_length=10, auto_created=True, editable=False)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    lunch_start = models.TimeField(null=True)
    lunch_end = models.TimeField(null=True)

    def __str__(self):
        return f"{self.doctor.last_name} - {self.day_name} - {self.date}"

    def save(self, *args, **kwargs):
        """Auto save day_name"""
        self.day_name = self.day_of_week().lower()
        super(Schedule, self).save(*args, **kwargs)

    def day_of_week(self):
        return calendar.day_name[self.date.weekday()]


