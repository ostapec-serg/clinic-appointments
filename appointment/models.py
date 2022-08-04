from django.contrib.auth.models import User
from django.db import models

from doctors.models import Doctor
from location.models import Location


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='appointment', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.SET_DEFAULT, default=None)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start} - {self.end}"
