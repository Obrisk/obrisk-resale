import datetime
import itertools
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from taggit.managers import TaggableManager

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class ClassifiedQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_active(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="A")

    def get_expired(self):
        """Returns only the items marked as EXPIRED in the current queryset."""
        return self.filter(status="E")

    def get_counted_tags(self):
        tag_dict = {}
        query = self.filter(status='A').annotate(
            tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Classified(models.Model):
    EXPIRED = "E"
    ACTIVE = "A"
    STATUS = (
        (ACTIVE, _("Active")),
        (EXPIRED, _("Expired")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="creater",
        on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    slug = models.SlugField(max_length=300, null=True, blank=True, unique=True, editable=False)
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    details = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    located_area = models.CharField (max_length=100)
    city = models.CharField (max_length=100)
    province_region = models.CharField(max_length= 100)
    contact_info = models.CharField (max_length=150, null=True, blank=True)
    country = models.CharField(max_length= 100)
    total_views = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    tags = TaggableManager()
    date = models.DateField(default=datetime.date.today)
    objects = ClassifiedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Classified")
        verbose_name_plural = _("Classifieds")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = first_slug = slugify(f"{self.user.username}-{self.title}-{self.date}", allow_unicode=True,
                                to_lower=True, max_length=300)
            
            for x in itertools.count(1):
                if not Classified.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)

        #These locations will be taken from the user's profile, else he has to change location.
        if not self.city:
            self.city =self.user.city
        if not self.province_region:
            self.province_region = self.user.province_region
        if not self.country:
            self.country = self.user.country

        super().save(*args, **kwargs)




class ClassifiedImages(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='attachments')
    file_thumbnail = ImageSpecField(source='file',
                                    processors=[ResizeToFill(100, 50)],
                                    format='JPEG',
                                    options={'quality': 60})
    image = CloudinaryFieldFix('image')

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.classified, public_id)

    def __str__(self):
        return str(self.image)

# image = ClassifiedImages.objects.all()[0]
# 

