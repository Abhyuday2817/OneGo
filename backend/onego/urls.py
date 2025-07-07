# 📁 onego/urls.py

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
from apps.payments.views import PaymentViewSet, CheckoutView, PaymentResultView, test_invoice_pdf
from apps.match.views import MatchViewSet
from apps.chat.views import ChatRoomViewSet, MessageViewSet, UserSearchView
from apps.consultations.views import ConsultationViewSet
from apps.notifications.views import NotificationViewSet
from apps.badges.views import BadgeViewSet, UserBadgeViewSet, LeaderboardViewSet
from apps.support.views import SupportTicketViewSet
from apps.users.views import UserViewSet, AuthViewSet
from apps.appointments.views import AppointmentViewSet
from apps.mentorship_reviews.urls import urlpatterns as mentorship_review_urls
from apps.learning_tracks.views import LearningTrackViewSet, TrackEnrollmentViewSet

# 📘 Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="OneGo API",
        default_version='v1',
        description="OneGo Learning + Mentorship Marketplace API"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# 🔄 Router setup
router = DefaultRouter()

# ✅ Register viewsets (no duplicates, all required basename specified)
router.register(r"users", UserViewSet)
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"categories", CategoryViewSet)
#router.register(r"mentors", MentorProfileViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"gigs", GigRequestViewSet)
router.register(r"bids", BidViewSet)
router.register(r"contracts", ContractViewSet)
router.register(r"sessions", SessionViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"consultations", ConsultationViewSet)
router.register(r"notifications", NotificationViewSet, basename="notifications")
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet, basename="transactions")
router.register(r"payments", PaymentViewSet)
router.register(r"chatrooms", ChatRoomViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"match", MatchViewSet, basename="match")
router.register(r"user-badges", UserBadgeViewSet, basename="user-badges")
router.register(r"badges", BadgeViewSet)
router.register(r"badges/leaderboard", LeaderboardViewSet, basename="leaderboard")
router.register(r"support", SupportTicketViewSet)
router.register(r"learning-tracks", LearningTrackViewSet)
router.register(r"track-enrollments", TrackEnrollmentViewSet)
router.register(r"mentors", MentorProfileViewSet, basename='mentor')

# ✅ All URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/chat/", include("apps.chat.urls")),

    # 🔐 Authentication
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/", include("apps.bids.urls")),
    path("api/consultations/", include("apps.consultations.urls")),
    path("api/enrollments/", include("apps.enrollments.urls")),
    path("api/", include("apps.gigs.urls")),
    path("api/", include("apps.learning_requests.urls")),
    path("api/", include("apps.bids.urls")),
    path("api/", include("apps.badges.urls")),
    path("api/", include("apps.categories.urls")),
    path("api/", include("apps.consultations.urls")),
    path("api/", include("apps.enrollments.urls")),
    path("api/", include("apps.gigs.urls")),
    path("api/", include("apps.mentors.urls")),
    path("api/", include("apps.mentorship_reviews.urls")),
    path("api/", include("apps.payments.urls")),
    path("api/", include("apps.reviews.urls")),
    path("api/", include("apps.payments.urls")),
    path("api/", include("apps.mentors.urls")),
    path("api/", include("apps.payments.urls")),
    path("api/", include("apps.wallets.urls")),
    path("api/", include("apps.transactions.urls")),
    path("api/", include("apps.sessions.urls")),
    path("api/", include("apps.support.urls")),
    path("api/support/", include("apps.support.urls")),
    path("api/enrollments/", include("apps.enrollments.urls")),
    path("api/enrollments/", include("apps.enrollments.urls")),

    # onego/urls.py

    path("api/", include("apps.users.urls")),

    # 🔎 Swagger & Redoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # 🧠 Custom includes
    path("api/learning/", include("apps.learning_requests.urls")),
    path("api/courses/", include("apps.courses.urls")),
    path("api/mentorship-reviews/", include(mentorship_review_urls)),
    path("api/dashboard/", include("apps.dashboard.urls")),

    # 🧑‍💻 Chat user search
    path("api/chat/users/", UserSearchView.as_view(), name="chat-user-search"),

    # 💸 Test PDF Invoice
    path("test-invoice/", test_invoice_pdf),
]

# 🗂️ Static & Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
