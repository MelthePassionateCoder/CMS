from django.shortcuts import render
from .models import Activity, Student_activity, SubjectEnrollment, Score

def add_activity(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    students = subject.student_set.all()
    activities = Activity.objects.filter(subject=subject)

    if request.method == 'POST':
        activity_name = request.POST['activity_name']
        category = request.POST['category']
        total_score = float(request.POST['total_score'])

        activity = Activity.objects.create(subject=subject, name=activity_name, category=category, totalScore=total_score)

        for student in students:
            score_value = float(request.POST.get(f'score_{student.id}', 0))
            Score.objects.create(student=student, activity=activity, score=score_value)

        return redirect('grades_view', subject_id=subject_id)

    return render(request, 'activitymoitoring/add_activity.html', {'subject': subject, 'students': students, 'activities': activities})