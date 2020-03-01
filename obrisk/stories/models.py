import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from obrisk.notifications.models import Notification, notification_handler

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, TagBase, GenericTaggedItemBase, CommonGenericTaggedItemBase, GenericUUIDTaggedItemBase

class StoryTags(TagBase):
    class Meta:
        verbose_name = _("Story Tag")
        verbose_name_plural = _("Story Tags")

class TaggedStory(GenericUUIDTaggedItemBase):
    tag = models.ForeignKey(
        StoryTags,
        on_delete=models.CASCADE,
        related_name="tags")

    class Meta:
        verbose_name = _("Tagged story")
        verbose_name_plural = _("Tagged stories")

class TaggedStories(TaggedItemBase):
    content_object = models.ForeignKey('Stories', on_delete=models.CASCADE)


class Stories(models.Model):
    """Stories model to contain small information snippets in the same manner as
    Twitter does."""

    PUBLIC = "P"
    AROUND = "A"
    CONNECTS = "C"

    VIEWERS = (
        (PUBLIC, _("Public")),
        (AROUND, _("around")),
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
    content = models.TextField(max_length=400, null=True)
    viewers =  models.CharField(max_length=1, choices=VIEWERS, default=PUBLIC)
    priority = models.IntegerField(default=0)
    tags = TaggableManager(through=TaggedStories, related_name='oldtags')
    new_tags = TaggableManager(through=TaggedStory, blank=True)
    city = models.CharField (max_length=100, null=True)
    video = models.CharField (max_length=300, null=True)
    province_region = models.CharField(max_length= 100, null=True)
    address = models.CharField(max_length=255, null=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name="liked_stories")
    reply = models.BooleanField(verbose_name=_("Is a reply?"), default=False)

    #This will help to only show the liked users when needed, otherwise don't load all of them.
    likes_count = models.IntegerField(default=0)  
    thread_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Stories")
        verbose_name_plural = _("Stories")
        ordering = ("-timestamp",)

    def __str__(self):
        if self.content:
            return str(self.content)
        else:
            return ""

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        #These locations will be taken from the user's profile, else he has to change location.
        if not self.reply:
            if not self.city:
                self.city =self.user.city
            if not self.province_region:
                self.province_region = self.user.province_region


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
        """The object update here is not saved, monitor this implementation so see if likes counts
        are updated in the database."""
        if user in self.liked.all():
            self.liked.remove(user)
            self.likes_count = F('likes_count') - 1
            self.save()

        else:
            self.liked.add(user)
            self.likes_count = F('likes_count') + 1
            self.save()
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
        #increment comments
        parent.thread_count = F('thread_count') + 1
        parent.save()


        notification_handler(
            user, parent.user, Notification.REPLY, action_object=reply_stories,
            id_value=str(parent.uuid_id), key='social_update')

    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all()

    def get_likers(self):
        return self.liked.all()[:3]

    def get_all_likers(self):
        return self.liked.all()
        
    def count_thread(self):
        return self.get_thread().count()

    def count_likers(self):
        return self.liked.count()


class StoryImages(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=300)
    image_thumb = models.CharField(max_length=300)


    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.story, public_id)

    def __str__(self):
        return str(self.image)
