import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdvisorySelectionForm
from grades.models import Grade, Subject, Semester, ObservedValue, CoreValue, BehaviorStatement
from grades.forms import GradeImportForm, ObservedValueImportForm
from advisory.models import Advisory
from .models import ExportTemplate
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from attendance.models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
from io import BytesIO
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
def export_templates(request):
    if request.method == 'POST':
        form = AdvisorySelectionForm(request.POST)
        if form.is_valid():
            advisory_id = form.cleaned_data['advisory'].id
            template_type = form.cleaned_data['template_type']

            if template_type == 'observed_values':
                return generate_excel_template(request, advisory_id)
            elif template_type == 'grades':
                return generate_grade_excel_template(request, advisory_id)
            elif template_type == 'attendance':
                return generate_attendance_excel_template(request, advisory_id)
            elif template_type == 'monthly attendance':
                return generate_excel_template_monthly_attendance(request,advisory_id)
            elif template_type== 'manual monthly attendance':
                return generate_excel_template_manual_input(request, advisory_id)
            elif template_type== 'report card':
                return report_cards_page(request, advisory_id)
    else:
        form = AdvisorySelectionForm()

    return render(request, 'export_templates/advisory_selection.html', {'form': form})

def report_cards_page(request, advisory_id):
    advisory = get_object_or_404(Advisory, id=advisory_id)
    students = advisory.students.all()
    school_months = SchoolMonth.objects.filter(school_year=advisory.school_year, semester=1).order_by('month_order')
    total_school_days = sum(month.school_days for month in school_months)
    school_month = {'school_months':school_months,'total_school_days':total_school_days}
    student_data = []
    present_data = []
    days_absent = []
    total_days_present = 0
    total_days_absent = 0
    for student in students:
        student_attendance = MonthlyAttendanceManual.objects.filter(advisory=advisory, student=student)
        total_days_present = student_attendance.aggregate(total_days_present=Sum('days_present'))['total_days_present'] or 0
        total_days_absent = student_attendance.aggregate(total_days_absent=Sum('days_absent'))['total_days_absent'] or 0
        monthly_attendance_data = student_attendance.values('student__complete_name', 'month__month_name', 'days_present', 'days_absent')
        
        student_info = {
            'student': student,
            'attendance_data': monthly_attendance_data,
            'total_days_present': total_days_present,
            'total_days_absent': total_days_absent,
            'school_months':school_month,
        }
        student_data.append(student_info)
    return render(request, 'advisory/report_card_base.html', {'advisory': advisory, 'students':student_data})
   

def generate_excel_template(request, advisory_id):
    advisory = Advisory.objects.get(pk=advisory_id)
    students = advisory.students.all()
    core_values = CoreValue.objects.all()
    behavior_statements = BehaviorStatement.objects.all()

    data = []
    for student in students:
        for behavior_statement in behavior_statements:
            print(student,behavior_statement)
            row_data = {
                'LRN': student.lrn,
                'Name': student.complete_name,
                'Core Value': behavior_statement.core_value,
                'Behavior Statement': behavior_statement.statement,
                'Quarter': 1, 
                'Grade': '',
            }
            data.append(row_data)

    df = pd.DataFrame(data)

    excel_filename = f"observed_values_template_{advisory.section}.xlsx"
    df.to_excel(excel_filename, index=False)

    with open(excel_filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{excel_filename}"'
    
    return response

def generate_grade_excel_template(request, advisory_id):
    advisory = Advisory.objects.get(pk=advisory_id)
    students = advisory.students.all()

    data = []
    for student in students:
        row_data = {
            'LRN': student.lrn,
            'Name': student.complete_name,
            'Subject': '',
        }
        data.append(row_data)

    df = pd.DataFrame(data)

    excel_filename = f"grades_{advisory.section}.xlsx"
    df.to_excel(excel_filename, index=False)

    with open(excel_filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{excel_filename}"'
    
    return response

def generate_attendance_excel_template(request, advisory_id):
    advisory = Advisory.objects.get(pk=advisory_id)
    students = advisory.students.all()

    data = []
    for student in students:
        row_data = {
            'LRN': student.lrn,
            'Name': student.complete_name,
            'Morning In': '',
            'Morning Out': '',
            'Afternoon In': '',
            'Afternoon Out': '',
        }
        data.append(row_data)

    df = pd.DataFrame(data)

    excel_filename = f"attendance_{advisory.section}.xlsx"
    df.to_excel(excel_filename, index=False)

    with open(excel_filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{excel_filename}"'

    return response

def generate_excel_template_monthly_attendance(request, advisory_id):
    advisory = get_object_or_404(Advisory, id=advisory_id)
    students = advisory.students.all()

    unique_dates = DailyAttendance.objects.filter(advisory=advisory).values_list('date', flat=True).distinct()

    data = []
    monthly_attendance_list = []

    for student in students:
        students_attendance = DailyAttendance.objects.filter(
            advisory=advisory,
            student=student,
            day_status='Present'
        )
        students_absent = DailyAttendance.objects.filter(
            advisory=advisory,
            student=student,
            day_status='Absent'
        )
        monthly_present_days = students_attendance.values(
            'student__id',
            month=TruncMonth('date')
        ).annotate(present_days=Count('date', distinct=True))
        monthly_absent_days = students_absent.values(
            'student__id',
            month=TruncMonth('date')
        ).annotate(absent_days=Count('date', distinct=True))

        monthly_attendance_list.append({
            'student': student,
            'attendance_data': monthly_present_days,
            'attendance_absent': monthly_absent_days,
        })

    data = []

    for monthly_attendance in monthly_attendance_list:
        student = monthly_attendance['student']
        attendance_data = monthly_attendance['attendance_data']
        attendance_absent = monthly_attendance['attendance_absent']

        for entry in attendance_data:
            data.append({
                'Student Name': student.complete_name,
                'Month': entry['month'],
                'Days Present': entry['present_days'],
                'Days Absent': 0  
            })

        for entry in attendance_absent:
            data.append({
                'Student Name': student.complete_name,
                'Month': entry['month'],
                'Days Present': 0,  
                'Days Absent': entry['absent_days']
            })
        
    df = pd.DataFrame(data)

    
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance_template.xlsx'
    excel_file.seek(0)
    response.write(excel_file.read())

    return response

def generate_excel_template_manual_input(request, advisory_id):
    advisory = get_object_or_404(Advisory, id=advisory_id)
    students = advisory.students.all()
    school_months = SchoolMonth.objects.filter(school_year=advisory.school_year, semester=1).order_by('month_order')

    
    data = {'Advisory': [], 'Student': [], 'Month': [],'Days Present': [], 'Days Absent':[]}
    for student in students:
        for school_month in school_months:
            data['Advisory'].append(advisory.section)
            data['Student'].append(student.complete_name)
            data['Month'].append(school_month.month_name)
            data['Days Present'].append('')
            data['Days Absent'].append('')

    df = pd.DataFrame(data)

    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='ManualInputTemplate', index=False)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=manual_input_template.xlsx'
    excel_file.seek(0)
    response.write(excel_file.read())

    return response