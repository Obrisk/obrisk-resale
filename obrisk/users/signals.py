from django.shortcuts import redirect
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

import requests
from slugify import slugify
import datetime
from obrisk.utils.images_upload import bucket


@receiver(user_signed_up)
def social_user_connected(user, **kwargs):
    ''' when triggerd, it initiates update profile picture which formerly
        was done as backgroundnd task and redirects to the homepage
    '''

    # checking extra_data and user profile pic
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
        thumb_name = "media/profile_pics/" + slugify(str(user.username)) + "/thumbnails/" + "thumb-" + d
        pic_name = "media/profile_pics/" + slugify(str(user.username)) + "/thumbnails" + "dp-" + d
        org_pic_name = "media/profile_pics/" + slugify(str(user.username)) + "/thumbnails" + "org-dp-" + d

        # upoad them in our oss
        bucket.put_object(thumb_name, thumbnail.content)
        bucket.put_object(pic_name, picture.content)
        bucket.put_object(org_pic_name, org_picture.content)

        #saving and updating user credentials .
        user.thumbnail = thumb_name
        user.picture = pic_name
        user.org_picture = picture
        user.save()

        return redirect("stories:list")
    else:
        return redirect("stories:list")
