from django.contrib import admin
from doctors import models


@admin.register(models.Doctor)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'specialisation')
    list_display_links = ('name', 'last_name', 'specialisation')
