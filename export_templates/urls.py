from django.urls import path
from .views import export_templates

urlpatterns = [
    path('', export_templates, name='advisory_selection'),
]