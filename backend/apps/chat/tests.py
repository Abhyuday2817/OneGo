from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.chat.models import ChatRoom, Message

User = get_user_model()

class ChatTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="Pass@123")
        self.user2 = User.objects.create_user(username="user2", password="Pass@123")
        self.room = ChatRoom.objects.create(name="Room 1")
        self.room.members.set([self.user1, self.user2])
        self.client.login(username="user1", password="Pass@123")

    def test_list_chatrooms(self):
        res = self.client.get("/api/chatrooms/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_send_message(self):
        res = self.client.post("/api/messages/", {
            "room": self.room.id,
            "content": "Hello World"
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["content"], "Hello World")
