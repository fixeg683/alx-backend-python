from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Built-in fields already include:
    id, password, first_name, last_name, email, username
    """

    # Example of EXTRA fields that do NOT exist in AbstractUser
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Tracks which users are in a conversation
    """

    conversation_id = models.AutoField(primary_key=True)    # REQUIRED BY TASK
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Stores messages inside conversations
    """

    message_id = models.AutoField(primary_key=True)        # REQUIRED BY TASK
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
