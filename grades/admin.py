from django.contrib import admin
from .models import Subject, Semester, Grade, CoreValue, BehaviorStatement, ObservedValue
# Register your models here.
admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(Grade)
admin.site.register(CoreValue)
admin.site.register(BehaviorStatement)
admin.site.register(ObservedValue)