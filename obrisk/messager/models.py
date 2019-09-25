import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from obrisk.classifieds.models import Classified



class ConversationQuerySet(models.query.QuerySet):
    """ Simply the queries in the views that check the conversations btn users """
    #https://docs.djangoproject.com/en/2.1/ref/models/querysets/#operators-that-return-new-querysets
    
    def get_conversations(self, user):
        """ Check if these 2 users had conversation before """
        return self.filter(first_user=user) | self.filter(second_user=user)

    def conversation_exists(self, user1, user2):
        qs = self.filter(first_user=user1, second_user=user2) | self.filter(first_user=user2, second_user=user1) 

        if qs:
            return True
        return False

    def get_conv_classified(self, user1, user2):
        qs = self.filter(first_user=user1, second_user=user2) | self.filter(first_user=user2, second_user=user1) 
        return qs.values_list('classified', flat=True)
    
class Conversation(models.Model):
    """Conversation information btn 2 users is stored here."""
    first_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='first_conv_user', null=True, on_delete=models.CASCADE)
    second_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='second_conv_user', null=True, blank=True, on_delete=models.CASCADE)
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='conversaction', null=True, blank=True)
    objects = ConversationQuerySet.as_manager()
    #messages = Defined in the Message class as a foreign key.



class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

    def get_msgs(self, sender, recipient):
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

    def get_conversations(self, recipient):
        user_list = [] #Stores user's list for checking inside this function.
        msgs_list = [] #Stores messages objects
        try:
            qs_sent = self.filter(sender=recipient)
            qs_recieved = self.filter(recipient=recipient)
            queryset = qs_sent.union(qs_recieved).order_by('-timestamp')
            
            #Search for conversations that user was involved
            for qs in queryset:
                if qs.sender == recipient:
                    if qs.recipient not in user_list:
                        msgs_list.append(qs)
                        user_list.append(qs.recipient)
                        
                elif qs.sender not in user_list:
                    msgs_list.append(qs)
                    user_list.append(qs.sender)
            return user_list, msgs_list

        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)


class Message(models.Model):
    """A private message sent between users."""
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    #In the near future enforce all messages to belong to a specific conversation,
    #this will improve the query speed on the conversation list. (null=False)
    conversation = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='messages', null=True,
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
    attachment = models.CharField(max_length=300, blank=True, null=True)
    has_link = models.BooleanField(default=False)  
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("-timestamp", )

    def __str__(self):
        if self.message:
            return self.message
        if self.image: 
            return self.image
        else:
            return str(self.uuid_id)

    def mark_as_read(self):
        """Method to mark a message as read."""
        if self.unread:
            self.unread = False
            self.save()

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
