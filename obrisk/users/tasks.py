import requests, datetime, time

from celery import shared_task
from slugify import slugify

from allauth.socialaccount.models import SocialAccount, SocialLogin
from obrisk.utils.images_upload import bucket
from obrisk.users.models import User


@shared_task
def update_profile_picture(user_id):
    '''
    A function to add the background task to update user picture download it from
    Linkedin and save it to our bucket using requests package
    '''
    time.sleep(1)
    # get  the user object
    user = User.objects.get(id=user_id)
    # check if the user is a social user and get the info from linkedin
    if user.socialaccount_set.all() and not user.picture:
        mid_size = user.socialaccount_set.all()[0].extra_data['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']
        thumbnail = user.socialaccount_set.all()[0].extra_data['profilePicture']['displayImage~']['elements'][0]['identifiers'][0]['identifier']
        full_image = user.socialaccount_set.all()[0].extra_data['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier']

        # downloading the images
        thumbnail = requests.get(thumbnail)
        picture = requests.get(mid_size)
        org_picture = requests.get(full_image)

        # naming them in our oss
        d = str(datetime.datetime.now())
        thumb_name = "media/profile_pics/" + slugify(str(user)) + "/thumbnails/" + "thumb-" + d
        pic_name = "media/profile_pics/" + slugify(str(user)) + "/thumbnails" + "dp-" + d
        org_pic_name = "media/profile_pics/" + slugify(str(user)) + "/thumbnails" + "org-dp-" + d

        # upoad them in our oss
        bucket.put_object(thumb_name, thumbnail.content)
        bucket.put_object(pic_name, picture.content)
        bucket.put_object(org_pic_name, org_picture.content)

        #saving and updating user credentials .
        user.thumbnail = thumb_name
        user.picture = pic_name
        user.org_picture = picture
        user.save()
