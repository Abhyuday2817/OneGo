from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import GigRequest, Bid, Contract
from .serializers import (
    GigRequestSerializer,
    BidSerializer,
    ContractSerializer
)
from .filters import GigRequestFilter


class GigRequestViewSet(viewsets.ModelViewSet):
    """
    CRUD + actions for Gig Requests
    """
    queryset = GigRequest.objects.prefetch_related("bids", "contracts").select_related("student", "category")
    serializer_class = GigRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["bidding_deadline", "budget_max", "created_at"]
    ordering = ["-bidding_deadline"]
    filterset_class = GigRequestFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(Q(student=user) | Q(bids__mentor__user=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["get"])
    def bids(self, request, pk=None):
        gig = self.get_object()
        qs = gig.bids.select_related("mentor__user")
        page = self.paginate_queryset(qs)
        serializer = BidSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"])
    def place_bid(self, request, pk=None):
        gig = self.get_object()
        if not gig.is_open():
            return Response({"detail": "Bidding is closed."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BidSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(gig_request=gig, mentor=request.user.mentorprofile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        gig = self.get_object()
        if request.user != gig.student:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        gig.cancel()
        return Response({"status": gig.status})

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        gig = self.get_object()
        if request.user != gig.student:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        gig.close()
        return Response({"status": gig.status})


class BidViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only access to Bids.
    Accept/reject via POST actions.
    """
    queryset = Bid.objects.select_related("mentor__user", "gig_request__student")
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(gig_request__student=user) | Q(mentor__user=user)
        ).distinct()

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        bid.accept()
        return Response(self.get_serializer(bid).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        bid = self.get_object()
        if request.user != bid.gig_request.student:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        bid.reject()
        return Response(self.get_serializer(bid).data)


class ContractViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View active/completed contracts.
    Cancel or complete via POST.
    """
    queryset = Contract.objects.select_related("mentor__user", "student", "gig_request", "bid")
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(student=user) | Q(mentor__user=user)
        ).distinct()

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        contract = self.get_object()
        if request.user not in [contract.student, contract.mentor.user]:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        contract.complete()
        return Response({"status": contract.status})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        contract = self.get_object()
        if request.user not in [contract.student, contract.mentor.user]:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        contract.cancel()
        return Response({"status": contract.status})
