from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, FormView
from .models import Section, Activity, Score
from .forms import SectionForm, AddStudentForm, ActivityForm, BaseScoreFormSet
from decimal import Decimal
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
    ScoreFormSet = BaseScoreFormSet
    if request.method == 'POST':
        formset = ScoreFormSet(request.POST, queryset=Score.objects.filter(activity=activity, section=section),students=students)
        
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                student = instance.student
                score_value = instance.score
                existing_score = Score.objects.filter(activity=activity, section=section, student=student).first()

                if existing_score:
                    existing_score.score = score_value
                    existing_score.save()
                else:
                    instance.section = section
                    instance.activity = activity
                    instance.save()
            return redirect('section-detail', pk=section_id)
    else:
        formset = ScoreFormSet(queryset=Score.objects.filter(activity=activity, section=section),students=students)

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
    student_scores = {}
    for student in students:
        scores_ = Score.objects.filter(activity=activity, student=student).first()
        if scores_:
            student_scores[student] = scores_.score
    return render(request, 'activitymonitoring/activity_details.html', {'section': section, 'activity': activity, 'missed_students': missed_students,'student_scores': student_scores})

def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    
    if request.method == 'POST':
        activity.delete()
        return redirect('activity-list', section_id=activity.section.id)

    return render(request, 'activitymonitoring/activity_delete.html', {'activity': activity})

def get_percentage(score,totalScore):
    return (Decimal(score)/Decimal(totalScore))*100

def get_weight_component(scores, subject_type):
    if subject_type == "core":
        ww_weight, pt_weight, qe_weight = 0.25, 0.50, 0.25
    else:
        ww_weight, pt_weight, qe_weight = 0.20, 0.60, 0.20

    weighted_scores = {
        'WW': Decimal(Decimal(scores['WW']) * Decimal(ww_weight)),
        'PT': Decimal(Decimal(scores['PT']) * Decimal(pt_weight)),
        'QE': Decimal(Decimal(scores['QE']) * Decimal(qe_weight))
    }
    
    total_weighted_score = sum(weighted_scores.values())
    
    return total_weighted_score

def transmute_grade(initial_grade):
    transmutation_table = {
        (100, 100): 100,
        (98.40, 99.99): 99,
        (96.80, 96.79): 97,
        (93.60, 95.19): 96,
        (92, 93.59): 95,
        (90.40, 91.99): 94,
        (88.80, 90.30): 93,
        (87.20, 88.79): 92,
        (85.60, 87.19): 91,
        (84, 85.59): 90,
        (82.40, 83.99): 89,
        (80.80, 82.39): 88,

        (79.20, 80.79): 87,
        (77.60, 79.19): 86,

        (36.00, 39.99): 69,

        (12.00, 15.99): 63,
        (8.00, 11.99): 62,
        (4.00, 7.99): 61,
        (0, 3.99): 60,
    }

    # Check which range the initial grade falls into
    for grade_range, final_grade in transmutation_table.items():
        if grade_range[0] <= initial_grade <= grade_range[1]:
            return final_grade
    
def compute_grade(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    students = section.students.all()
    activities = Activity.objects.filter(section__id=section_id)
    # section= get_object_or_404(Section, id=section_id)
    # students = section.students.all()
    activity_totalScore = {'WW':0,'PT':0,'QE':0}
    student_activity_scores = {}
    for student in students:
        scores = Score.objects.filter(student=student, section_id=section_id)
        for score in scores:
            student_name = student.complete_name
            activity_type = score.activity.activity_type
            if student_name not in student_activity_scores:
                student_activity_scores[student_name] = {'WW': 0, 'PT': 0, 'QE': 0}
            if activity_type == 'WW':
                student_activity_scores[student_name]['WW'] += Decimal(score.score)
            elif activity_type == 'PT':
                student_activity_scores[student_name]['PT'] += Decimal(score.score)
            elif activity_type == 'QE':
                student_activity_scores[student_name]['QE'] += Decimal(score.score)
    
    for activity in activities:
        activity_type = activity.activity_type
        activity_totalScore[activity_type] += Decimal(activity.totalScore)
    
    for student_name, scores in student_activity_scores.items():
        for activity_type in scores:
            if activity_totalScore[activity_type] != 0:
                scores[activity_type] /= Decimal(activity_totalScore[activity_type])
                scores[activity_type] *= 100
    context_list = []
    for student_name, scores in student_activity_scores.items():
        weight_score = get_weight_component(scores, section.subject.category)
        final_grade = transmute_grade(weight_score)
        context = {
            'student': student_name,
            'ww': scores['WW'],
            'pt': scores['PT'],
            'qe': scores['QE'],
            'initial_grade': weight_score,
            'final_grade': final_grade
        }
        context_list.append(context)
        
    return render(request, 'activitymonitoring/compute_grade.html', {'context_list': context_list})
    # for student_id, activity_scores in student_activity_scores.items():
    #     print(f"Student ID: {student_name}")
    #     print(f"Sum of Written Work (WW) Scores: {activity_scores['WW']}")
    #     print(f"Sum of Performance Task (PT) Scores: {activity_scores['PT']}")
    #     print(f"Sum of Quarterly Exam (QE) Scores: {activity_scores['QE']}")
    #     print("\n")
    #print(f"\n\n\n{students_}\n\n")
    

    