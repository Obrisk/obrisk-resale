import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer


class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

    def get_conversation(self, sender, recipient):
        """Returns all the messages sent between two users."""
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('timestamp')

    def get_most_recent_conversation(self, recipient):
        """Returns the most recent conversation counterpart's username."""
        try:
            qs_sent = self.filter(sender=recipient)
            qs_recieved = self.filter(recipient=recipient)
            qs = qs_sent.union(qs_recieved).latest("timestamp")
            if qs.sender == recipient:
                return qs.recipient

            return qs.sender

        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)

    def mark_conversation_as_read(self, sender, recipient):
        """Mark as read any unread elements in the current conversation."""
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)

    def get_all_conversation(self, recipient):
        chat_list = [] #Stores messages objects
        msgs_list = []
        try:
            qs_sent = self.filter(sender=recipient)
            qs_recieved = self.filter(recipient=recipient)
            queryset = qs_sent.union(qs_recieved).order_by('-timestamp')
            
            #Search for conversations that user was involved
            for qs in queryset:
                if qs.sender == recipient:
                    if qs.recipient not in chat_list:
                        msgs_list.append(qs)
                        chat_list.append(qs.recipient)
                        
                elif qs.sender not in chat_list:
                    msgs_list.append(qs)
                    chat_list.append(qs.sender)

            return chat_list, msgs_list

        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)


class Message(models.Model):
    """A private message sent between users."""
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        verbose_name=_("Sender"), null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages', null=True,
        blank=True, verbose_name=_("Recipient"), on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000, blank=True)
    unread = models.BooleanField(default=True, db_index=True)
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("-timestamp", )

    def __str__(self):
        return self.message

    def mark_as_read(self):
        """Method to mark a message as read."""
        if self.unread:
            self.unread = False
            self.save()

    @staticmethod
    def send_message(sender, recipient, message):
        """Method to create a new message in a conversation.
        :requires:

        :param sender: User instance of the user sending the message.
        :param recipient: User instance of the user to recieve the message.
        :param message: Text piece shorter than 1000 characters containing the
                        actual message.
        """
        new_message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )
        channel_layer = get_channel_layer()
        
        msg_sender = str(sender)
        msg_recip = str(recipient)
        msg = str(new_message.uuid_id)
        payload = {
                'type': 'receive',
                'key': 'message',
                'message_id': msg,
                'sender': msg_sender,
                'recipient':  msg_recip
            }
        async_to_sync(channel_layer.group_send)(recipient.username, payload)
        return new_message
