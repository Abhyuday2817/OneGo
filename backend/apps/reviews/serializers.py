from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserSerializer
from apps.mentors.serializers import MentorProfileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    reviewer      = UserSerializer(read_only=True)
    reviewer_id   = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer().Meta.model.objects.all(),
        source='reviewer',
        write_only=True
    )
    reviewee      = MentorProfileSerializer(read_only=True)
    reviewee_id   = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer().Meta.model.objects.all(),
        source='reviewee',
        write_only=True
    )
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer', 'reviewer_id', 'reviewer_name',
            'reviewee', 'reviewee_id',
            'rating', 'comment',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'reviewer_name']
