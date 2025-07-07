from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LearningRequestViewSet, LearningRequestProposalViewSet

router = DefaultRouter()
router.register(r'learning-requests', LearningRequestViewSet, basename='learning-request')
router.register(r'learning-proposals', LearningRequestProposalViewSet, basename='learning-proposal')

urlpatterns = [
    path('', include(router.urls)),
]

# Example Routes Created:
# /api/learning-requests/             → List, Create, Retrieve, Update, Delete
# /api/learning-requests/my_requests/ → List own requests (custom action)
# /api/learning-requests/{id}/close/  → Close a request

# /api/learning-proposals/            → List/Create mentor proposals
# /api/learning-proposals/my_proposals/  → List mentor's own proposals
# /api/learning-proposals/{id}/select/   → Mark proposal as selected
