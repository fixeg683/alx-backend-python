from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # Message object
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False

    def has_permission(self, request, view):
        # Only authenticated users can access the API
        return request.user and request.user.is_authenticated
