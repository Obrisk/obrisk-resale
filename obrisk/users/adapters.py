#This adapter file is just for reference but it is never used.
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError


class AccountAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        if len(username) > 16:
            raise ValidationError('The username length must be less than 16 characters')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.

        
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
