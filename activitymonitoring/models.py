from django.db import models
from django.utils import timezone
from student.models import Student
from grades.models import Subject
# Create your models here.
class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('written_work', 'Written Work'),
        ('performance_task', 'Performance Task'),
        ('quarter_exam', 'Quarter Exam'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    totalScore = models.FloatField()
    deadline = models.DateField()
    created = models.DateTimeField(default=timezone.now)

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    score = models.FloatField()
