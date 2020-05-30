from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from obrisk.notifications.models import Notification, notification_handler


MALE = "M"
FEMALE = "F"
STATUS = (
    (MALE, _("Male")),
    (FEMALE, _("Female")),
)


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_("Full name"), blank=True, max_length=255)
    org_picture = models.CharField(max_length=150, null=True, blank=True)
    picture = models.CharField(max_length=150, null=True, blank=True)
    thumbnail = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)

    job_title = models.CharField(
        _('Job title'), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _('Personal URL'), max_length=555, blank=True, null=True)
    facebook_account = models.CharField(
        _('Facebook a/c profile name'), max_length=255, blank=True, null=True)
    instagram_account = models.CharField(
        _('Instagram a/c profile name'), max_length=255, blank=True, null=True)
    linkedin_account = models.CharField(
        _('LinkedIn a/c profile name'), max_length=255, blank=True, null=True)
    snapchat_account = models.CharField(
        _('Snapchat a/c profile name'), max_length=255, blank=True, null=True)
    wechat_id = models.CharField (max_length=150, null=True, blank=True)

    wechat_openid = models.CharField(
            max_length=100,blank=True,
            null=True,verbose_name="wechat_openid",
            unique=True
    )
    #Without blank=True the forms add is required label
    address = models.CharField(max_length=300, null=True, blank=True)
    province_region = models.CharField (_('Province'), max_length=200)
    city = models.CharField  (  _('City'), max_length=200)
    nationality = models.CharField (_('Nationality'), max_length=200, blank=True, null=True )
    short_bio = models.CharField(
        _('Describe yourself'), max_length=60, blank=True, null=True)
    bio = models.CharField(
        _('Short bio'), max_length=280, blank=True, null=True)
    country = models.CharField(
        _('Country'), max_length=100, default="China")
    points = models.IntegerField(  _('Points'), default=0)
    phone_number = PhoneNumberField (_('Phone number'))  #Needs a country's code 
    is_official = models.BooleanField (default=False)      #For the use of published posts
    is_seller = models.BooleanField (default=False)  #For sellers in Classifieds.
    #The values here are only in one month therefore reset every month.
    classifieds_transactions_received = models.IntegerField(default=0)
    no_of_classifieds_posted = models.IntegerField( default=0)
    no_of_classifieds_negotiated = models.IntegerField( default=0)
    no_of_jobs_applied =  models.IntegerField( default=0)
    no_of_jobs_posted =  models.IntegerField( default=0)
    no_of_events_registered =  models.IntegerField( default=0)
    status = models.IntegerField(default=0)
    # near future please add unique 12 digit ID to use instead of username for url's especially in chat.
    #https://stackoverflow.com/questions/42703059/how-to-create-a-8-digit-unique-id-in-python

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_profile_name(self):
        return self.username


def broadcast_login(sender, user, request, **kwargs):
    """Handler to be fired up upon user login signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_IN)


# def broadcast_logout(sender, user, request, **kwargs):
#     """Handler to be fired up upon user logout signal to notify all users."""
#     notification_handler(user, "global", Notification.LOGGED_OUT)


# user_logged_in.connect(broadcast_login)
# user_logged_out.connect(broadcast_logout)
