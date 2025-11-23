from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=[("guest", "Guest"), ("host", "Host"), ("admin", "Admin")],
        default="guest",
    )

    def __str__(self):
        return self.username
