from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'created_at',
            'last_message',
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'id': last_msg.id,
                'text': last_msg.text,
                'sender': last_msg.sender.username,
                'created_at': last_msg.created_at,
            }
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'created_at']
        read_only_fields = ['sender', 'created_at']
