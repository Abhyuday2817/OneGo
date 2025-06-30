from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Bid
from .serializers import BidSerializer
from .filters import BidFilter


class BidViewSet(viewsets.ModelViewSet):
    """
    Full CRUD on Bids, plus accept/reject actions.
    """
    queryset = Bid.objects.select_related("mentor__user", "gig_request__student").all()
    serializer_class = BidSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ["created_at", "proposed_rate", "status"]
    ordering = ["-created_at"]
    search_fields = ["proposal_text", "mentor__user__username"]
    filterset_class = BidFilter

    def perform_create(self, serializer):
        """
        Automatically attach the logged-in user's mentor profile to the bid.
        """
        serializer.save(mentor=self.request.user.mentorprofile)

    @action(detail=True, methods=["post"], url_path="accept", url_name="accept")
    def accept(self, request, pk=None):
        """
        Accept a bid. Only the student who created the gig can accept a bid.
        """
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Only the gig owner can accept bids."}, status=status.HTTP_403_FORBIDDEN)
        bid.accept()
        return Response(self.get_serializer(bid).data)

    @action(detail=True, methods=["post"], url_path="reject", url_name="reject")
    def reject(self, request, pk=None):
        """
        Reject a bid. Only the student who created the gig can reject a bid.
        """
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Only the gig owner can reject bids."}, status=status.HTTP_403_FORBIDDEN)
        bid.reject()
        return Response(self.get_serializer(bid).data)

    @action(detail=False, methods=["get"], url_path="my-bids")
    def my_bids(self, request):
        """
        List bids by the current mentor.
        """
        if not hasattr(request.user, "mentorprofile"):
            return Response({"detail": "Only mentors can access their bids."}, status=status.HTTP_403_FORBIDDEN)
        bids = Bid.objects.filter(mentor=request.user.mentorprofile)
        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="received")
    def received_bids(self, request):
        """
        List all bids received on gigs posted by the current student.
        """
        bids = Bid.objects.filter(gig_request__student=request.user)
        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data)
