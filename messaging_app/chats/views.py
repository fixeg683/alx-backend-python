from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant, IsMessageOwnerOrParticipant, ConversationPermissions
from .pagination import MessagePagination, ConversationPagination
from .filters import MessageFilter, ConversationFilter

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing conversations.
    Only authenticated participants can access the conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [ConversationPermissions]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__username']
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """
        Return only conversations where the current user is a participant
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).prefetch_related('participants', 'messages')
        return Conversation.objects.none()
    
    def perform_create(self, serializer):
        """
        Automatically add the current user as a participant when creating a conversation
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing messages.
    Only authenticated participants can send, view, update and delete messages in a conversation.
    Implements pagination (20 messages per page) and filtering.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant, IsMessageOwnerOrParticipant]
    pagination_class = MessagePagination  # 20 messages per page
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['content', 'sender__username']
    ordering_fields = ['timestamp', 'is_read']
    ordering = ['-timestamp']  # Latest messages first
    
    def get_queryset(self):
        """
        Return only messages from conversations where the current user is a participant
        Apply filters and prefetch related objects for performance
        """
        user = self.request.user
        if not user.is_authenticated:
            return Message.objects.none()
            
        # Get conversation_id from query parameters for direct filtering
        conversation_id = self.request.query_params.get('conversation_id')
        
        queryset = Message.objects.filter(
            conversation__participants=user
        ).select_related('sender', 'conversation')
        
        if conversation_id:
            # Verify user is participant in this specific conversation
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if user not in conversation.participants.all():
                    return Message.objects.none()
                queryset = queryset.filter(conversation_id=conversation_id)
            except Conversation.DoesNotExist:
                return Message.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new message with the current user as sender
        Validate that the user is a participant in the conversation
        """
        conversation_id = self.request.data.get('conversation_id') or self.request.data.get('conversation')
        
        if not conversation_id:
            return Response(
                {"error": "conversation_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Check if user is participant in the conversation
            if self.request.user not in conversation.participants.all():
                return Response(
                    {"error": "You are not a participant in this conversation"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Save the message with the current user as sender
            serializer.save(sender=self.request.user, conversation=conversation)
            
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        """
        Handle PUT and PATCH requests for message updates
        """
        message = self.get_object()
        
        # Check if user is the message sender (owner)
        if message.sender != request.user:
            return Response(
                {"error": "You can only update your own messages"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests for message deletion
        """
        message = self.get_object()
        
        # Check if user is the message sender (owner)
        if message.sender != request.user:
            return Response(
                {"error": "You can only delete your own messages"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def conversation_messages(self, request):
        """
        Custom action to get messages for a specific conversation
        Requires conversation_id query parameter
        Uses pagination (20 messages per page)
        """
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {"error": "conversation_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verify user is participant in the conversation
            conversation = Conversation.objects.get(id=conversation_id)
            if request.user not in conversation.participants.all():
                return Response(
                    {"error": "You are not a participant in this conversation"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get messages for this conversation with pagination
            messages = Message.objects.filter(conversation_id=conversation_id)
            
            # Apply pagination
            page = self.paginate_queryset(messages)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
            
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )
