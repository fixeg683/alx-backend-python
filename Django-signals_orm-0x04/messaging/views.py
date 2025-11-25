from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
from .models import Message, Notification, MessageHistory

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_view(request, user_id):
    """
    View to display conversation between current user and another user
    """
    other_user = get_object_or_404(User, id=user_id)
    
    # Get messages with optimized queries
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('timestamp')
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'messaging/conversation.html', context)

@login_required
def unread_messages_view(request):
    """
    View to display unread messages using custom manager
    """
    unread_messages = Message.unread_objects.for_user(request.user)
    
    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/unread_messages.html', context)

@login_required
def message_history_view(request, message_id):
    """
    View to display message edit history
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    history = message.history.all()
    
    context = {
        'message': message,
        'history': history,
    }
    return render(request, 'messaging/message_history.html', context)

@login_required
@require_http_methods(["POST"])
def delete_user_view(request):
    """
    View to allow user to delete their account
    """
    user = request.user
    user.delete()
    # User will be logged out automatically due to session invalidation
    return JsonResponse({'status': 'success', 'message': 'Account deleted successfully'})

def get_threaded_messages(message_id):
    """
    Function to recursively fetch all replies to a message
    """
    message = Message.objects.select_related('sender', 'receiver').get(id=message_id)
    
    def get_replies(msg):
        replies = msg.replies.select_related('sender', 'receiver').all()
        threaded_replies = []
        for reply in replies:
            threaded_replies.append({
                'message': reply,
                'replies': get_replies(reply)
            })
        return threaded_replies
    
    return {
        'message': message,
        'replies': get_replies(message)
    }