from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from obrisk.notifications.models import Notification, notification_handler


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_("Full name"), blank=True, max_length=255)
    picture = models.ImageField(
        _('Profile picture'), upload_to='profile_pics/', null=True, blank=True)
    job_title = models.CharField(
        _('Job title'), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _('Personal URL'), max_length=555, blank=True, null=True)
    facebook_account = models.URLField(
        _('Facebook profile'), max_length=255, blank=True, null=True)
    instagram_account = models.URLField(
        _('Instagram account'), max_length=255, blank=True, null=True)
    linkedin_account = models.URLField(
        _('LinkedIn profile'), max_length=255, blank=True, null=True)
    short_bio = models.CharField(
        _('Describe yourself'), max_length=60, blank=True, null=True)
    bio = models.CharField(
        _('Short bio'), max_length=280, blank=True, null=True)
    country = models.CharField(
        _('Country'), max_length=100, default="Tanzania")
    province_region = models.CharField (_('Province/Region'), max_length=100, default="Mbeya")
    city = models.CharField  (  _('City'), max_length=100, default="Mbeya mjini") 
    points = models.IntegerField(  _('Points'), default=0)
    nationality = models.CharField (_('Nationality'), max_length=100, blank=True, null=True )
    phone_number = PhoneNumberField (_('Phone number'), default="Unknown_phone_no")  #Needs a country's code 
    is_official = models.BooleanField (default=False)      #For the use of published posts
    is_seller = models.BooleanField (default=False)  #For sellers in Classifieds.
    # near future please add unique 12 digit ID to use instead of username for url's especially in chat.
    #https://stackoverflow.com/questions/42703059/how-to-create-a-8-digit-unique-id-in-python

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username


def broadcast_login(sender, user, request, **kwargs):
    """Handler to be fired up upon user login signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_IN)


def broadcast_logout(sender, user, request, **kwargs):
    """Handler to be fired up upon user logout signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_OUT)


# user_logged_in.connect(broadcast_login)
# user_logged_out.connect(broadcast_logout)
