from rest_framework import viewsets, permissions, status
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
        user = self.request.user
        if user.is_staff:
            return LearningRequest.objects.all()
        return LearningRequest.objects.filter(is_open=True) | LearningRequest.objects.filter(student=user)

    @action(detail=False, methods=["get"])
    def my_requests(self, request):
        """
        /api/learning-requests/my_requests/
        Return only the learning requests posted by the current student.
        """
        queryset = LearningRequest.objects.filter(student=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        """
        /api/learning-requests/{id}/close/
        Closes the learning request.
        """
        learning_request = self.get_object()
        if learning_request.student != request.user:
            return Response({"error": "You are not the owner of this request."}, status=403)
        learning_request.close()
        return Response({"status": "Request closed"})


class LearningRequestProposalViewSet(viewsets.ModelViewSet):
    queryset = LearningRequestProposal.objects.all()
    serializer_class = LearningRequestProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LearningRequestProposal.objects.all()
        return LearningRequestProposal.objects.filter(mentor=user)

    @action(detail=False, methods=["get"])
    def my_proposals(self, request):
        """
        /api/learning-proposals/my_proposals/
        Returns all proposals submitted by the current mentor.
        """
        proposals = LearningRequestProposal.objects.filter(mentor=request.user)
        serializer = self.get_serializer(proposals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def select(self, request, pk=None):
        """
        /api/learning-proposals/{id}/select/
        Mark a proposal as selected (only by the student who created the request).
        """
        proposal = self.get_object()
        request_owner = proposal.request.student
        if request.user != request_owner:
            return Response({"error": "Only the owner of the request can select a proposal."}, status=403)
        if proposal.request.selected_proposal():
            return Response({"error": "A proposal is already selected."}, status=400)

        proposal.mark_as_selected()
        return Response({"status": "Proposal selected", "proposal_id": proposal.id})
