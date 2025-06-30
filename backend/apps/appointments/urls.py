from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentListCreateView.as_view(), name='appointments_list_create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('analytics/', views.AnalyticsView.as_view(), name='appointments_analytics'),
    path('reminder/<int:pk>/', views.AppointmentReminderView.as_view(), name='appointments_reminder'),
    path('export/', views.AppointmentExportCSVView.as_view(), name='appointments_export'),
    path('calendar/<int:pk>/sync/', views.AppointmentGoogleCalendarSyncView.as_view(), name='appointments_google_sync'),
]