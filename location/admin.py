from django.contrib import admin

from location import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
