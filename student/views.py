from django.shortcuts import render, get_object_or_404
from django.views.generic import (UpdateView, 
                                CreateView,
                                DetailView, 
                                ListView)
from .models import Student
from django.urls import reverse_lazy
# Create your views here.
class StudentCreateView(CreateView):
    model = Student
    template_name = 'student/student_create.html'
    fields = ['lrn', 'firstname', 'middlename', 'lastname','gender', 'date_of_birth','birth_cert']
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        return super().form_valid(form)

class StudentListView(ListView):
    model = Student
    template_name = 'student/student_list.html' 
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.all()

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['lrn', 'firstname', 'middlename', 'lastname', 'date_of_birth','birth_cert']
    template_name = 'student/student_update.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Student, pk=self.kwargs['pk'])