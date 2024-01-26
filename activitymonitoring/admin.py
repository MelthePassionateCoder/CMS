from django.contrib import admin
from .models import Activity, Student_activity, SubjectEnrollment, Score
# Register your models here.
admin.site.register(Activity)
admin.site.register(Student_activity)
admin.site.register(SubjectEnrollment)
admin.site.register(Score)