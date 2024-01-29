from django import forms
from django.forms import inlineformset_factory
from .models import Section, Activity, Score
from student.models import Student

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
        fields = ['section','student', 'score','activity']

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)

class ScoreFormSet(inlineformset_factory(Activity, Score, form=ScoreForm, extra=1, exclude=['activity'])):
    def __init__(self, *args, **kwargs):
        self.section = kwargs.pop('section', None)
        self.students = kwargs.pop('students', None)
        super(ScoreFormSet, self).__init__(*args, **kwargs)
        if self.students:
            self.forms[0].fields['student'].queryset = self.students
    
    def add_fields(self, form, index):
        super(ScoreFormSet, self).add_fields(form, index)
        form.fields['section'].widget = forms.HiddenInput()
        form.fields['activity'].widget = forms.HiddenInput()
