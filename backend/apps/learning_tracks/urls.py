### 📁 apps/learning_tracks/urls.py

from django.urls import path
from .views import TrackListView, TrackDetailView, EnrollInTrackView, MyTrackEnrollmentsView

urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/<int:track_id>/enroll/', EnrollInTrackView.as_view(), name='track-enroll'),
    path('my-tracks/', MyTrackEnrollmentsView.as_view(), name='my-tracks'),
]  

### ✅ Additional Suggestions
# 1. Add TrackProgressView to update quiz/course completion
# 2. Add mentor-only TrackCreateView if mentors allowed to create from frontend
# 3. Track badge system (e.g., "Completed Track X")