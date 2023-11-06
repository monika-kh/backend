from django.contrib import admin
from .models import *

admin.site.register(EmployeeAttendence)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ['city', 'technologies_familiar_with']