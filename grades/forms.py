from django import forms
from .models import Grade, Subject, Semester, Quarter
from .models import ObservedValue

class ObservedValueImportForm(forms.Form):
    excel_file = forms.FileField(label='Excel File')

class GradeImportForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    quarter = forms.ModelChoiceField(queryset=Quarter.objects.all())
    excel_file = forms.FileField(label='Select Excel File')

class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name','order', 'category']