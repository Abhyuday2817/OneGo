# onego/backend/admin/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .dashboard import revenue_by_month, top_categories_by_enrollment

class AdminReportView(APIView):
    """
    A simple endpoint returning month-by-month revenue
    and your top categories by enrollment count.
    """
    permission_classes = []  # you probably want IsAdminUser here

    def get(self, request):
        return Response({
            "monthly_revenue": revenue_by_month(),
            "top_categories": top_categories_by_enrollment(),
        })
