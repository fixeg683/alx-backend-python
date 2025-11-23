import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

# Use the global custom user model
User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    """
    Conversation model with UUID primary key
    Tracks participants using ManyToMany relation to the CustomUser
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(
        User, related_name="conversations_participated"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Message model with UUID primary key
    Linked to Conversation and CustomUser
    """
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
