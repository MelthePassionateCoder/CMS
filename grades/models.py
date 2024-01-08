from django.db import models
from advisory.models import Advisory
from student.models import Student

class Subject(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.name

class Semester(models.Model):
    Semester_Choices = [
        ('1', 'First Semester'),
        ('2', 'Second Semester')
    ]
    name = models.CharField(max_length=10, choices=Semester_Choices, default="1")

    def __str__(self):
        return self.name

class Quarter(models.Model):
    Quarter_Choices = [
        ('1', '1st Quarter'),
        ('2', '2nd Quarter'),
        ('3', '3rd Quarter'),
        ('4', '4th Quarter'),
    ]
    name = models.CharField(max_length=10, choices=Quarter_Choices, default="1")
    order = models.IntegerField()

    def __str__(self):
        return self.name
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, default="1")
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.complete_name} - {self.subject} - {self.semester}"

class CoreValue(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BehaviorStatement(models.Model):
    core_value = models.ForeignKey(CoreValue, on_delete=models.CASCADE)
    statement = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.core_value.name} - {self.statement}"

class ObservedValue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)
    core_value = models.ForeignKey(CoreValue, on_delete=models.CASCADE)
    behavior_statement = models.ForeignKey(BehaviorStatement, on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, default="1")
    grade = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])

    def __str__(self):
        return f"{self.student.complete_name} - {self.core_value.name} - {self.behavior_statement.statement} - Quarter {self.quarter}"