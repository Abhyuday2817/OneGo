from rest_framework import serializers
from apps.mentors.serializers import MentorProfileSerializer
from apps.courses.serializers import CourseSerializer

class MentorRecommendationSerializer(serializers.Serializer):
    """
    A lean serializer for “recommended” mentors.
    """
    id = serializers.IntegerField()
    user = serializers.CharField(source="user.username")
    bio = serializers.CharField()
    rating = serializers.FloatField()
    hourly_rate = serializers.DecimalField(max_digits=8, decimal_places=2)

class CourseRecommendationSerializer(serializers.Serializer):
    """
    A lean serializer for “recommended” courses.
    """
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField(source="category.name")
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    delivery_type = serializers.CharField()
    mentor = serializers.CharField(source="mentor.user.username")
