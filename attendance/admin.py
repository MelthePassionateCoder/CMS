from django.contrib import admin
from .models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
# Register your models here.
admin.site.register(DailyAttendance)
admin.site.register(SchoolMonth)
admin.site.register(MonthlyAttendanceManual)