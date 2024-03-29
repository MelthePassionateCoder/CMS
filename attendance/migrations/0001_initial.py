# Generated by Django 5.0 on 2023-12-31 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advisory', '0001_initial'),
        ('student', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_year', models.CharField(choices=[('2023', '2023-2024'), ('2024', '2024-2025'), ('2025', '2025-2026'), ('2026', '2026-2027')], max_length=15)),
                ('semester', models.PositiveIntegerField()),
                ('month', models.CharField(max_length=15)),
                ('month_name', models.CharField(max_length=15)),
                ('month_order', models.PositiveIntegerField()),
                ('school_days', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('morning_in_status', models.CharField(blank=True, choices=[('Present', 'Present'), ('Tardy', 'Tardy'), ('Absent', 'Absent')], max_length=10, null=True)),
                ('morning_out_status', models.CharField(blank=True, choices=[('Present', 'Present'), ('Tardy', 'Tardy'), ('Absent', 'Absent')], max_length=10, null=True)),
                ('afternoon_in_status', models.CharField(blank=True, choices=[('Present', 'Present'), ('Tardy', 'Tardy'), ('Absent', 'Absent')], max_length=10, null=True)),
                ('afternoon_out_status', models.CharField(blank=True, choices=[('Present', 'Present'), ('Tardy', 'Tardy'), ('Absent', 'Absent')], max_length=10, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/excel_files/')),
                ('day_status', models.CharField(blank=True, choices=[('Present', 'Present'), ('Tardy', 'Tardy'), ('Absent', 'Absent')], max_length=10, null=True)),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisory.advisory')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyAttendanceManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_present', models.IntegerField()),
                ('days_absent', models.IntegerField()),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisory.advisory')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.schoolmonth')),
            ],
        ),
    ]
