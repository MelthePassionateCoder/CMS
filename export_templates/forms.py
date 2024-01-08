from django import forms
from advisory.models import Advisory

class AdvisorySelectionForm(forms.Form):
    advisory = forms.ModelChoiceField(queryset=Advisory.objects.all(), label='Select Advisory')
    template_type = forms.ChoiceField(choices=[('observed_values', 'Observed Values'), ('grades', 'Grades'), ('attendance', 'Attendance'),('monthly attendance', 'Monthly Attendance'),('manual monthly attendance', 'Manual Monthly Attendance'),('report card', 'Report Card')],
                                     widget=forms.RadioSelect, label='Select Template Type')