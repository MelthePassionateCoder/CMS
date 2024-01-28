from django import forms
from django.forms import inlineformset_factory
from .models import Section, Activity, Score

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

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'activity_type', 'totalScore','deadline','description']

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['section','student', 'score']

class ScoreFormSet(inlineformset_factory(Activity, Score, form=ScoreForm, extra=1, exclude=['activity'])):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students', None)
        super(ScoreFormSet, self).__init__(*args, **kwargs)
        if students:
            self.forms[0].fields['student'].queryset = students