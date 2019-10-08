import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from obrisk.notifications.models import Notification, notification_handler

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedStories(TaggedItemBase):
    content_object = models.ForeignKey('Stories', on_delete=models.CASCADE)




class Stories(models.Model):
    """Stories model to contain small information snippets in the same manner as
    Twitter does."""

    PUBLIC = "P"
    NEAR_BY = "N"
    CONNECTS = "C"

    VIEWERS = (
        (PUBLIC, _("Public")),
        (NEAR_BY, _("near-by")),
        (CONNECTS, _("Connects")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="publisher",
        on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True,
        null=True, on_delete=models.CASCADE, related_name="thread")
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=400)
    viewers =  models.CharField(max_length=1, choices=VIEWERS, default=PUBLIC)
    priority = models.IntegerField(default=0)
    tags = TaggableManager(through=TaggedStories)
    city = models.CharField (max_length=100, null=True)
    province_region = models.CharField(max_length= 100, null=True)
    address = models.CharField(max_length=255, null=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name="liked_stories")
    reply = models.BooleanField(verbose_name=_("Is a reply?"), default=False)

    class Meta:
        verbose_name = _("Stories")
        verbose_name_plural = _("Stories")
        ordering = ("-timestamp",)

    def __str__(self):
        return str(self.content)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.reply:
            channel_layer = get_channel_layer()
            payload = {
                    "type": "receive",
                    "key": "additional_stories",
                    "actor_name": self.user.username

                }
            async_to_sync(channel_layer.group_send)('notifications', payload)

    def get_absolute_url(self):
        return reverse("stories:detail", kwargs={"uuid_id": self.uuid})

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)
            notification_handler(user, self.user,
                                 Notification.LIKED, action_object=self,
                                 id_value=str(self.uuid_id),
                                 key='social_update')

    def get_parent(self):
        if self.parent:
            return self.parent

        else:
            return self

    def reply_this(self, user, text):
        """Handler function to create a Stories instance as a reply to any
        published stories.

        :requires:

        :param user: The logged in user who is doing the reply.
        :param content: String with the reply.
        """
        parent = self.get_parent()
        reply_stories = Stories.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )
        notification_handler(
            user, parent.user, Notification.REPLY, action_object=reply_stories,
            id_value=str(parent.uuid_id), key='social_update')

    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all().order_by('timestamp')

    def count_thread(self):
        return self.get_thread().count()

    def count_likers(self):
        return self.liked.count()

    def get_likers(self):
        return self.liked.all()


class StoryImages(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=300)
    image_thumb = models.CharField(max_length=300)

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.story, public_id)

    def __str__(self):
        return str(self.image)
