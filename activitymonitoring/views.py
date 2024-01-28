from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, FormView
from .models import Section, Activity, Score
from .forms import SectionForm, AddStudentForm, ActivityForm, ScoreFormSet
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
    
def create_activity(request, section_id):
    section = Section.objects.get(pk=section_id)

    if request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.section = section
            activity.save()
            return redirect('enter_scores', section_id=section_id, activity_id=activity.id)
    else:
        activity_form = ActivityForm()

    return render(request, 'activitymonitoring/activity_create.html', {'section': section, 'activity_form': activity_form})

def enter_scores(request, section_id, activity_id):
    section = Section.objects.get(pk=section_id)
    activity = Activity.objects.get(pk=activity_id)

    students = section.students.all()

    if request.method == 'POST':
        formset = ScoreFormSet(request.POST, queryset=Score.objects.filter(activity=activity), students=students, section=section)
        if formset.is_valid():
            for form in formset:
                score = form.save(commit=False)
                score.activity = activity
                score.save()
            return redirect('section-detail', pk=section_id)
    else:
        formset = ScoreFormSet(queryset=Score.objects.filter(activity=activity), students=students, section=section)

    return render(request, 'activitymonitoring/scores_create.html', {'section': section, 'activity': activity, 'formset': formset})

def activity_list(request, section_id):
    section = Section.objects.get(pk=section_id)
    activities = Activity.objects.filter(section=section)

    return render(request, 'activitymonitoring/activity_list.html', {'section': section, 'activities': activities})

def activity_details(request, section_id, activity_id):
    section = Section.objects.get(pk=section_id)
    activity = Activity.objects.get(pk=activity_id)
    students = section.students.all()
    scores = Score.objects.filter(activity=activity)

    missed_students = students.exclude(pk__in=scores.values_list('student', flat=True))

    return render(request, 'activitymonitoring/activity_details.html', {'section': section, 'activity': activity, 'missed_students': missed_students})

def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    
    if request.method == 'POST':
        activity.delete()
        return redirect('activity-list', section_id=activity.section.id)

    return render(request, 'activitymonitoring/activity_delete.html', {'activity': activity})

def compute_grade(request, section_id):
    section = Section.objects.get(pk=section_id)
    students = section.students.all()
    subject = section.subject
    activity_types = ['Written Work', 'Performance Task', 'Quarterly Exam']

    grades = []

    for student in students:
        student_scores = Score.objects.filter(student=student,section=section)

        if student_scores:
            weighted_scores = []
            for activity_type in activity_types:
                activity_scores = student_scores.filter(activity__activity_type=activity_type)
                if activity_scores:
                    highest_possible_score = activity_scores.aggregate(Max('score'))['score__max']
                    learner_total_raw_score = sum(activity.score for activity in activity_scores)
                    percentage_score = (learner_total_raw_score / highest_possible_score) * 100

                    if subject.category == 'core':
                        if activity_type == 'Written Work':
                            weighted_score = percentage_score * 0.25
                        elif activity_type == 'Performance Task':
                            weighted_score = percentage_score * 0.50
                        elif activity_type == 'Quarterly Exam':
                            weighted_score = percentage_score * 0.25
                    

                    weighted_scores.append(weighted_score)

            initial_grade = sum(weighted_scores)
            grades.append({'student': student, 'grade': initial_grade})

    return render(request, 'activitymonitoring/compute_grade.html', {'section': section, 'subject': subject, 'grades': grades})