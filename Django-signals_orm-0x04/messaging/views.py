from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch, Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages as django_messages
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
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).only('id', 'sender', 'receiver', 'content', 'timestamp', 'read', 'edited').order_by('timestamp')
    
    context = {
        'other_user': other_user,
        'messages': messages,
    }
    return render(request, 'messaging/conversation.html', context)

@login_required
def unread_messages_view(request):
    """
    View to display unread messages using custom manager with .only() optimization
    """
    # Using the custom manager with unread_for_user method and .only() optimization
    unread_messages = Message.unread.unread_for_user(request.user)
    
    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/unread_messages.html', context)

@login_required
def inbox_view(request):
    """
    View to display user's inbox with unread messages using custom manager
    """
    # Using custom manager to get only unread messages received by the user
    unread_received_messages = Message.unread.unread_received_for_user(request.user)
    
    # Get all received messages (including read) for the inbox with optimization
    all_received_messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').only(
        'id', 'sender', 'content', 'timestamp', 'read'
    ).order_by('-timestamp')
    
    context = {
        'unread_received_messages': unread_received_messages,
        'all_received_messages': all_received_messages,
        'unread_count': unread_received_messages.count(),
    }
    return render(request, 'messaging/inbox.html', context)

@login_required
def mark_as_read_view(request, message_id):
    """
    View to mark a message as read
    """
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.mark_as_read()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('inbox')

@login_required
def mark_all_as_read_view(request):
    """
    View to mark all unread messages as read
    """
    # Using custom manager to get unread messages
    unread_messages = Message.unread.unread_for_user(request.user)
    updated_count = unread_messages.update(read=True)
    
    django_messages.success(request, f'Marked {updated_count} messages as read.')
    return redirect('inbox')

@login_required
def message_history_view(request, message_id):
    """
    View to display message edit history
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has permission to view this message's history
    if message.sender != request.user and message.receiver != request.user:
        return render(request, 'messaging/access_denied.html', status=403)
    
    history = message.history.select_related('edited_by').only(
        'id', 'old_content', 'edited_by', 'edited_at'
    ).all()
    
    context = {
        'message': message,
        'history': history,
    }
    return render(request, 'messaging/message_history.html', context)

@login_required
def edit_message_view(request, message_id):
    """
    View to edit a message and track the edit history
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content and new_content != message.content:
            message.content = new_content
            message.save()  # This will trigger the pre_save signal and create history
    
    context = {
        'message': message,
    }
    return render(request, 'messaging/edit_message.html', context)

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

# Rest of the views remain the same...
