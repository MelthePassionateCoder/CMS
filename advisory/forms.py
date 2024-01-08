from django import forms
from .models import Advisory

class AdvisoryForm(forms.ModelForm):
    class Meta:
        model = Advisory
        fields = ['school_year','section', 'strand', 'students']

        widgets = {
            'students': forms.CheckboxSelectMultiple,
        }

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Advisory
        fields = ['students']
        widgets = {
            'students': forms.CheckboxSelectMultiple,
        }