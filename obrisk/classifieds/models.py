from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from django_comments.signals import comment_was_posted
from taggit.managers import TaggableManager


from obrisk.notifications.models import Notification, notification_handler


class ClassifiedQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    def get_counted_tags(self):
        tag_dict = {}
        query = self.filter(status='P').annotate(
            tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Classified(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="creater",
        on_delete=models.SET_NULL)
    
    image = models.ImageField(
        _('Featured image'), upload_to='classified_pictures/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=PUBLISHED)
    details = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00 , null=False)
    city = models.CharField (max_length=100, null=False)
    district = models.CharField (max_length=100, null=False)
    street_area = models.CharField (max_length=100, null=False)
    total_views = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    tags = TaggableManager()
    objects = ClassifiedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Classified")
        verbose_name_plural = _("Classifieds")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.title}",
                                to_lower=True, max_length=80)

        super().save(*args, **kwargs)

def notify_comment(**kwargs):
    """Handler to be fired up upon comments signal to notify the creater of a
    given classified."""
    actor = kwargs['request'].user
    receiver = kwargs['comment'].content_object.user
    obj = kwargs['comment'].content_object
    notification_handler(
        actor, receiver, Notification.COMMENTED, action_object=obj
        )

comment_was_posted.connect(receiver=notify_comment)
