from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError
from django.conf import settings
from allauth.account.utils import user_field

class AccountAdapter(DefaultAccountAdapter):

    def clean_username(self, username, **kwargs):
        if len(username) > getattr(settings, 'ACCOUNT_USERNAME_MAX_LENGTH', 16):
            raise ValidationError('The username length must be less than 16 characters')
        return DefaultAccountAdapter.clean_username(self, username, **kwargs)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def authentication_error(self, request, provider_id, error, exception, extra_context):
        ''' This is for debugging when there is a failure
        linked with the provider'''

        # print(provider_id)
        # print(error.__str__())
        # print(exception.__str__())
        # print(extra_context)
        pass

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
