from django.urls import path
from .views import add_activity

urlpatterns = [
    path('add_activity/<int:subject_id>/', add_activity , name='add_activity'),
]