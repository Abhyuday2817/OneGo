from rest_framework import serializers
from .models import MentorReview


class MentorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorReview
        fields = ['id', 'mentor', 'student', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']