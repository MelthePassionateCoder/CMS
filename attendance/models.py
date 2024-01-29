from django.db import models
from student.models import Student
from advisory.models import Advisory
from django.utils import timezone

class DailyAttendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Tardy', 'Tardy'),
        ('Absent', 'Absent'),
    ]

    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    morning_in_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    morning_out_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    afternoon_in_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    afternoon_out_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    file = models.FileField(upload_to='uploads/excel_files/', null=True, blank=True)
    day_status = models.CharField(max_length=10, blank=True, null=True)

    def clean(self):
        status_choices = [choice[0] for choice in self.STATUS_CHOICES]

        for field in ['morning_in_status', 'morning_out_status', 'afternoon_in_status', 'afternoon_out_status']:
            status = getattr(self, field)
            if status and status not in status_choices:
                raise ValidationError(f"Invalid status '{status}' for field '{field}'")

    def save(self, *args, **kwargs):
        all_present = all(
            field == 'Present' for field in [self.morning_in_status, self.morning_out_status, self.afternoon_in_status, self.afternoon_out_status]
        )

        morning_late = self.morning_in_status == 'Absent' and self.morning_out_status == 'Present'

        cutting_class = (
            self.morning_in_status == self.morning_out_status == 'Present'
            and self.afternoon_in_status == self.afternoon_out_status == 'Absent'
        )

        if all_present:
            self.day_status = 'Present'
        # elif morning_late:
        #     self.day_status = 'Late'
        # elif cutting_class:
        #     self.day_status = 'Cutting class'
        else:
            self.day_status = 'Absent'

        super().save(*args, **kwargs)

class SchoolMonth(models.Model):
    SCHOOL_YEAR_CHOICES = [
        ('2023', '2023-2024'),
        ('2024', '2024-2025'),
        ('2025', '2025-2026'),
        ('2026', '2026-2027'),
    ]

    school_year = models.CharField(max_length=15, choices=SCHOOL_YEAR_CHOICES)
    semester = models.PositiveIntegerField()
    month = models.CharField(max_length=15)
    month_name = models.CharField(max_length=15)
    month_order = models.PositiveIntegerField()
    school_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.semester} - {self.month_name} - {self.school_year}"

class MonthlyAttendanceManual(models.Model):
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.ForeignKey(SchoolMonth, on_delete=models.CASCADE)
    days_present = models.IntegerField()
    days_absent = models.IntegerField()