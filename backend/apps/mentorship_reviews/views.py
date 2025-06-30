from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MentorReview
from .serializers import MentorReviewSerializer


class MentorReviewViewSet(viewsets.ModelViewSet):
    queryset = MentorReview.objects.all()
    serializer_class = MentorReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter reviews by mentor or student.
        """
        queryset = super().get_queryset()
        mentor_id = self.request.query_params.get('mentor')
        student_id = self.request.query_params.get('student')

        if mentor_id:
            queryset = queryset.filter(mentor_id=mentor_id)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset