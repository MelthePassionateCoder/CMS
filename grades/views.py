import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Grade, Subject, Semester, ObservedValue, CoreValue, BehaviorStatement
from .forms import GradeImportForm, ObservedValueImportForm
from advisory.models import Advisory

def input_grades(request, advisory_id):
    advisory = Advisory.objects.get(pk=advisory_id)

    if request.method == 'POST':
        form = GradeImportForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            semester = form.cleaned_data['semester']
            quarter = form.cleaned_data['quarter']
            excel_file = request.FILES['excel_file']

            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                lrn_column_name = 'LRN'
                lrn = row[lrn_column_name]
                student = advisory.students.filter(lrn=lrn).first()

                if student:
                    value = row[subject.name]
                    existing_grade = Grade.objects.filter(
                        student=student,
                        advisory=advisory,
                        subject=subject,
                        semester=semester,
                        quarter=quarter
                    ).first()

                    if existing_grade:
                        existing_grade.value = float(value)
                        existing_grade.save()
                    else:
                        Grade.objects.create(
                            student=student,
                            advisory=advisory,
                            subject=subject,
                            semester=semester,
                            quarter=quarter,
                            value=float(value)
                        )

            return redirect('success_page')
    else:
        form = GradeImportForm()

    return render(request, 'grades/grade_input.html', {'form': form, 'advisory': advisory})

def input_observed_values(request, advisory_id):
    advisory = Advisory.objects.get(pk=advisory_id)

    if request.method == 'POST':
        if 'manual_input' in request.POST:
            form = ObservedValueForm(request.POST)
            if form.is_valid():
                observed_value = form.save(commit=False)
                observed_value.student = advisory.students.filter(lrn=form.cleaned_data['lrn']).first()
                observed_value.advisory = advisory
                observed_value.save()
        elif 'excel_input' in request.POST:
            form = ObservedValueImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    lrn = row['LRN']
                    complete_name = row['Name']
                    student = advisory.students.filter(lrn=lrn).first()
                    core_value = row['Core Value']
                    behavior_statement = row['Behavior Statement']
                    quarter = row['Quarter']
                    grade = row['Grade']
                    observed_value = ObservedValue.objects.create(
                        student=student,
                        advisory=advisory,
                        core_value=core_value,
                        behavior_statement=behavior_statement,
                        quarter=quarter,
                        grade=grade
                    )
                return redirect('success_page') 
        else:
            form = ObservedValueImportForm()
    else:
        form = ObservedValueImportForm()

    observed_values = ObservedValue.objects.filter(advisory=advisory)

    return render(request, 'grades/input_observed_values.html', {'form': form, 'advisory': advisory, 'observed_values': observed_values})

