from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from rest_framework.views import APIView
from rest_framework.response import Response

# -----------------------
# API Root
# -----------------------
class APIRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Welcome to Messaging API",
            "conversations": "/api/conversations/",
            "messages": "/api/messages/"
        })

# -----------------------
# Conversation ViewSet
# -----------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Only return conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

# -----------------------
# Message ViewSet
# -----------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only return messages in conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)
