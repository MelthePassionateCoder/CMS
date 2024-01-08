from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AttendanceUploadForm, SchoolMonthForm, ManualAttendanceForm, MonthlyAttendanceManualUploadForm
from .utils import process_attendance_file
from advisory.models import Advisory
from .models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
from student.models import Student
from django.db.utils import IntegrityError
import pandas as pd
class AttendanceUploadView(View):
    template_name = 'attendance/upload_attendance.html'

    def get(self, request, advisory_id):
        advisory = Advisory.objects.get(id=advisory_id)
        form = AttendanceUploadForm(initial={'advisory': advisory})
        return render(request, self.template_name, {'form': form, 'advisory': advisory})

    def post(self, request, advisory_id):
        advisory = Advisory.objects.get(id=advisory_id)
        form = AttendanceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            date = form.cleaned_data['date']
            file = request.FILES['file']

            success, message = process_attendance_file(file, advisory_id, date)

            if success:
                return redirect('success_page')
            else:
                return render(request, self.template_name, {'form': form, 'advisory': advisory, 'error_message': message})

        return render(request, self.template_name, {'form': form, 'advisory': advisory})

def success_page(request):
    return render(request, 'attendance/success_page.html')


def attendance_list(request, advisory_id):
    advisory = get_object_or_404(Advisory, id=advisory_id)
    students_attendance = DailyAttendance.objects.filter(advisory=advisory)

    student_name_filter = request.GET.get('student_name_filter', None)
    student = advisory.students.all().filter(lrn=student_name_filter).first()
    if student_name_filter:
        students_attendance = DailyAttendance.objects.filter(student=student)

    return render(request, 'attendance/attendance_list.html', {'advisory': advisory, 'students_attendance': students_attendance})

def school_month_list(request):
    school_months = SchoolMonth.objects.all().order_by('month_order')
    return render(request, 'attendance/academic_calendar.html', {'school_months': school_months})

def add_school_month(request):
    if request.method == 'POST':
        form = SchoolMonthForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('school_month_list')
            except IntegrityError:
                form.add_error(None, 'A SchoolMonth with this school year and month already exists.')
    else:
        form = SchoolMonthForm()
    return render(request, 'attendance/academic_calendar.html', {'form': form, 'action': 'Add'})

def edit_school_month(request, month_id):
    school_month = get_object_or_404(SchoolMonth, pk=month_id)

    if request.method == 'POST':
        form = SchoolMonthForm(request.POST, instance=school_month)
        if form.is_valid():
            updated_school_month = form.save(commit=False)
            updated_school_month.school_month_field = f"{updated_school_month.school_year}-{updated_school_month.month}"

            existing_instance = SchoolMonth.objects.exclude(id=month_id).filter(
                school_month_field=updated_school_month.school_month_field
            ).first()

            if existing_instance:
                existing_instance.school_days = updated_school_month.school_days
                existing_instance.save()

                return redirect('school_month_list')

            updated_school_month.save()

            return redirect('school_month_list')
    else:
        form = SchoolMonthForm(instance=school_month)

    return render(request, 'attendance/academic_calendar.html', {'form': form, 'action': 'Edit'})

def delete_school_month(request, month_id):
    school_month = get_object_or_404(SchoolMonth, pk=month_id)

    if request.method == 'POST':
        school_month.delete()
        return redirect('school_month_list')

    return render(request, 'attendance/delete_school_month_confirm.html', {'school_month': school_month})

def upload_manual_input(request, advisory_id):
    advisory = get_object_or_404(Advisory, id=advisory_id)
    if request.method == 'POST':
        form = MonthlyAttendanceManualUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, sheet_name='ManualInputTemplate')

            for index, row in df.iterrows():
                student_name = row['Student']
                month_name = row['Month']
                days_present = row['Days Present']
                days_absent = row['Days Absent']

                student = Student.objects.get(complete_name=student_name)
                month = SchoolMonth.objects.get(month_name=month_name)

                existing_entry = MonthlyAttendanceManual.objects.filter(
                    advisory=advisory,
                    student=student,
                    month=month
                ).first()

                if existing_entry:
                    existing_entry.days_present = days_present
                    existing_entry.days_absent = days_absent
                    existing_entry.save()
                else:
                    MonthlyAttendanceManual.objects.create(
                        advisory=advisory,
                        student=student,
                        month=month,
                        days_present=days_present,
                        days_absent=days_absent
                    )

            return redirect('success_page')
    else:
        form = MonthlyAttendanceManualUploadForm()

    return render(request, 'attendance/input_attendance.html', {'form': form})