### 📁 apps/learning_tracks/serializers.py

from rest_framework import serializers
from .models import LearningTrack, TrackEnrollment
from apps.courses.serializers import CourseSerializer

class LearningTrackSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    mentor_name = serializers.CharField(source='mentor.user.username', read_only=True)

    class Meta:
        model = LearningTrack
        fields = ['id', 'title', 'description', 'mentor_name', 'courses', 'created_at']

class TrackEnrollmentSerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=LearningTrack.objects.all())

    class Meta:
        model = TrackEnrollment
        fields = ['id', 'track', 'student', 'progress', 'is_completed']
        read_only_fields = ['id', 'student', 'progress', 'is_completed']
