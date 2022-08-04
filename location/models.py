from django.db import models


class Location(models.Model):
    name = models.PositiveIntegerField(help_text="Room number")

    def __str__(self):
        return f"Room number - {self.name}"
