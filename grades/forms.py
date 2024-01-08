from django import forms
from .models import Grade, Subject, Semester
from .models import ObservedValue

class ObservedValueImportForm(forms.Form):
    excel_file = forms.FileField(label='Excel File')

class GradeImportForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    excel_file = forms.FileField(label='Select Excel File')