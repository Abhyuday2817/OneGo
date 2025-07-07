from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Bid
from .serializers import BidSerializer
from .filters import BidFilter
from services.notifications import notify_user


class IsMentorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, "mentorprofile")


class BidViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Bids, with mentor-specific creation and student-only accept/reject control.
    """
    queryset = Bid.objects.select_related("mentor__user", "gig_request__student").all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, IsMentorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ["created_at", "proposed_rate", "status"]
    ordering = ["-created_at"]
    search_fields = ["proposal_text", "mentor__user__username"]
    filterset_class = BidFilter

    def perform_create(self, serializer):
        """
        Automatically attach the logged-in mentor.
        """
        serializer.save(mentor=self.request.user.mentorprofile)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        """
        Student accepts a bid.
        """
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Only the gig owner can accept bids."}, status=status.HTTP_403_FORBIDDEN)

        if bid.is_accepted():
            return Response({"detail": "This bid is already accepted."}, status=400)

        bid.accept()
        return Response(self.get_serializer(bid).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        """
        Student rejects a bid.
        """
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Only the gig owner can reject bids."}, status=status.HTTP_403_FORBIDDEN)

        if bid.is_rejected():
            return Response({"detail": "This bid is already rejected."}, status=400)

        bid.reject()
        return Response(self.get_serializer(bid).data)

    @action(detail=False, methods=["get"], url_path="my-bids")
    def my_bids(self, request):
        """
        List all bids placed by the current mentor.
        """
        if not hasattr(request.user, "mentorprofile"):
            return Response({"detail": "Only mentors can access this."}, status=status.HTTP_403_FORBIDDEN)

        bids = Bid.objects.filter(mentor=request.user.mentorprofile)
        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="received")
    def received_bids(self, request):
        """
        List all bids received on the student's gigs.
        """
        bids = Bid.objects.filter(gig_request__student=request.user)
        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        """
        Mentor cancels a pending bid (optional).
        """
        bid = self.get_object()

        if request.user != bid.mentor.user:
            return Response({"detail": "Only the mentor who made the bid can cancel it."}, status=403)

        if not bid.is_pending():
            return Response({"detail": "Only pending bids can be cancelled."}, status=400)

        bid.status = Bid.STATUS_REJECTED
        bid.save()

        notify_user(
            bid.gig_request.student,
            f"{bid.mentor.user.username} has cancelled their bid on your gig “{bid.gig_request.title}”."
        )

        return Response({"detail": "Bid cancelled."}, status=200)
