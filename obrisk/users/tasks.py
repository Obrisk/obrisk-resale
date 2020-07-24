import requests
import datetime
import time
import oss2
import uuid

from django.core.cache import cache
from celery import shared_task
from slugify import slugify

from allauth.socialaccount.models import (
        SocialAccount, SocialLogin
    )
from obrisk.utils.images_upload import bucket
from obrisk.users.models import User


def update_prof_pic_sync(user, thumb, mid, full):
    """
    Runs the bg task to update user picture download it from
    social app and save it to our bucket
    It has to sleep for sometime or execution will fail
    """
    try:
        # timeout is high because it is task.py
        thumbnail = requests.get(thumb, timeout=30)
        picture = requests.get(mid, timeout=30)
        org_picture = requests.get(full, timeout=30)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to download social pic" + e)
        return None

    # naming them in our oss
    salt = uuid.uuid4().hex[:12]
    thumb_name = "media/profile_pics/" + slugify(
            str(user.username)
        ) + "/thumbnails/" + "thumb-" + salt
    pic_name = "media/profile_pics/" + slugify(
            str(user.username)) + "/mid-thumbnails/" + "dp-" + salt
    org_pic_name = "media/profile_pics/" + slugify(
            str(user.username)
        ) + "/full-pic/" + "org-dp-" + salt

    # upoad them in our oss
    try:
        bucket.put_object(thumb_name, thumbnail.content)
        bucket.put_object(pic_name, picture.content)
        bucket.put_object(org_pic_name, org_picture.content)

    except (oss2.exceptions.ClientError,
            oss2.exceptions.RequestError) as e:
        logging.error("Failed to upload social Image" + e)

    else:
        #saving and updating user credentials .
        user.thumbnail = thumb_name
        user.picture = pic_name
        user.org_picture = picture
        user.save()


@shared_task
def update_profile_picture(user_id, socialapp):
    """
    Runs the bg task to update user picture download it from
    social app and save it to our bucket
    It has to sleep for sometime or execution will fail
    """
    time.sleep(1)
    user = User.objects.get(id=user_id)

    if socialapp == 'linkedin':

        thumbnail = user.socialaccount_set.all()[0] \
                .extra_data['profilePicture']['displayImage~'] \
                ['elements'][0]['identifiers'][0]['identifier']
        mid_size = user.socialaccount_set.all()[0] \
                .extra_data['profilePicture']['displayImage~'] \
                ['elements'][2]['identifiers'][0]['identifier']
        full_image = user.socialaccount_set.all()[0] \
                .extra_data['profilePicture']['displayImage~'] \
                ['elements'][3]['identifiers'][0]['identifier']

    elif socialapp == 'wechat':

        picture = cache.get(user.wechat_openid)
        thumbnail = picture[:-3] + '64'
        mid_size = picture
        full_image = picture[:-3] + '0'

    else:
        return None

    try:
        # timeout is high because it is task.py
        thumbnail = requests.get(thumbnail, timeout=30)
        picture = requests.get(mid_size, timeout=30)
        org_picture = requests.get(full_image, timeout=30)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to download social pic" + e)
        return None

    # naming them in our oss
    salt = uuid.uuid4().hex[:12]
    thumb_name = "media/profile_pics/" + slugify(
            str(user.username)
        ) + "/thumbnails/" + "thumb-" + salt
    pic_name = "media/profile_pics/" + slugify(
            str(user.username)) + "/mid-thumbnails/" + "dp-" + salt
    org_pic_name = "media/profile_pics/" + slugify(
            str(user.username)
        ) + "/full-pic/" + "org-dp-" + salt

    # upoad them in our oss
    try:
        bucket.put_object(thumb_name, thumbnail.content)
        bucket.put_object(pic_name, picture.content)
        bucket.put_object(org_pic_name, org_picture.content)

    except (oss2.exceptions.ClientError,
            oss2.exceptions.RequestError) as e:
        logging.error("Failed to upload social Image" + e)

    else:
        #saving and updating user credentials .
        user.thumbnail = thumb_name
        user.picture = pic_name
        user.org_picture = picture
        user.save()
