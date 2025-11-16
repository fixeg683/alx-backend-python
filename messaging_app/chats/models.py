import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Override the default primary key with UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[
            ("guest", "Guest"),
            ("host", "Host"),
            ("admin", "Admin"),
        ],
        default="guest",
    )

    def __str__(self):
        # Use username for clarity (email may be blank unless enforced)
        return self.username


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"{self.sender.username} → {self.conversation.id}"
