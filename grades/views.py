import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Grade, Subject, Semester, ObservedValue, CoreValue, BehaviorStatement, Quarter
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
            form = ObservedValueImportForm(request.POST)
            if form.is_valid():
                observed_value = form.save(commit=False)
                observed_value.student = advisory.students.filter(lrn=form.cleaned_data['lrn']).first()
                core_value_name = form.cleaned_data['core_value']
                core_value, _ = CoreValue.objects.get_or_create(name=core_value_name)
                observed_value.core_value = core_value
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
                    core_value_name = row['Core Value']
                    core_value, _ = CoreValue.objects.get_or_create(name=core_value_name)
                    behavior_statement_name = row['Behavior Statement']
                    behavior_statement, _ = BehaviorStatement.objects.get_or_create(
                                                                        core_value=core_value,
                                                                        statement=behavior_statement_name)
                    quarter_name = row['Quarter']
                    quarter, _ =Quarter.objects.get_or_create(name=quarter_name)
                    grade = row['Grade']
                    existing_observed_value = ObservedValue.objects.filter(
                        student=student,
                        advisory=advisory,
                        core_value=core_value,
                        behavior_statement=behavior_statement,
                        quarter=quarter
                    ).first()
                    if existing_observed_value:
                        existing_observed_value.grade = row['Grade']
                        existing_observed_value.save()
                    else:
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

