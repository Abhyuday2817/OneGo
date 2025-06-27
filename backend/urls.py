from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'transactions/create', TransactionCreateViewSet, basename='transaction-create')

urlpatterns = [
    path('api/', include(router.urls)),
urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App endpoints (all start with /api/)
    path('api/onego/', include('onego.urls')),           # Global/cross-app endpoints, dashboards, settings, etc.
    path('api/users/', include('users.urls')),           # User registration, profile, etc.
    path('api/doctors/', include('doctors.urls')),       # Doctor dashboard, profile, etc.
    path('api/appointments/', include('appointments.urls')), # Appointment booking, listing, details

    # Add more as you expand (payments, notifications, chat, etc.)
    # path('api/payments/', include('payments.urls')),
    # path('api/notifications/', include('notifications.urls')),
    # path('api/chat/', include('chat.urls')),
]

