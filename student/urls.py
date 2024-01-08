from django.urls import path
from .views import (StudentCreateView, 
                    StudentListView, 
                    StudentUpdateView, 
                    StudentDetailView)

urlpatterns = [
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
]