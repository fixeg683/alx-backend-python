from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal to create notification when a new message is created
    """
    if created and instance.receiver != instance.sender:  # Don't notify if user messages themselves
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits before saving
    """
    if instance.pk:  # Only for existing instances (edits)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Message content changed, log the history
                # Get the current user from thread local (if available)
                from django.utils.module_loading import import_string
                from django.conf import settings
                
                edited_by = None
                try:
                    # Try to get the current user from request
                    from django.contrib.auth import get_user
                    from crum import get_current_user
                    edited_by = get_current_user()
                except:
                    # If crum is not available, try alternative methods
                    try:
                        from threading import local
                        _thread_locals = local()
                        if hasattr(_thread_locals, 'request'):
                            edited_by = _thread_locals.request.user
                    except:
                        pass
                
                # If we couldn't get the current user, use the message sender as fallback
                if edited_by is None or not edited_by.is_authenticated:
                    edited_by = instance.sender
                
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=edited_by
                )
                instance.edited = True
                instance.edited_by = edited_by
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all related data when a user is deleted
    Using explicit queryset filtering to ensure all related data is deleted
    """
    user_id = instance.id
    
    # Delete all messages where user is sender or receiver using Message.objects.filter()
    Message.objects.filter(sender_id=user_id).delete()
    Message.objects.filter(receiver_id=user_id).delete()
    
    # Delete all notifications for the user using Notification.objects.filter()
    Notification.objects.filter(user_id=user_id).delete()
    
    # Delete all message histories where the user edited messages using MessageHistory.objects.filter()
    MessageHistory.objects.filter(edited_by_id=user_id).delete()
    
    # Also clean up any message histories for messages that were sent/received by this user
    # First get all message IDs where user was involved
    user_message_ids = list(Message.objects.filter(sender_id=user_id).values_list('id', flat=True))
    user_message_ids.extend(list(Message.objects.filter(receiver_id=user_id).values_list('id', flat=True)))
    
    # Delete message histories for those messages
    if user_message_ids:
        MessageHistory.objects.filter(message_id__in=user_message_ids).delete()

# Alternative approach using pre_delete to handle foreign key constraints
@receiver(post_delete, sender=User)
def cleanup_user_data_alternative(sender, instance, **kwargs):
    """
    Alternative implementation that explicitly deletes all related data
    """
    try:
        # Get the user ID before deletion
        user_id = instance.id
        
        # Method 1: Delete messages where user is sender
        sent_messages = Message.objects.filter(sender_id=user_id)
        sent_message_count = sent_messages.count()
        sent_messages.delete()
        print(f"Deleted {sent_message_count} sent messages for user {user_id}")
        
        # Method 2: Delete messages where user is receiver  
        received_messages = Message.objects.filter(receiver_id=user_id)
        received_message_count = received_messages.count()
        received_messages.delete()
        print(f"Deleted {received_message_count} received messages for user {user_id}")
        
        # Method 3: Delete notifications for the user
        user_notifications = Notification.objects.filter(user_id=user_id)
        notification_count = user_notifications.count()
        user_notifications.delete()
        print(f"Deleted {notification_count} notifications for user {user_id}")
        
        # Method 4: Delete message histories edited by the user
        edited_histories = MessageHistory.objects.filter(edited_by_id=user_id)
        edited_history_count = edited_histories.count()
        edited_histories.delete()
        print(f"Deleted {edited_history_count} message histories edited by user {user_id}")
        
        # Method 5: Clean up orphaned message histories (for messages that were already deleted)
        # This handles cases where CASCADE might not have worked properly
        all_message_ids = Message.objects.all().values_list('id', flat=True)
        orphaned_histories = MessageHistory.objects.exclude(message_id__in=all_message_ids)
        orphaned_count = orphaned_histories.count()
        orphaned_histories.delete()
        print(f"Deleted {orphaned_count} orphaned message histories")
        
    except Exception as e:
        print(f"Error during user data cleanup: {e}")

# More explicit version that handles each model separately
@receiver(post_delete, sender=User)
def comprehensive_user_data_cleanup(sender, instance, **kwargs):
    """
    Comprehensive cleanup using explicit Message.objects.filter() calls
    """
    user_id = instance.id
    
    # 1. Clean up Message model data
    try:
        # Delete all messages sent by the user
        messages_sent = Message.objects.filter(sender_id=user_id)
        messages_sent_count = messages_sent.count()
        messages_sent.delete()
        print(f"Deleted {messages_sent_count} messages sent by user {user_id}")
        
        # Delete all messages received by the user  
        messages_received = Message.objects.filter(receiver_id=user_id)
        messages_received_count = messages_received.count()
        messages_received.delete()
        print(f"Deleted {messages_received_count} messages received by user {user_id}")
    except Exception as e:
        print(f"Error cleaning up messages for user {user_id}: {e}")
    
    # 2. Clean up Notification model data
    try:
        notifications = Notification.objects.filter(user_id=user_id)
        notification_count = notifications.count()
        notifications.delete()
        print(f"Deleted {notification_count} notifications for user {user_id}")
    except Exception as e:
        print(f"Error cleaning up notifications for user {user_id}: {e}")
    
    # 3. Clean up MessageHistory model data
    try:
        # Delete histories where user was the editor
        edited_histories = MessageHistory.objects.filter(edited_by_id=user_id)
        edited_history_count = edited_histories.count()
        edited_histories.delete()
        print(f"Deleted {edited_history_count} message histories edited by user {user_id}")
        
        # Also clean up histories for messages that involved this user
        # Get all message IDs where this user was involved
        user_related_message_ids = set()
        user_related_message_ids.update(Message.objects.filter(sender_id=user_id).values_list('id', flat=True))
        user_related_message_ids.update(Message.objects.filter(receiver_id=user_id).values_list('id', flat=True))
        
        if user_related_message_ids:
            related_histories = MessageHistory.objects.filter(message_id__in=user_related_message_ids)
            related_history_count = related_histories.count()
            related_histories.delete()
            print(f"Deleted {related_history_count} message histories related to user {user_id}")
            
    except Exception as e:
        print(f"Error cleaning up message histories for user {user_id}: {e}")
