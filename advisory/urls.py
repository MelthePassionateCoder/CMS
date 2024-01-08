from django.urls import path
from .views import (AdvisoryCreateView, 
                    AdvisoryListView,
                    AdvisoryDetailView, 
                    AddStudentsToAdvisoryView, 
                    AdvisoryUpdateView, 
                    AdvisoryDeleteView,
                    report_cards_page)

urlpatterns = [
    path('create/', AdvisoryCreateView.as_view(), name='advisory-create'),
    path('', AdvisoryListView.as_view(), name='advisory-list'),
    path('advisory/<int:pk>/', AdvisoryDetailView.as_view(), name='advisory-detail'),
    path('<int:advisory_id>/add-students/', AddStudentsToAdvisoryView.as_view(), name='add-students'),
    path('<int:pk>/update/', AdvisoryUpdateView.as_view(), name='advisory-update'),
    path('<int:pk>/delete/', AdvisoryDeleteView.as_view(), name='advisory-delete'),
    path('<int:advisory_id>/report-cards/', report_cards_page, name='report_cards_page'),
]