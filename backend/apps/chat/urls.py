from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet, UserSearchView

router = DefaultRouter()
router.register(r"rooms", ChatRoomViewSet, basename="chatroom")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    # Main REST API routes
    path("", include(router.urls)),

    # Custom user search endpoint for chat room creation, invite, etc.
    path("users/", UserSearchView.as_view(), name="chat-user-search"),
]
