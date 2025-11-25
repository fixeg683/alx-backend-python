from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingModelsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
    
    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertFalse(message.read)
        self.assertFalse(message.edited)
    
    def test_notification_creation_signal(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check if notification was created by signal
        notification = Notification.objects.filter(user=self.user2, message=message).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
    
    def test_message_edit_history_signal(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check if history was created
        history = MessageHistory.objects.filter(message=message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original content")
        self.assertTrue(message.edited)
    
    def test_unread_messages_manager(self):
        # Create read and unread messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message",
            read=False
        )
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
        
        unread_count = Message.unread_objects.for_user(self.user2).count()
        self.assertEqual(unread_count, 1)
    
    def test_threaded_conversation(self):
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Parent message"
        )
        
        reply_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply message",
            parent_message=parent_message
        )
        
        self.assertEqual(parent_message.replies.count(), 1)
        self.assertEqual(parent_message.replies.first(), reply_message)
    
    def test_user_deletion_cleanup(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Delete user and check if related data is cleaned up
        user1_id = self.user1.id
        self.user1.delete()
        
        # Check if messages sent by user1 are deleted
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(sender_id=user1_id)

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
    
    def test_post_save_signal_creates_notification(self):
        message_count = Message.objects.count()
        notification_count = Notification.objects.count()
        
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check if message was created
        self.assertEqual(Message.objects.count(), message_count + 1)
        # Check if notification was created by signal
        self.assertEqual(Notification.objects.count(), notification_count + 1)
    
    def test_pre_save_signal_logs_edits(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        message_history_count = MessageHistory.objects.count()
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check if history was created
        self.assertEqual(MessageHistory.objects.count(), message_history_count + 1)