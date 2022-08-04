from django.contrib import admin

from schedule import models


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date')
    list_display_links = ('doctor', 'date')
