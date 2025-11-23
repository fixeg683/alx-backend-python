from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow participants in a conversation to:
    - Send messages (POST)
    - View messages (GET) 
    - Update messages (PUT, PATCH)
    - Delete messages (DELETE)
    """
    
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all, but we'll filter by participant in get_queryset
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
        # Check if the user is a participant in the conversation for this message
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Message owner to update or delete their own messages
    - Conversation participants to view messages
    """
    
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
    - Only participants can view the conversation
    - Only participants can add messages
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        return request.user in obj.participants.all()
