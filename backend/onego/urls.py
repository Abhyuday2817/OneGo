from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ViewSets from apps
from apps.categories.views import CategoryViewSet
from apps.mentors.views import MentorProfileViewSet
from apps.courses.views import CourseViewSet
from apps.enrollments.views import EnrollmentViewSet
from apps.gigs.views import GigRequestViewSet, ContractViewSet
from apps.bids.views import BidViewSet
from apps.sessions.views import SessionViewSet
from apps.reviews.views import ReviewViewSet
from apps.wallets.views import WalletViewSet
from apps.transactions.views import TransactionViewSet
from apps.payments.views import PaymentViewSet, CheckoutView, PaymentResultView
from apps.match.views import MatchViewSet
from apps.chat.views import ChatRoomViewSet, MessageViewSet, UserSearchView
from apps.consultations.views import ConsultationViewSet
from apps.notifications.views import NotificationViewSet
from apps.badges.views import BadgeViewSet, UserBadgeViewSet, LeaderboardViewSet
from apps.support.views import SupportTicketViewSet
from apps.users.views import UserViewSet, AuthViewSet
from apps.appointments.views import AppointmentViewSet
from apps.payments.views import test_invoice_pdf
from django.urls import path, include
from django.urls import path, include
# OpenAPI Schema view
schema_view = get_schema_view(
    openapi.Info(
        title="OneGo API",
        default_version='v1',
        description="OneGo Learning + Mentorship Marketplace API"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()

# Core APIs
router.register(r"users", UserViewSet, basename="user")
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"mentors", MentorProfileViewSet, basename="mentor")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")

# Gigs/Bids/Contracts
router.register(r"gigs", GigRequestViewSet, basename="gig")
router.register(r"bids", BidViewSet, basename="bid")
router.register(r"contracts", ContractViewSet, basename="contract")

# Sessions & Appointments
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

# Reviews, Consultations, Notifications
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"consultations", ConsultationViewSet, basename="consultation")
router.register(r"notifications", NotificationViewSet, basename="notification")

# Wallets, Transactions, Payments
router.register(r"wallets", WalletViewSet, basename="wallet")
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"payments", PaymentViewSet, basename="payment")

# Chat & Messaging
router.register(r"chatrooms", ChatRoomViewSet, basename="chatroom")
router.register(r"messages", MessageViewSet, basename="message")

# Discovery / Matching
router.register(r"match", MatchViewSet, basename="match")

# Badges & Leaderboard
router.register(r"badges", BadgeViewSet, basename="badge")
router.register(r"user-badges", UserBadgeViewSet, basename="user-badge")
router.register(r"badges/leaderboard", LeaderboardViewSet, basename="leaderboard")

# Support
router.register(r"support", SupportTicketViewSet, basename="support")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # Swagger / Redoc
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Auth using dj-rest-auth (JWT)
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/learning/', include('apps.learning_requests.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),


    # Chat search endpoint
    path("api/chat/users/", UserSearchView.as_view(), name="chat-user-search"),
    path('accounts/', include('allauth.urls')),
    path('api/mentorship-reviews/', include('apps.mentorship_reviews.urls')),
    # Payment endpoints
    path("api/payments/checkout/", CheckoutView.as_view(), name="checkout"),
    path("api/payments/result/", PaymentResultView.as_view(), name="payment-result"),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),  # 🔑 Auth endpoints
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # optional
]

urlpatterns += [
    
    path('api/dashboard/', include('apps.dashboard.urls')),
]

# Static & Media URL serving
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("test-invoice/", test_invoice_pdf),
]

