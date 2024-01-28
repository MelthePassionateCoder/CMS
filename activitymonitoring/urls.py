from django.urls import path
from .views import SectionListView, SectionCreateView,SectionDetailView, AddStudentsToSectionView
urlpatterns = [
    path('', SectionListView.as_view(), name='section-list'),
    path('create/', SectionCreateView.as_view(), name='section-create'),
    path('section/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),
    path('add-students/<int:section_id>', AddStudentsToSectionView.as_view(), name='add-students-section'),
]