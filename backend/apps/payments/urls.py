# payments/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WalletViewSet,
    TransactionViewSet,
    PaymentViewSet,
)

router = DefaultRouter()
# GET  /api/payments/wallets/                → list all wallets (admin)  
# GET  /api/payments/wallets/{username}/     → retrieve a user’s wallet  
# POST /api/payments/wallets/{username}/top_up/  
# POST /api/payments/wallets/{username}/hold/  
# POST /api/payments/wallets/{username}/release/
router.register(r"wallets", WalletViewSet, basename="wallet")

# GET /api/payments/transactions/        → ledger entries  
# GET /api/payments/transactions/{pk}/  
router.register(r"transactions", TransactionViewSet, basename="transaction")

# GET  /api/payments/payments/           → list your payments  
# POST /api/payments/payments/           → create (top‐up or session charge)  
# GET  /api/payments/payments/{pk}/      → retrieve  
# POST /api/payments/payments/{pk}/refund/  
# GET  /api/payments/payments/{pk}/invoice/  
# POST /api/payments/payments/webhook/  
# GET  /api/payments/payments/stats/?period=day|month
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
