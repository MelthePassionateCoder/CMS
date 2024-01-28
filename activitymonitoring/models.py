# from django.db import models
# from django.utils import timezone
# from student.models import Student
# from grades.models import Subject
# # Create your models here.
# class Activity(models.Model):
#     CATEGORY_CHOICES = [
#         ('WW', 'Written Work'),
#         ('PT', 'Performance Task'),
#         ('QE', 'Quarter Exam'),
#     ]

#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     totalScore = models.FloatField()
#     deadline = models.DateField()
#     created = models.DateTimeField(default=timezone.now)

# class Student_activity(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     subjects = models.ManyToManyField(Subject, through='SubjectEnrollment')

# class SubjectEnrollment(models.Model):
#     student = models.ForeignKey(Student_activity, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

# class Score(models.Model):
#     student = models.ForeignKey(Student_activity, on_delete=models.CASCADE)
#     activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
#     score = models.FloatField()

from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from grades.models import Subject
from django.urls import reverse
from django.utils import timezone
# Create your models here.
School_Year_Choices = {
    "2023": "2023-2024",
    "2024": "2024-2025",
    "2025": "2025-2026",
}

class Section(models.Model):
    school_year = models.CharField(max_length=10, choices=School_Year_Choices, default='2023')
    section = models.CharField(max_length=20, null=True)
    students = models.ManyToManyField(Student)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    # def get_absolute_url(self):
    #     return reverse('advisory-detail', kwargs={'pk':self.pk})
    
    def __str__(self):
        return f"{self.subject} - {self.school_year} - {self.section}"


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('WW', 'Written Work'),
        ('PT', 'Performance Task'),
        ('QE', 'Quarter Exam'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=2, choices=ACTIVITY_TYPES)
    name = models.CharField(max_length=50)
    totalScore = models.FloatField()
    deadline = models.DateField()
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=200,null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_activity_type_display()}"

class Score(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.activity} - {self.score}"