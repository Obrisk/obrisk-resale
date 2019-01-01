import uuid
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from taggit.managers import TaggableManager

from cloudinary.models import CloudinaryField


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
    title = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    #displayImage = ProcessedImageField(upload_to=get_displayImage_filename, processors=[ResizeToFit(300)], format='JPEG', options={'quality': 90}, default=None)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=PUBLISHED)
    details = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00 , null=False)
    #city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=False)
    #city = models.CharField(max_length=1, choices=CITIES)
    city = models.CharField (max_length=100, null=False)
    located_area = models.CharField (max_length=100, null=False)
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


class ClassifiedImages(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.classified, public_id)

def get_displayImage_filename():
    return "Since adding cloudinary these functions are useless!"

def get_images_filename():
    return "Also this is useless"
