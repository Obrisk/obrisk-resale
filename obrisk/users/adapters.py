import requests
import datetime

from obrisk.utils.images_upload import bucket
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError
from django.conf import settings
from allauth.account.utils import user_field
# from django.contrib.auth import get_user_model
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

    def pre_social_login(self, request, sociallogin):

        social_user = sociallogin.user
        if not social_user.picture:
            # downloading the images
            usr = social_user.socialaccount_set.all()[0].extra_data['profilePicture']
            thumbnail = usr['displayImage~']['elements'][0]['identifiers'][0]['identifier']
            mid_size = usr['displayImage~']['elements'][2]['identifiers'][0]['identifier']
            full_image = usr['displayImage~']['elements'][3]['identifiers'][0]['identifier']

            thumbnail = requests.get(thumbnail)
            picture = requests.get(mid_size)
            org_picture = requests.get(full_image)

            # naming them in our oss
            d = str(datetime.datetime.now())
            thumb_name = "media/profile_pics/" + slugify(str(social_user)) + "/thumbnails/" + "thumb-" + d
            pic_name = "media/profile_pics/" + slugify(str(social_user)) + "/thumbnails" + "dp-" + d
            org_pic_name = "media/profile_pics/" + slugify(str(social_user)) + "/thumbnails" + "org-dp-" + d

            # upoad them in our oss
            bucket.put_object(thumb_name, thumbnail.content)
            bucket.put_object(pic_name, picture.content)
            bucket.put_object(org_pic_name, org_picture.content)

            # saving and updating user credentials .
            social_user.thumbnail = thumb_name
            social_user.picture = pic_name
            social_user.org_picture = picture
            social_user.save()


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
