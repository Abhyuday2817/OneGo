from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, ChatRoom

class MessageModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')
        self.room = ChatRoom.objects.create(name="Test Room")
        self.room.members.set([self.sender, self.receiver])
        self.msg = Message.objects.create(
            room=self.room,
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

    def test_create_message(self):
        self.assertEqual(str(self.msg), f"{self.room}: From {self.sender} to {self.receiver} at {self.msg.sent_at}")
        self.assertEqual(self.msg.room, self.room)
        self.assertEqual(self.msg.sender, self.sender)

    def test_room_membership(self):
        self.assertIn(self.sender, self.room.members.all())
        self.assertIn(self.receiver, self.room.members.all())