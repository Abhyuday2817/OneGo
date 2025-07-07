# apps/support/urls.py

from rest_framework.routers import DefaultRouter
from .views import SupportTicketViewSet

# Register only the viewset, no prefix needed since it’s handled in onego/urls.py
router = DefaultRouter()
router.register(r'', SupportTicketViewSet, basename='support')

urlpatterns = router.urls
