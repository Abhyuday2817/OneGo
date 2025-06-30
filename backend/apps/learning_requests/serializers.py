from rest_framework import serializers
from .models import LearningRequest, LearningRequestProposal


class LearningRequestSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = LearningRequest
        fields = '__all__'
        read_only_fields = ['student', 'created_at', 'updated_at']


class LearningRequestProposalSerializer(serializers.ModelSerializer):
    mentor_username = serializers.ReadOnlyField(source='mentor.username')

    class Meta:
        model = LearningRequestProposal
        fields = '__all__'
        read_only_fields = ['mentor', 'created_at']
