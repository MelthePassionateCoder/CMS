from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, FormView
from .models import Section
from .forms import SectionForm, AddStudentForm
# Create your views here.

class SectionListView(ListView):
    model = Section
    template_name = 'activitymonitoring/section_list.html' 
    context_object_name = 'sections'

    def get_queryset(self):
        return Section.objects.all()

class SectionCreateView(CreateView):
    form_class = SectionForm
    template_name = 'activitymonitoring/section_create.html' 
    success_url = reverse_lazy('section-list') 

    def form_valid(self, form):
        form.instance.subject_teacher = self.request.user
        return super().form_valid(form)

class SectionDetailView(DetailView):
	model = Section
	template_name = 'activitymonitoring/section_detail.html'
	context_object_name = 'sections'

class AddStudentsToSectionView(FormView):
    template_name = 'activitymonitoring/add_students.html'
    form_class = AddStudentForm

    def get_success_url(self):
        return reverse('section-detail', kwargs={'pk': self.kwargs['section_id']})

    def form_valid(self, form):
        section = get_object_or_404(Section, pk=self.kwargs['section_id'])
        students = form.cleaned_data['students']
        section.students.add(*students)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_id'])
        return context