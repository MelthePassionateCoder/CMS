from django.contrib import admin
from .models import Subject, Semester, Grade, Quarter, CoreValue, BehaviorStatement, ObservedValue
# Register your models here.
admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(Quarter)
admin.site.register(Grade)
admin.site.register(CoreValue)
admin.site.register(BehaviorStatement)
admin.site.register(ObservedValue)