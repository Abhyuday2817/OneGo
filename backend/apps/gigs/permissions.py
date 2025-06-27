# File: apps/gigs/permissions.py

from rest_framework import permissions
from .models import GigRequest, Bid, Contract

class IsGigStudent(permissions.BasePermission):
    """
    Allows access only to the student who created the gig.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, GigRequest):
            return obj.student == request.user
        if isinstance(obj, Bid):
            return obj.gig_request.student == request.user
        if isinstance(obj, Contract):
            return obj.student == request.user
        return False

class IsContractParticipant(permissions.BasePermission):
    """
    Allows access only to the student or mentor associated with a contract.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Contract):
            return request.user in [obj.student, obj.mentor.user]
        return False
