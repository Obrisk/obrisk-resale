from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    def clean_username(self, username, **kwargs):
        if len(username) > 16:
            raise ValidationError('The username length must be less than 16 characters')
        return DefaultAccountAdapter.clean_username(self, username, **kwargs)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        print(provider_id)
        print(error.__str__())
        print(exception.__str__())
        print(extra_context)

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
