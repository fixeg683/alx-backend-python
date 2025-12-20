from rest_framework import permissions
from .models import Conversation, Message

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users who are participants
    in a conversation to send, view, update and delete messages.
    """
    
    def has_permission(self, request, view):
        # First, check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Allow safe methods (GET, HEAD, OPTIONS) but we'll filter by participant in get_queryset
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For POST, check if user is participant in the conversation
        if request.method == 'POST':
            conversation_id = request.data.get('conversation_id') or request.data.get('conversation')
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id)
                    return request.user in conversation.participants.all()
                except Conversation.DoesNotExist:
                    return False
            return False
            
        return True

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Check if the user is a participant in the conversation for this message
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Authenticated users only
    - Message owner to update or delete their own messages
    - Conversation participants to view messages
    """
    
    def has_permission(self, request, view):
        # Require authentication for all operations
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow participants to view messages
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
            
        # Allow message owner to update (PUT, PATCH) or delete (DELETE) their messages
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user
            
        return False


class ConversationPermissions(permissions.BasePermission):
    """
    Custom permission for conversation access:
    - Only authenticated users
    - Only participants can view the conversation
    - Only participants can add messages
    """
    
    def has_permission(self, request, view):
        # Require authentication for all operations
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        return request.user in obj.participants.all()
