import uuid
import itertools
import operator
import datetime
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from slugify import slugify
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from phonenumber_field.modelfields import PhoneNumberField


class ClassifiedTags(TagBase):
    class Meta:
        verbose_name = _("Classifieds Tag")
        verbose_name_plural = _("Classifieds Tags")


class TaggedClassifieds(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ClassifiedTags,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items")
    class Meta:
        verbose_name = _("Classified tag")
        verbose_name_plural = _("Classified Tags")


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

    OFFLINE = "O"
    SHIPPING = "S"
    ANY = "A"
    HANDOVER = (
        (OFFLINE, _("Offline_pickup")),
        (SHIPPING, _("Shipping")),
        (ANY, _("any")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="creater",
        on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
            max_length=300, null=True,
            blank=True, unique=True, editable=False
        )
    status = models.CharField(max_length=1, choices=STATUS, default=ACTIVE)
    details = models.CharField(max_length=2000, null=True, blank=True)
    price = models.DecimalField(
            blank=True, null=True,
            max_digits=15, decimal_places=2, default=0.00
        )
    english_address = models.CharField (max_length=300, null=True, blank=True)
    chinese_address = models.CharField (max_length=300, null=True, blank=True)
    city = models.CharField (max_length=200, null=True, blank=True)
    province_region = models.CharField(max_length= 200, null=True, blank=True)
    phone_number = models.CharField (max_length=150, null=True, blank=True)
    wechat_id = models.CharField (max_length=150, null=True, blank=True)
    country = models.CharField(max_length= 100, null=True, blank=True)
    thumbnail = models.CharField (max_length=300, null=True, blank=True)
    video = models.CharField (max_length=300, null=True, blank=True)
    edited = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=True)
    tags = TaggableManager(through=TaggedClassifieds, blank=True)
    priority = models.IntegerField(default=0)
    shipping_price = models.DecimalField(
            max_digits=15, decimal_places=2, default=0.00
        )
    handover_method = models.CharField(max_length=1, choices=HANDOVER, default=ANY)
    bidding = models.BooleanField(default=False)
    max_bid_price = models.DecimalField(
            null=True, blank=True,
            max_digits=15, decimal_places=2, default=0.00
        )
    bids_count = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True, blank=True)
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
            self.slug = first_slug = slugify(f"{self.user.username}-{self.title}",
                                to_lower=True, max_length=300)

            for x in itertools.count(1):
                if not Classified.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)

        #These locations will be taken from the user's profile,
        #else he has to change location.
        if not self.city:
            self.city =self.user.city
        if not self.province_region:
            self.province_region = self.user.province_region
        if not self.country:
            self.country = self.user.country
        if not self.chinese_address:
            self.chinese_address = self.user.chinese_address
        if not self.english_address:
            self.english_address = self.user.english_address

        super().save(*args, **kwargs)


class ClassifiedImages(models.Model):
    classified = models.ForeignKey(
            Classified,
            on_delete=models.CASCADE,
            related_name='images'
        )
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


class ClassifiedOrder(models.Model):
    AWAITING = "A"
    CONFIRMED = "C"
    DISPATCHED = "D"
    FETCHED = "F"
    INFERRED = "I"
    REIMBURSED = "R"
    AXED = "X"

    STATUS = (
        (AWAITING, _("Awaiting")),
        (CONFIRMED, _("Confirmed")),
        (DISPATCHED, _("Dispatched")),
        (FETCHED, _("Fetched")),
        (INFERRED, _("Inferred")),
        (REIMBURSED, _("Reimbursed")),
        (AXED, _("Axed")),
    )

    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    is_offline = models.BooleanField(default=False)
    classified = models.ForeignKey(
        Classified, null=True, related_name="paid_order",
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
            auto_now_add=True, editable=False
        )
    buyer = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            null=True, related_name="order_user",
            on_delete=models.CASCADE
        )

    recipient_name = models.CharField(
            _("Full name"), blank=True, max_length=255
        )
    recipient_phone_number = PhoneNumberField(
            ('Phone number'), null=True, blank=True
        )
    tracking_number = models.CharField (
            max_length=600, null=True, blank=True
        )
    buyer_transaction_id = models.CharField (
            max_length=600, null=True, blank=True
        )
    seller_transaction_id = models.CharField (
            max_length=600, null=True, blank=True
        )
    notes = models.CharField(
            max_length=1000, null=True, blank=True
        )
    recipient_chinese_address = models.CharField (
            max_length=300, null=True, blank=True
        )
    status = models.CharField(
            max_length=1, choices=STATUS, default=AWAITING
        )
    slug = models.SlugField(
            max_length=300, null=True,
            blank=True, unique=True, editable=False
        )

    class Meta:
        verbose_name = _("Classifieds_Order")
        verbose_name_plural = _("Classifieds_orders")
        ordering = ("-timestamp",)

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('classifieds:orders', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = first_slug = slugify(
                    f"{self.classified.title}-{uuid.uuid4().hex}",
                    to_lower=True, max_length=300)

            for x in itertools.count(1):
                if not ClassifiedOrder.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)

        super().save(*args, **kwargs)


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
