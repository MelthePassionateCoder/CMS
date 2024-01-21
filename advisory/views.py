from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView,ListView, DetailView, FormView, UpdateView, DeleteView
from .models import Advisory
from attendance.models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
from grades.models import Subject, Grade, ObservedValue
from .forms import AdvisoryForm, AddStudentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from attendance.models import DailyAttendance
from student.models import Student
from xhtml2pdf import pisa
from django.views import View
from django.db.models import Count, Sum, Case, When, DecimalField
from django.db.models.functions import TruncMonth
# Create your views here.
class AdvisoryCreateView(CreateView):
    model = Advisory
    form_class = AdvisoryForm
    template_name = 'advisory/advisory_create.html' 
    success_url = reverse_lazy('advisory-list') 

    def form_valid(self, form):
        form.instance.adviser = self.request.user
        return super().form_valid(form)

class AdvisoryListView(ListView):
    model = Advisory
    template_name = 'advisory/advisory_list.html' 
    context_object_name = 'advisories'

    def get_queryset(self):
        return Advisory.objects.all()

class AdvisoryDetailView(DetailView):
	model = Advisory
	template_name = 'advisory/advisory_detail.html'
	context_object_name = 'advisory'

class AddStudentsToAdvisoryView(FormView):
    template_name = 'advisory/add_students.html'
    form_class = AddStudentForm

    def get_success_url(self):
        return reverse('advisory-detail', kwargs={'pk': self.kwargs['advisory_id']})

    def form_valid(self, form):
        advisory = get_object_or_404(Advisory, pk=self.kwargs['advisory_id'])
        students = form.cleaned_data['students']
        advisory.students.add(*students)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advisory'] = get_object_or_404(Advisory, pk=self.kwargs['advisory_id'])
        return context

class AdvisoryUpdateView(UpdateView):
    model = Advisory
    form_class = AdvisoryForm
    template_name = 'advisory/advisory_update.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Advisory, pk=self.kwargs['pk'])

class AdvisoryDeleteView(DeleteView):
    model = Advisory
    template_name = 'advisory/advisory_delete.html'
    success_url = reverse_lazy('advisory-list') 

    def get_object(self, queryset=None):
        return get_object_or_404(Advisory, pk=self.kwargs['pk'])

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
        grades = Grade.objects.filter(advisory__id=advisory_id, student__complete_name=student)
        first_semester_data = Grade.objects.filter(student=student, advisory=advisory, semester__name='1').order_by('subject__order')
        first_semester_q1_q2_data = first_semester_data.filter(quarter__name__in=['1', '2'])
        
        second_semester_data = Grade.objects.filter(student=student, advisory=advisory,semester__name='2').order_by('subject__order')
        second_semester_q3_q4_data = second_semester_data.filter(quarter__name__in=['3', '4'])
        
        grouped_first_semester_data = {}
        for grade in first_semester_q1_q2_data:
            subject_name = grade.subject.name
            if subject_name not in grouped_first_semester_data:
                grouped_first_semester_data[subject_name] = {'q1': None, 'q2': None,'semester_final': None, 'remarks': None, 'cat': grade.subject.category}
            if grade.quarter.name == '1':
                grouped_first_semester_data[subject_name]['q1'] = round(grade.value)
            elif grade.quarter.name == '2':
                grouped_first_semester_data[subject_name]['q2'] = round(grade.value)
        
        grouped_second_semester_data = {}
        for grade in second_semester_q3_q4_data:
            subject_name = grade.subject.name
            if subject_name not in grouped_second_semester_data:
                grouped_second_semester_data[subject_name] = {'q3': None, 'q4': None, 'semester_final': None, 'remarks': None,'cat':grade.subject.category}
            if grade.quarter.name == '3':
                grouped_second_semester_data[subject_name]['q3'] = grade.value
            elif grade.quarter.name == '4':
                grouped_second_semester_data[subject_name]['q4'] = grade.value
        
        for grades in grouped_first_semester_data.values():
            grades['semester_final'] = calculate_semester_final_grade([grades['q1'], grades['q2']])
            grades['remarks'] = determine_remarks(grades['semester_final'])
        
        for grades in grouped_second_semester_data.values():
            grades['semester_final'] = calculate_semester_final_grade([grades['q3'], grades['q4']])
            grades['remarks'] = determine_remarks(grades['semester_final'])

        observed_values = ObservedValue.objects.filter(advisory=advisory, student=student).order_by('behavior_statement__order')
        
        grouped_data_observed_values = {}
        for value in observed_values:
            core_value = value.core_value
            behavior_statement = value.behavior_statement
            quarter = value.quarter
            grade = value.grade

            key = (core_value, behavior_statement)
            if key not in grouped_data_observed_values:
                grouped_data_observed_values[key] = {'quarter_1': None, 'quarter_2': None, 'quarter_3': None, 'quarter_4': None}
            if quarter == '1':
                grouped_data_observed_values[key]['quarter_1'] = grade
            elif quarter == '2':
                grouped_data_observed_values[key]['quarter_2'] = grade
            elif quarter == '3':
                grouped_data_observed_values[key]['quarter_3'] = grade
            elif quarter == '4':
                grouped_data_observed_values[key]['quarter_4'] = grade
        
        student_info = {
            'student': student,
            'attendance_data': monthly_attendance_data,
            'total_days_present': total_days_present,
            'total_days_absent': total_days_absent,
            'school_months':school_month,
            'grouped_first_semester_data': grouped_first_semester_data,
            'grouped_second_semester_data': grouped_second_semester_data,
            'grouped_data_observed_values': grouped_data_observed_values
            
        }
        student_data.append(student_info)
        print(f"\n\n\n{grouped_data_observed_values}\n\n\n")
    return render(request, 'advisory/report_card_template.html', {'advisory': advisory, 'students':student_data})
    # context = {'advisory': advisory, 'students': students, 'attendance_counts':attendance_counts}
    # return render(request, 'advisory/report_card_template.html', context)


def calculate_semester_final_grade(grades):
    total = 0
    count = 0
    for grade in grades:
        if grade:
            total += grade
            count += 1
    average = total / count if count > 0 else None
    return round(average) if average is not None else None

def determine_remarks(semester_final_grade):
    return 'Passed' if semester_final_grade is not None and semester_final_grade >= 75 else 'Failed'