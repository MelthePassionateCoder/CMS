from django.urls import path
from .views import (SectionListView, 
                    SectionCreateView,
                    SectionDetailView, 
                    AddStudentsToSectionView, 
                    create_activity, 
                    enter_scores, 
                    activity_list,
                    activity_details,
                    delete_activity,
                    compute_grade)
urlpatterns = [
    path('', SectionListView.as_view(), name='section-list'),
    path('create/', SectionCreateView.as_view(), name='section-create'),
    path('section/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),
    path('add-students/<int:section_id>', AddStudentsToSectionView.as_view(), name='add-students-section'),
    path('create_activity/<int:section_id>/', create_activity, name='create_activity'),
    path('enter_scores/<int:section_id>/<int:activity_id>/', enter_scores, name='enter_scores'),
    path('list/<int:section_id>/', activity_list, name='activity-list'),
    path('details/<int:section_id>/<int:activity_id>/', activity_details, name='activity-details'),
    path('delete/<int:activity_id>/', delete_activity, name='activity-delete'),
    path('compute_grade/<int:section_id>/', compute_grade, name='compute_grade'),
]