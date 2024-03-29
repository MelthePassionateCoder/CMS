# Generated by Django 5.0 on 2024-01-21 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advisory', '0002_advisory_principal_name_advisory_track'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoreValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1', '1st Quarter'), ('2', '2nd Quarter'), ('3', '3rd Quarter'), ('4', '4th Quarter')], default='1', max_length=10)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], default='1', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('category', models.CharField(choices=[('core', 'Core'), ('applied', 'Applied'), ('specialized', 'Specialized')], default='core', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
                ('core_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.corevalue')),
            ],
        ),
        migrations.CreateModel(
            name='ObservedValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisory.advisory')),
                ('behavior_statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.behaviorstatement')),
                ('core_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.corevalue')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('quarter', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='grades.quarter')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('advisory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisory.advisory')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('quarter', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='grades.quarter')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.subject')),
            ],
        ),
    ]
