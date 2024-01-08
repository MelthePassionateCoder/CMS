from django.db import models
from django.urls import reverse
# Create your models here.

Gender_Choices = {
    "F": "Female",
    "M": "Male",
}

class Student(models.Model):
    lrn = models.CharField(max_length=20, unique=True)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    complete_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender_Choices, default='F')
    date_of_birth = models.DateField()
    birth_cert = models.BooleanField(default=False, verbose_name='Birth Certificate')
    attendance = models.IntegerField(default=0, verbose_name='Daily Attendance')
    
    def save(self, *args, **kwargs):
        self.complete_name = f"{self.firstname} {self.middlename} {self.lastname}".strip()

        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.complete_name

    
    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk':self.pk})