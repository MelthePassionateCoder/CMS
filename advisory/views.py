from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView,ListView, DetailView, FormView, UpdateView, DeleteView
from .models import Advisory
from attendance.models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
from .forms import AdvisoryForm, AddStudentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from attendance.models import DailyAttendance
from student.models import Student
from xhtml2pdf import pisa
from django.views import View
from django.db.models import Count, Sum
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
        
        student_info = {
            'student': student,
            'attendance_data': monthly_attendance_data,
            'total_days_present': total_days_present,
            'total_days_absent': total_days_absent,
            'school_months':school_month,
        }
        student_data.append(student_info)
    return render(request, 'advisory/report_card_template.html', {'advisory': advisory, 'students':student_data})
    # context = {'advisory': advisory, 'students': students, 'attendance_counts':attendance_counts}
    # return render(request, 'advisory/report_card_template.html', context)

    