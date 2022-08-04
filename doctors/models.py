from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150, unique=True)
    specialisation = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.last_name} - {self.specialisation}"
