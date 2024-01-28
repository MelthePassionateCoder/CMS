from django import forms
from .models import Section

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['school_year','section', 'subject', 'students']

        widgets = {
            'students': forms.CheckboxSelectMultiple,
        }

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['students']
        widgets = {
            'students': forms.CheckboxSelectMultiple,
        }