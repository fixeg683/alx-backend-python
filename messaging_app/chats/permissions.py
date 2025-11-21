from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access or modify messages.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # For Message object
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False

    def has_permission(self, request, view):
        # Only authenticated users can access
        if not request.user or not request.user.is_authenticated:
            return False

        # For safe methods (GET, HEAD, OPTIONS) we allow
        if request.method in permissions.SAFE_METHODS:
            return True

        # For unsafe methods, check object-level permission in viewsets
        return True
