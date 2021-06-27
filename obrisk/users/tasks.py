import requests
import datetime
import time
import oss2
import uuid
import logging

from django.core.cache import cache
from celery import shared_task
from slugify import slugify

from allauth.socialaccount.models import (
        SocialAccount, SocialLogin
    )
from obrisk.utils.images_upload import bucket
from obrisk.users.models import User


def upload_image(username, thumb, mid, full):
    try:
        thumbnail = requests.get(thumb, timeout=180)
        picture = requests.get(mid, timeout=180)
        org_picture = requests.get(full, timeout=180)

    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        logging.error("Failed to download social pic" + e)
        return None, None, None

    # naming them in our oss
    salt = uuid.uuid4().hex[:12]
    thumb_name = "media/images/profile_pics/" + slugify(
            str(username)
        ) + "/thumbnails/" + "thumb-" + salt + ".jpeg"
    pic_name = "media/images/profile_pics/" + slugify(
                str(username)
            ) + "/mid-thumbnails/" + "dp-" + salt + ".jpeg"
    org_pic_name = "media/images/profile_pics/" + slugify(
            str(username)
        ) + "/full-pic/" + "org-dp-" + salt + ".jpeg"

    # upoad them in our oss
    try:
        bucket.put_object(thumb_name, thumbnail.content)
        bucket.put_object(pic_name, picture.content)
        bucket.put_object(org_pic_name, org_picture.content)

    except Exception as e:
        logging.error("Failed to upload social Image" + e)

    return thumb_name, pic_name, org_pic_name


def update_prof_pic_sync(user, thumb, mid, full):
    """
    Runs the bg task to update user picture download it from
    social app and save it to our bucket
    It has to sleep for sometime or execution will fail
    """
    thumb_name, pic_name, picture = upload_image(user.username, thumb, mid, full)

    #saving and updating user credentials .
    user.thumbnail = thumb_name
    user.picture = pic_name
    user.org_picture = picture
    user.save()


@shared_task
def update_prof_pic_async(user_id, thumb, mid, full):
    """
    Runs the bg task to update user picture download it from
    social app and save it to our bucket
    It has to sleep for sometime for the view to save user to database
    """
    time.sleep(5)
    user = User.objects.get(id=user_id)

    thumb_name, pic_name, picture = upload_image(user.username, thumb, mid, full)
    #saving and updating user credentials .
    user.thumbnail = thumb_name
    user.picture = pic_name
    user.org_picture = picture
    user.save()
