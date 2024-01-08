from django import forms
from .models import DailyAttendance, SchoolMonth, MonthlyAttendanceManual
from student.models import Student
from advisory.models import Advisory
from django.forms import inlineformset_factory
class AttendanceUploadForm(forms.Form):
    advisory = forms.ModelChoiceField(queryset=Advisory.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.SelectDateWidget())
    file = forms.FileField(label='Select an Excel file')

class SchoolMonthForm(forms.ModelForm):
    class Meta:
        model = SchoolMonth
        fields = ['school_year', 'semester','month', 'month_name', 'month_order', 'school_days']
    
ManualAttendanceForm = forms.modelformset_factory(
    MonthlyAttendanceManual,
    fields=('days_present', 'days_absent'),
    extra=0  
)

class MonthlyAttendanceManualUploadForm(forms.Form):
    file = forms.FileField(label='Select Excel File')