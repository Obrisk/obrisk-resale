from allauth.socialaccount.models import SocialAccount, SocialAccount
from celery import shared_task
from obrisk.users.models import User
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import requests
from slugify import slugify
from django.http import JsonResponse
import base64
import datetime
import oss2
from obrisk.users.models import User
from allauth.socialaccount.models import SocialAccount, SocialAccount, SocialLogin

#@shared_task
def update_social_user_profile_picture():
    '''
    required to add the background task to update user picture download it from
    Linkedin and save it to our bucket using requests package
    '''
    # Try to Get the list from cache
    # token = cache.get(f"")
    # get social user

    user = User.objects.all()
     
     # get  the user info from linkedin
    for ac in user.socialaccount_set.all():
        user_info = ac.extra_data
        mid_size = user_info['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']
        thumbnail = user_info['profilePicture']['displayImage~']['elements'][0]['identifiers'][0]['identifier']
        full_image = user_info['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier']
        
        # downloading the images
        thumbnail = requests.get(thumbnail)
        picture = requests.get(mid_size)
        org_picture = requests.get(full_image)
        
        # naming them in our oss
        d = str(datetime.datetime.now())
        thumb_name = "media/socialaccount/linkedin/thumb/profile_pics/" + slugify(str(user)) + "/thumbnails/" + "thumb-" + d 
        pic_name = "media/socialaccount/linkedin/pic/profile_pics/" + slugify(str(user)) + "/thumbnails" + "dp-" + d 
        name = "media/socialaccount/linkedin/org_pic/profile_pics/" + slugify(str(user)) + "/thumbnails" + "dp-" + d 
        org_pic_name
         
        # uploding them to the s3 buckect  
        bucket.put_object(thumbnail, thumb_name)
        bucket.put_object(picture, pic_name)
        bucket.put_object(org_pic, org_pic_name)
            
        # saving and updating user credentials .
        user.thumbnail = thumb_name
        user.picture = pic_name
        user.org_picture = picture
        user.save()
            
