from django.contrib import admin

from appointment import models


@admin.register(models.Appointment)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'doctor', 'location', 'date', )
    list_display_links = ('first_name', 'last_name', 'doctor', 'location',)
