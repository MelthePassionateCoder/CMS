from django.urls import path
from .views import input_grades, input_observed_values

urlpatterns = [
    path('<int:advisory_id>/input-grades/', input_grades, name='grade_input'),
    path('<int:advisory_id>/input-observed-values/', input_observed_values, name='input_observed_values'),
    
]