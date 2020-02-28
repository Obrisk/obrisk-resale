import requests
import datetime

from obrisk.utils.images_upload import bucket
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError
from django.conf import settings
from allauth.account.utils import user_field
from django.contrib.auth import get_user_model
from slugify import slugify
# from django.http import JsonResponse


class AccountAdapter(DefaultAccountAdapter):

    def clean_username(self, username, **kwargs):
        if len(username) > 16:
            raise ValidationError('The username length must be less than 16 characters')
        return DefaultAccountAdapter.clean_username(self, username, **kwargs)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def authentication_error(self, request, provider_id, error, exception, extra_context):
        # print(provider_id)
        # print(error.__str__())
        # print(exception.__str__())
        # print(extra_context)
        pass

#    #def pre_social_login(self, request, sociallogin):
#        try:
#            get_user_model().objects.get(email=sociallogin.user.email)
#            print(get_user_model().objects.get(email=sociallogin.user.email), 'its from the email')
#        except get_user_model().DoesNotExist:
#            from django.contrib import messages
#            messages.add_message(request, messages.ERROR, 'Social logon from this account not allowed.') 
#           raise ImmediateHttpResponse(HttpResponse(status=500))
#        else:
#            user = get_user_model().objects.get(email=sociallogin.user.email)
#            if not sociallogin.is_existing:
#                sociallogin.connect(request, user) 

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def populate_user(self,
                      request,
                      sociallogin,
                      data,
                      **kwargs):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        name = data.get('name')
        user = sociallogin.user
        name_parts = (name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        user_field(user, 'name',
                   (str(first_name) + str(last_name)) or (str(name_parts[0]) + str(name_parts[2])))

        return DefaultSocialAccountAdapter.populate_user(self, request, sociallogin, data)
