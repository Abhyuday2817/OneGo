from rest_framework.routers import DefaultRouter
from .views import GigRequestViewSet, BidViewSet, ContractViewSet

router = DefaultRouter()
router.register(r"gigs", GigRequestViewSet, basename="gig")
router.register(r"bids", BidViewSet, basename="bid")
router.register(r"contracts", ContractViewSet, basename="contract")

urlpatterns = router.urls
