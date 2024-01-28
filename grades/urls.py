from django.urls import path
from .views import input_grades, input_observed_values, SubjectList, SubjectCreate
urlpatterns = [
    path('<int:advisory_id>/input-grades/', input_grades, name='grade_input'),
    path('<int:advisory_id>/input-observed-values/', input_observed_values, name='input_observed_values'),
    path('subject/', SubjectList.as_view(), name='subject-list'),
    path('subject/create/', SubjectCreate.as_view(), name='subject-create'),
]