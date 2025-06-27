import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Connects to ws://.../ws/chat/<room_id>/ 
    and broadcasts messages to participants.
    """

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = f"chat_{self.room_id}"

        # ensure user is authenticated and in the room
        user = self.scope["user"]
        if not user.is_authenticated:
            return await self.close()

        room = await sync_to_async(ChatRoom.objects.get)(pk=self.room_id)
        if not await sync_to_async(room.participants.filter(pk=user.pk).exists)():
            return await self.close()

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # broadcast join
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "presence", "user": user.username, "action": "joined"}
        )

    async def disconnect(self, close_code):
        # leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        user = self.scope["user"]
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "presence", "user": user.username, "action": "left"}
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]

        # typing indicator
        if data.get("type") == "typing":
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "typing", "user": user.username}
            )
            return

        # message
        content = data.get("content", "").strip()
        if not content:
            return

        # save message
        msg = await sync_to_async(Message.objects.create)(
            room_id=self.room_id, sender=user, content=content
        )
        serialized = {
            "id": msg.id,
            "sender": user.username,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
        }

        # broadcast message
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat_message", "message": serialized}
        )

    async def chat_message(self, event):
        # send to WebSocket
        await self.send(text_data=json.dumps({"type": "message", "message": event["message"]}))

    async def typing(self, event):
        await self.send(text_data=json.dumps({"type": "typing", "user": event["user"]}))

    async def presence(self, event):
        await self.send(text_data=json.dumps({
            "type": "presence",
            "user": event["user"],
            "action": event["action"]
        }))
