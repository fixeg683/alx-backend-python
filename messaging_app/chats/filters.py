# messaging_app/chats/filters.py
import django_filters
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # filter messages by a user id who is participant in message's conversation
    participant = django_filters.ModelChoiceFilter(
        field_name="conversation__participants",
        queryset=User.objects.all(),
        label="participant",
        method=None
    )

    # created_at range filtering
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["conversation", "participant", "created_after", "created_before", ]
