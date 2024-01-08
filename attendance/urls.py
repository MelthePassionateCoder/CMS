from django.urls import path
from .views import (AttendanceUploadView,
                    success_page, 
                    attendance_list,
                    school_month_list, 
                    add_school_month, 
                    edit_school_month,
                    delete_school_month,
                    upload_manual_input)
urlpatterns = [
    path('upload/<int:advisory_id>/', AttendanceUploadView.as_view(), name='upload_attendance'),
    path('success/', success_page, name='success_page'),
    path('list/<int:advisory_id>/', attendance_list, name='attendance-list'),
    path('school-months/', school_month_list, name='school_month_list'),
    path('school-months/add/', add_school_month, name='add_school_month'),
    path('school_month/delete/<int:month_id>/', delete_school_month, name='delete_school_month'),
    path('school-months/edit/<int:month_id>/', edit_school_month, name='edit_school_month'),
    path('<int:advisory_id>/upload-manual-input/', upload_manual_input, name='upload_manual_input'),
]