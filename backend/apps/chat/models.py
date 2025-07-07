from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatRoom(models.Model):
    """
    A chat room: either 1:1 DM (is_group=False) or a named group chat.
    """
    name = models.CharField(max_length=255, blank=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chat_rooms",
        through="ChatMembership",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["is_group", "created_at"])]
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"

    def __str__(self):
        if self.is_group:
            return self.name or f"Group Chat {self.pk}"
        users = list(self.members.values_list("username", flat=True))
        return "DM: " + " & ".join(users)

    def last_message(self):
        return self.messages.order_by("-sent_at").first()

    def unread_count(self, user):
        return self.messages.exclude(read_by=user).count()

    def is_muted_for(self, user):
        membership = ChatMembership.objects.filter(room=self, user=user).first()
        if membership and membership.muted_until:
            return membership.muted_until > timezone.now()
        return False

    @classmethod
    def get_or_create_dm(cls, user1, user2):
        dm = cls.objects.filter(is_group=False, members=user1).filter(members=user2).first()
        if dm:
            return dm
        dm = cls.objects.create(is_group=False)
        dm.members.set([user1, user2])
        return dm


class ChatMembership(models.Model):
    """
    Represents a user's membership in a chat room.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="memberships")
    joined_at = models.DateTimeField(auto_now_add=True)
    muted_until = models.DateTimeField(null=True, blank=True)
    nickname = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = [["user", "room"]]
        verbose_name = "Chat Membership"
        verbose_name_plural = "Chat Memberships"

    def __str__(self):
        return f"{self.user.username} in {self.room}"


class Message(models.Model):
    """
    A message sent in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="received_messages")
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="read_messages", blank=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    system_message = models.BooleanField(default=False)

    class Meta:
        ordering = ["sent_at"]
        indexes = [
            models.Index(fields=["room", "sent_at"]),
            models.Index(fields=["receiver", "sent_at"]),
        ]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"[{self.room}] {self.sender}: {self.content[:20]}"

    def mark_read(self, user):
        if user not in self.read_by.all():
            self.read_by.add(user)
        return self.read_by.count()

    def edit(self, new_content):
        self.content = new_content
        self.edited_at = timezone.now()
        self.save()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    @property
    def is_unread(self):
        return not self.read_by.exists()

    @staticmethod
    def bulk_mark_read(room, user):
        qs = Message.objects.filter(room=room).exclude(read_by=user)
        for msg in qs:
            msg.read_by.add(user)
        return qs.count()

    def toggle_pin(self):
        self.pinned = not self.pinned
        self.save()
        return self.pinned


class Attachment(models.Model):
    """
    Represents an attachment associated with a message.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return f"Attachment for Message {self.message_id}"


class Reaction(models.Model):
    """
    Reactions (like emoji) to a message.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    reacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["message", "user", "emoji"]]
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"

    def __str__(self):
        return f"{self.user.username} reacted with {self.emoji}"
