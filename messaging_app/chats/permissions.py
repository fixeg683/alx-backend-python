from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message
        if isinstance(obj, Conversation):
            # Only participants can access conversation
            return request.user in obj.participants.all()
        else:
            # For Message objects, check if user is a participant in the parent conversation
            return request.user in obj.conversation.participants.all()

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated
