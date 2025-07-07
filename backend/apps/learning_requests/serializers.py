from rest_framework import serializers
from .models import LearningRequest, LearningRequestProposal
from django.utils import timezone


class LearningRequestProposalSerializer(serializers.ModelSerializer):
    mentor_username = serializers.ReadOnlyField(source='mentor.username')
    is_winner = serializers.SerializerMethodField()

    class Meta:
        model = LearningRequestProposal
        fields = [
            'id',
            'mentor',
            'mentor_username',
            'request',
            'proposal_text',
            'proposed_price',
            'estimated_days',
            'is_selected',
            'created_at',
            'is_winner',
        ]
        read_only_fields = ['mentor', 'created_at', 'is_selected']

    def get_is_winner(self, obj):
        return obj.is_selected


class LearningRequestSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')
    total_proposals = serializers.IntegerField(read_only=True)
    selected_proposal_id = serializers.SerializerMethodField()
    proposals = LearningRequestProposalSerializer(many=True, read_only=True)

    class Meta:
        model = LearningRequest
        fields = [
            'id',
            'student',
            'student_username',
            'title',
            'description',
            'category',
            'budget_min',
            'budget_max',
            'preferred_language',
            'timeline_days',
            'is_open',
            'created_at',
            'updated_at',
            'total_proposals',
            'selected_proposal_id',
            'proposals',
        ]
        read_only_fields = ['student', 'created_at', 'updated_at', 'is_open']

    def get_selected_proposal_id(self, obj):
        selected = obj.selected_proposal()
        return selected.id if selected else None

    def validate(self, data):
        """
        Ensure budget_max ≥ budget_min.
        """
        if data.get("budget_max") and data.get("budget_min"):
            if data["budget_max"] < data["budget_min"]:
                raise serializers.ValidationError("Maximum budget must be greater than or equal to minimum budget.")
        return data

    def create(self, validated_data):
        """
        Automatically assign current user as the student.
        """
        user = self.context['request'].user
        validated_data['student'] = user
        return super().create(validated_data)
