from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    filter_horizontal = ('participants',)  # for ManyToMany field
    search_fields = ('conversation_id',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('message_body', 'sender__username', 'conversation__conversation_id')
