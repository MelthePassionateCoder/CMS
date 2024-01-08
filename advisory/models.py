from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from django.urls import reverse
# Create your models here.
School_Year_Choices = {
    "2023": "2023-2024",
    "2024": "2024-2025",
    "2025": "2025-2026",
}
Track = {
    "TVL": "TVL",
}
Strand = {
    "ICT": "ICT",
}

class Advisory(models.Model):
    school_year = models.CharField(max_length=10, choices=School_Year_Choices, default='2023')
    section = models.CharField(max_length=20, null=True)
    track = models.CharField(max_length=10, choices=Track, default='TVL')
    strand = models.CharField(max_length=10, choices=Strand, default='ICT')
    adviser = models.ForeignKey(User, on_delete=models.CASCADE)
    principal_name = models.CharField(max_length=20, null=True)
    students = models.ManyToManyField(Student)
    

    def get_absolute_url(self):
        return reverse('advisory-detail', kwargs={'pk':self.pk})
    
    def __str__(self):
        return f"{self.section} - {self.school_year} - {self.adviser}"


    