from django.urls import path
from .views import MentorDashboardView, StudentDashboardView

urlpatterns = [
    path('mentor/', MentorDashboardView.as_view(), name='mentor-dashboard'),
    path('student/', StudentDashboardView.as_view(), name='student-dashboard'),
]
