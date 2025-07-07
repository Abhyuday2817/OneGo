### 📁 apps/learning_tracks/views.py

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import LearningTrack, TrackEnrollment
from .serializers import LearningTrackSerializer, TrackEnrollmentSerializer

# 🔹 Public API: List all tracks
class TrackListView(generics.ListAPIView):
    queryset = LearningTrack.objects.all().order_by('-created_at')
    serializer_class = LearningTrackSerializer
    permission_classes = [permissions.AllowAny]

# 🔹 Public API: Get details of one track
class TrackDetailView(generics.RetrieveAPIView):
    queryset = LearningTrack.objects.all()
    serializer_class = LearningTrackSerializer
    permission_classes = [permissions.AllowAny]

# 🔹 Authenticated: Enroll in a learning track
class EnrollInTrackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, track_id):
        user = request.user
        try:
            track = LearningTrack.objects.get(id=track_id)
            enrollment, created = TrackEnrollment.objects.get_or_create(student=user, track=track)
            if not created:
                return Response({"message": "Already enrolled."}, status=200)
            return Response({"message": "Enrolled successfully."})
        except LearningTrack.DoesNotExist:
            return Response({"error": "Track not found."}, status=404)

# 🔹 Authenticated: View user's track enrollments
class MyTrackEnrollmentsView(generics.ListAPIView):
    serializer_class = TrackEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrackEnrollment.objects.filter(student=self.request.user)

# ✅ Full ViewSet for LearningTrack (admin/future CRUD use)
class LearningTrackViewSet(viewsets.ModelViewSet):
    queryset = LearningTrack.objects.all().order_by('-created_at')
    serializer_class = LearningTrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def is_enrolled(self, request, pk=None):
        user = request.user
        track = self.get_object()
        enrolled = TrackEnrollment.objects.filter(student=user, track=track).exists()
        return Response({"enrolled": enrolled})

# ✅ Full ViewSet for TrackEnrollment (admin/mentor use)
class TrackEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = TrackEnrollment.objects.select_related('student', 'track').all()
    serializer_class = TrackEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
