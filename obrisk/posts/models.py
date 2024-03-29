import datetime
import itertools
from slugify import slugify

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from obrisk.notifications.models import (
        Notification, notification_handler)
from obrisk.utils.fields import RichTextField


class PostTags(TagBase):
    class Meta:
        verbose_name = _("Post Tag")
        verbose_name_plural = _("Post Tags")


class TaggedPost(GenericTaggedItemBase):
    tag = models.ForeignKey(
        PostTags,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items")


class PostQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    #this query is the longest.
    def get_active(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_draft(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    #Improve the performance of this query. It is too slow.
    def get_counted_tags(self):
        tag_dict = {}
        query = self.filter(status='P').annotate(
            tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.slugs():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Post(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
    )

    ARTICLE = "A"
    AWESOME_LIST = "A"
    CAREER = "C"
    EVENT = "E"
    HOW_TO = "H"
    LIFESYLE = "L"
    NEWS = "N"

    CATEGORY = (
        (ARTICLE, _("Article")),
        (AWESOME_LIST, _("Awesome list")),
        (CAREER, _("Career")),
        (EVENT, _("Event")),
        (HOW_TO, _("How-to-guide")),
        (LIFESYLE, _("Lifestyle")),
        (NEWS, _("News")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="author",
        on_delete=models.CASCADE)
    image = models.CharField(max_length=150, null=True, blank=True)
    img_small = models.CharField(max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80, null=False, unique=True)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = MarkdownxField(null=True, blank=True)
    content_html = RichTextField(null=True, blank=True)
    content_json = JSONField(null=True, blank=True)
    category =  models.CharField(max_length=1, choices=CATEGORY, default=ARTICLE)
    edited = models.BooleanField(default=False)
    tags = TaggableManager(through=TaggedPost, blank=True)
    date = models.DateField(default=datetime.date.today) #Just for slug.
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = first_slug = slugify(f"{self.user.username}-{self.title}",
                                to_lower=True, max_length=150)

            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post,
        on_delete=models.CASCADE, related_name='comments')
    user =models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="commentor",
        on_delete=models.CASCADE)
    body = models.TextField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)


def notify_comment(**kwargs):
    """Handler to be fired up upon comments signal to notify the author of a
    given posts."""
    actor = kwargs['request'].user
    receiver = kwargs['comment'].content_object.user
    obj = kwargs['comment'].content_object
    notification_handler(
        actor, receiver, Notification.COMMENTED, action_object=obj
    )
