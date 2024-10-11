from django.contrib import admin
from .models import PowerOutage

# Register your models here.
@admin.register(PowerOutage)
class PowerOutageAdmin(admin.ModelAdmin):
    list_display = ('area', 'state', 'affected_zone', 'date', 'start_time', 'end_time', 'slug', 'created_at', 'updated_at')