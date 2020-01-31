import datetime
import itertools
import operator
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import SearchVectorField

from slugify import slugify
from taggit.managers import TaggableManager

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

        #return the slugs instead of names.
        for obj in query:
            for tag in obj.tags.slugs():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else: #smart
                    tag_dict[tag] += 1

        return sorted(tag_dict.items(), key=operator.itemgetter(1), reverse=True)


class Classified(models.Model):
    EXPIRED = "E"
    ACTIVE = "A"
    STATUS = (
        (ACTIVE, _("Active")),
        (EXPIRED, _("Expired")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="creater",
        on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300, null=True, blank=True, unique=True, editable=False)
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    details = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    address = models.CharField (max_length=300, null=True, blank=True)
    city = models.CharField (max_length=200)
    province_region = models.CharField(max_length= 200)
    phone_number = models.CharField (max_length=150, null=True, blank=True)
    wechat_id = models.CharField (max_length=150, null=True, blank=True)
    country = models.CharField(max_length= 100)
    total_views = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=True)
    tags = TaggableManager()
    priority = models.IntegerField(default=0)
    #This date is used only for the slug and the timestamp for creation time.
    date = models.DateField(default=datetime.date.today)
    # search_vector = SearchVectorField(null=True)

    objects = ClassifiedQuerySet.as_manager()

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("Classified")
        verbose_name_plural = _("Classifieds")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classifieds:classified', args=[self.slug])

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
    image = models.CharField(max_length=300)
    image_mid_size = models.CharField(max_length=300)
    image_thumb = models.CharField(max_length=300)

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.classified, public_id)

    def __str__(self):
        return str(self.image)

class OfficialAd(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="official_user",
        on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    details = models.CharField(max_length=2000)
    address = models.CharField (max_length=100, null=True, blank=True)
    city = models.CharField (max_length=100)
    province_region = models.CharField(max_length= 100)
    phone_number = models.CharField (max_length=150, null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("OfficialAd")
        verbose_name_plural = _("OfficialAds")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #These locations will be taken from the user's profile, else he has to change location.
        if not self.city:
            self.city =self.user.city
        if not self.province_region:
            self.province_region = self.user.province_region
        if not self.country:
            self.country = self.user.country

        super().save(*args, **kwargs)


class OfficialAdImages(models.Model):
    official_ad = models.ForeignKey(OfficialAd, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=300)

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Image <%s:%s>" % (self.official_ad, public_id)

    def __str__(self):
        return str(self.image)


class InDemand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             related_name='indemand_user', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item
