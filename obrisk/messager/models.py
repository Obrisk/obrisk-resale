import uuid
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from obrisk.classifieds.models import Classified



class ConversationQuerySet(models.query.QuerySet):
    """ Simply the queries in the views that check the conversations btn users """
    #https://docs.djangoproject.com/en/2.1/ref/models/querysets/#operators-that-return-new-querysets
    
    def get_conversations(self, user):
        """ Get all conversations of a specific user """
        return self.filter( Q(first_user=user) | Q(second_user=user))

    def conversation_exists(self, user1, user2):
        """ Check if these 2 users had conversation before """
        qs = self.filter(first_user=user1, second_user=user2) | self.filter(first_user=user2, second_user=user1) 

        if qs:
            return True
        return False


    def get_conv_classified(self, user1, user2):
        qs = self.filter(Q (first_user=user1, second_user=user2)) | self.filter(first_user=user2, second_user=user1) 
        return qs.values_list('classified', flat=True)
    
class Conversation(models.Model):
    """Conversation information btn 2 users is stored here."""
    first_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='first_conv_user', null=True, on_delete=models.CASCADE)
    second_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='second_conv_user', null=True, blank=True, on_delete=models.CASCADE)
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='conversaction', null=True, blank=True)
    objects = ConversationQuerySet.as_manager()
    is_empty = models.BooleanField(default=True)
    #timestamp to rule whether is_empty conversations should be deleted.
    timestamp = models.DateTimeField(auto_now_add=True)
    #The default on key should be unique but put there just in case.
    key = models.CharField(max_length=64, unique=True, null=True)
    #messages = Defined in the Message class as a foreign key.

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")
        ordering = ("-timestamp", )
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = "{}.{}".format(*sorted([self.first_user.pk, self.second_user.pk]))
        super(Conversation, self).save(*args, **kwargs)


class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

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


class Message(models.Model):
    """A private message sent between users."""
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    #In the near future enforce all messages to belong to a specific conversation,
    #this will improve the query speed on the conversation list. (null=False)
    conversation = models.ForeignKey(
        Conversation, related_name='messages', null=True,
        blank=True,  on_delete=models.CASCADE)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        verbose_name=_("Sender"), null=True, on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages', null=True,
        blank=True, verbose_name=_("Recipient"), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000, blank=True, null=True)
    unread = models.BooleanField(default=True, db_index=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    img_preview = models.CharField(max_length=300, blank=True, null=True)
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='message', null=True, blank=True)
    attachment = models.CharField(max_length=300, blank=True, null=True)
    has_link = models.BooleanField(default=False)  
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("timestamp", )

    def __str__(self):
        if self.message:
            return self.message
        elif self.image: 
            return self.image
        elif self.attachment:
            return self.attachment
        else:
            return "This message has no string representation"

    def mark_as_read(self):
        """Method to mark a message as read."""
        if self.unread:
            self.unread = False
            self.save()
    
    def save(self, *args, **kwargs):
        """ Override to add conversation in the msg obj whenever a new message
        is sent btn users and update the empty conversation check.
        This operation is only done here on model level."""   
        if not self.conversation:
            key = "{}.{}".format(*sorted([self.sender.pk, self.recipient.pk]))
            try:
                conv = Conversation.objects.get(key=key)
                conv.is_empty = False
                conv.save()
                self.conversation = conv
            except:
                conv = Conversation(first_user=self.sender,
                                second_user=self.recipient,
                                key=key,
                                is_empty=False
                        )
                conv.save()
                self.conversation = conv
        super().save(*args, **kwargs)


    @staticmethod
    def send_message(sender, recipient, message,
                    image=None, img_preview=None, attachment=None):
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
            message=message,
            image=image, 
            img_preview=img_preview, 
            attachment=attachment
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
                'recipient':  msg_recip,
                'image': image, 
                'img_preview': img_preview, 
                'attachment': attachment
            }
        async_to_sync(channel_layer.group_send)(recipient.username, payload)
        return new_message

