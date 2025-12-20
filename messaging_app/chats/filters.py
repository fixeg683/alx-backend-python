import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class MessageFilter(filters.FilterSet):
    """
    Filter class for Message model to retrieve:
    - Messages with specific users
    - Messages within a time range
    - Messages from specific conversations
    """
    
    # Filter by conversation ID
    conversation = filters.NumberFilter(field_name='conversation__id')
    
    # Filter by sender username
    sender = filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    
    # Filter by date range
    start_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    
    # Filter by recent messages (last 24 hours, 7 days, etc.)
    recent = filters.ChoiceFilter(
        method='filter_recent',
        choices=[
            ('24h', 'Last 24 hours'),
            ('7d', 'Last 7 days'),
            ('30d', 'Last 30 days')
        ]
    )
    
    # Filter by read status
    is_read = filters.BooleanFilter(field_name='is_read')
    
    # Search in message content
    search = filters.CharFilter(field_name='content', lookup_expr='icontains')
    
    class Meta:
        model = Message
        fields = [
            'conversation', 
            'sender', 
            'start_date', 
            'end_date', 
            'is_read',
            'search'
        ]
    
    def filter_recent(self, queryset, name, value):
        """
        Filter messages by recent time periods
        """
        now = timezone.now()
        if value == '24h':
            return queryset.filter(timestamp__gte=now - timedelta(hours=24))
        elif value == '7d':
            return queryset.filter(timestamp__gte=now - timedelta(days=7))
        elif value == '30d':
            return queryset.filter(timestamp__gte=now - timedelta(days=30))
        return queryset


class ConversationFilter(filters.FilterSet):
    """
    Filter class for Conversation model to retrieve:
    - Conversations with specific participants
    - Recent conversations
    """
    
    # Filter by participant username
    participant = filters.CharFilter(
        method='filter_by_participant',
        label='Participant username'
    )
    
    # Filter by multiple participants
    participants = filters.CharFilter(
        method='filter_by_participants',
        label='Multiple participant usernames (comma-separated)'
    )
    
    # Filter by recent conversations
    recent = filters.BooleanFilter(
        method='filter_recent_conversations',
        label='Recent conversations (last 30 days)'
    )
    
    # Search in conversation messages content
    search = filters.CharFilter(
        method='filter_conversation_search',
        label='Search in conversation messages'
    )
    
    class Meta:
        model = Conversation
        fields = ['participant', 'participants', 'recent', 'search']
    
    def filter_by_participant(self, queryset, name, value):
        """
        Filter conversations that include a specific participant
        """
        return queryset.filter(participants__username__iexact=value)
    
    def filter_by_participants(self, queryset, name, value):
        """
        Filter conversations that include all specified participants
        """
        usernames = [username.strip() for username in value.split(',')]
        for username in usernames:
            queryset = queryset.filter(participants__username__iexact=username)
        return queryset.distinct()
    
    def filter_recent_conversations(self, queryset, name, value):
        """
        Filter conversations that have been active recently (last 30 days)
        """
        if value:
            thirty_days_ago = timezone.now() - timedelta(days=30)
            return queryset.filter(
                messages__timestamp__gte=thirty_days_ago
            ).distinct()
        return queryset
    
    def filter_conversation_search(self, queryset, name, value):
        """
        Search in conversation messages content
        """
        return queryset.filter(
            messages__content__icontains=value
        ).distinct()
