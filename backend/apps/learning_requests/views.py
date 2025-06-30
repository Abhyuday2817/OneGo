from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import LearningRequest, LearningRequestProposal
from .serializers import LearningRequestSerializer, LearningRequestProposalSerializer


class LearningRequestViewSet(viewsets.ModelViewSet):
    queryset = LearningRequest.objects.all().order_by('-created_at')
    serializer_class = LearningRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return LearningRequest.objects.all()
        return LearningRequest.objects.filter(is_open=True)


class LearningRequestProposalViewSet(viewsets.ModelViewSet):
    queryset = LearningRequestProposal.objects.all()
    serializer_class = LearningRequestProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

    def get_queryset(self):
        return LearningRequestProposal.objects.filter(mentor=self.request.user)
