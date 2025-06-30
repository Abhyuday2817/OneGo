from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LearningRequestViewSet, LearningRequestProposalViewSet

router = DefaultRouter()
router.register(r'learning-requests', LearningRequestViewSet, basename='learning-request')
router.register(r'proposals', LearningRequestProposalViewSet, basename='proposal')

urlpatterns = [
    path('', include(router.urls)),
]
