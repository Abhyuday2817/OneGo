from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as df_filters
from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from .models import Session
from .serializers import SessionSerializer
from services.escrow import hold_session_fee, release_to_mentor, refund_session


class SessionFilter(df_filters.FilterSet):
    student = df_filters.NumberFilter(field_name="student_id")
    mentor = df_filters.NumberFilter(field_name="mentor_id")
    upcoming = df_filters.BooleanFilter(method="filter_upcoming")

    class Meta:
        model = Session
        fields = ["status", "session_type", "student", "mentor", "upcoming"]

    def filter_upcoming(self, qs, name, value):
        now = timezone.now()
        return qs.filter(start_time__gt=now) if value else qs.filter(start_time__lte=now)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related("student", "mentor__user").all()
    serializer_class = SessionSerializer
    filterset_class = SessionFilter
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["start_time", "status"]
    ordering = ["-start_time"]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(student=user) | Q(mentor__user=user)
        )

    def perform_create(self, serializer):
        session = serializer.save()
        hold_session_fee(self.request.user, session)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        session = self.get_object()
        role = request.query_params.get("role")
        if role == "student" and request.user == session.student:
            session.student_confirmed = True
        elif role == "mentor" and request.user == session.mentor.user:
            session.mentor_confirmed = True
        else:
            return Response(
                {"detail": "Invalid role or permission."},
                status=status.HTTP_403_FORBIDDEN
            )

        session.save()
        session.try_verify()
        return Response(SessionSerializer(session).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        session = self.get_object()
        if request.user not in [session.student, session.mentor.user]:
            return Response(status=status.HTTP_403_FORBIDDEN)
        session.cancel()
        refund_session(session)
        return Response({"status": "cancelled"})

    @action(detail=False, methods=["post"])
    def bulk_cancel(self, request):
        ids = request.data.get("ids", [])
        sessions = Session.objects.filter(id__in=ids)
        cancelled_count = 0
        for sess in sessions:
            sess.cancel()
            refund_session(sess)
            cancelled_count += 1
        return Response({"cancelled_count": cancelled_count})

    @action(detail=False, methods=["get"])
    def stats(self, request):
        qs = self.get_queryset()
        mentor_id = request.query_params.get("mentor_id")
        if mentor_id:
            qs = qs.filter(mentor_id=mentor_id)

        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")

        if date_from:
            qs = qs.filter(start_time__gte=date_from)
        if date_to:
            qs = qs.filter(end_time__lte=date_to)

        total = qs.count()
        completed = qs.filter(status=Session.STATUS_COMPLETED).count()
        revenue = sum(
            s.rate_applied * s.duration_minutes()
            for s in qs.filter(status=Session.STATUS_COMPLETED)
        )

        return Response({
            "total_sessions": total,
            "completed_sessions": completed,
            "estimated_revenue": round(float(revenue), 2)
        })
