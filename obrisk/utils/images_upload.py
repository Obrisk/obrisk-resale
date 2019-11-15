from django.contrib import messages
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from slugify import slugify

import json
import base64
import re
import os
import datetime

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from obrisk.classifieds.models import ClassifiedImages
from obrisk.stories.models import StoryImages

# STSGetting Started Tutorial See https://yq.aliyun.com/articles/57895
# STS's official documentation can be found at https://help.aliyun.com/document_detail/28627.html

# Initialize the information such as AccessKeyId, AccessKeySecret, and Endpoint.
# Get through environment variables, or replace something like "< your AccessKeyId>" with a real AccessKeyId.
# Note: AccessKeyId and AccessKeySecret are the keys of the sub-users.
# RoleArn can be viewed in the console under Access Control > Role Management > Administration > Basic Information > Arn.
#
# Taking the Hangzhou area as an example, the Endpoint can be
#   https://oss-cn-hangzhou.aliyuncs.com
# Access by HTTPS.

access_key_id = os.getenv('RAM_USER_ID')
access_key_secret = os.getenv('RAM_USER_S3KT_KEY')
bucket_name = os.getenv('OSS_BUCKET')
endpoint = os.getenv('OSS_ENDPOINT')
sts_role_arn = os.getenv('OSS_STS_ARN')
region = os.getenv('OSS_REGION')


class StsToken(object):
    """Temporary user key returned by AssumeRole
    :param str access_key_id: access user id of the temporary user
    :param str access_key_secret: temporary user's access key secret
    :param int expiration: expiration time, UNIX time, seconds from UTC zero on January 1, 1970
    :param str security_token: temporary user token
    :param str request_id: request ID
    """

    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        request_id = ''


def fetch_sts_token(access_key_id, access_key_secret, role_arn):
    """Sub User Role Playing to Get the Key of a Temporary User
    :param access_key_id: access key id of the subuser
    :param access_key_secret: subuser's access key secret
    :param role_arn: Arn of the STS role
    :return StsToken: temporary user key
    """

    try:        
        #Default timeout is 5 secs, but the server is far from alibaba data centers so increase it.
        #This is Tokyo data center.
        clt = client.AcsClient(access_key_id, access_key_secret, 'ap-northeast-1',
                             timeout=30, max_retry_time=3)
        
    except:
        try:
            #Retry again to get client authorization on different Alibaba data center (Hangzhou)
            clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou',
                                timeout=30, max_retry_time=3)
        except:
            return False

    try:
        #converting the clt results to json
        req = AssumeRoleRequest.AssumeRoleRequest()

        req.set_accept_format('json')
        req.set_RoleArn(role_arn)
        req.set_RoleSessionName('obriskdev-1330-oss-sts')
        body = clt.do_action_with_exception(req)
        j = json.loads(oss2.to_unicode(body))
    except:
        try:
            time.sleep(2)

            req = AssumeRoleRequest.AssumeRoleRequest()
            req.set_accept_format('json')
            req.set_RoleArn(role_arn)
            req.set_RoleSessionName('obriskdev-1330-oss-sts')

            body = clt.do_action_with_exception(req)
            j = json.loads(oss2.to_unicode(body))
        except:
            return False

    #Using the clt results to create an STSToken
    token = StsToken()

    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

    return token


bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

@login_required
@require_http_methods(["GET"])
def get_oss_auth(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
    
    if token == False:
        #for debugging on the logs
        print("WARNING: OSS STS initialization was not successful, please consider redesigning the infastructure!")
        #This is very bad, but we'll do it until we move the servers to China.
        #Send the alert email to developers (via celery) instead of logging.
        key_id = str(access_key_id)
        scrt = str(access_key_secret)
        data = {
            'direct': "true",
            'region': region,
            'accessId': key_id,
            'stsTokenKey': scrt,
            'bucket': bucket_name
        }
        return JsonResponse(data)

    else:
        key_id = str(token.access_key_id)
        scrt = str(token.access_key_secret)
        token_value = str(token.security_token)
        data = {
            'region': region,
            'accessKeyId': key_id,
            'accessKeySecret': scrt,
            'SecurityToken': token_value,
            'bucket': bucket_name
        }       
        return JsonResponse(data)


def multipleImagesPersist(request, images_list, app, obj):
    ''' This function takes the request, images list, app name (string) and app object
    and it validates the images list and saves the images to the database.
    It returns True if the images where saved to the db and False if there is a validation problem '''

    #The code from here onwards assume the first element of images list is undefined.
    #This variable will be used in the end of this code.
    tot_img_objs = len(images_list)

    if tot_img_objs < 1:
        obj.delete()
        return False

    #from here if you return form invalid then you have to prior delete the obj, obj.delete()
    #The current implementation will sucessfully create obj even when there are error on images
    #This is just to help to increase the app post on the website. The user shouldn't be discourage with errors
    #Also most of errors are caused by our frontend OSS when uploading the images so don't return invalid form to user.
    for index, str_result in enumerate(images_list):
        if str_result.startswith(f'{app}/{request.user.username}') == False:
            #Check if it was default image as it has no username.
            #This is the same default on all multiple upload apps
            #Though stories shouldn't have this, form shouldn't be submitted without images
            if (str_result != 'classifieds/error-img.jpg'):
                obj.delete()
                return False 
        
        d = str(datetime.datetime.now())

        if app == 'classifieds':
            img_obj = ClassifiedImages(classified=obj, image=str_result)
            thumb_name = "classifieds/" + slugify(str(obj.user)) + "/" + \
                    slugify(str(obj.title), allow_unicode=True, to_lower=True) + "/thumbnails/" + d + str(index)
            style = 'image/resize,m_fill,h_156,w_156'

        elif app == 'stories':
            #The image here is full url to the OSS bucket because of how it is consumed in the front-end
            img_obj = StoryImages(
                    story=obj, 
                    image='https://obrisk.oss-cn-hangzhou.aliyuncs.com/'+ str_result
                )
            thumb_name = "stories/" + slugify(str(obj.user)) + "/thumbnails/" + d + str(index)
            style = 'image/resize,m_fill,h_456,w_456'

        else:
            return False

        try:
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                        oss2.compat.to_string(base64.urlsafe_b64encode(
                                                            oss2.compat.to_bytes(thumb_name))),
                                                        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
            bucket.process_object(str_result, process)
        
        except oss2.exceptions.OssError as e:
            #Most likely this is our problem so save the image without the thumbnail:
            if index+1 == tot_img_objs:
                #To-do:
                #Take this image object to background task (celery) and retry to generate thumbnail
                #Send alert email to the developers
                messages.error(request, f"We are having difficulty processing your image(s), \
                    check your post if everything is fine. \
                    status= f{e.status}, requestID= f{e.request_id}")
                
            img_obj.image_thumb = str_result 
            img_obj.save()
            continue   

        except Exception:
            #If there is a problem with the thumbnail generation, most likely our code is wrong... 
            if index+1 == tot_img_objs:
                #To-do 
                #Pass the image object to background task and verify if image exist
                #and retry thumbnail creation
                #Send email to the developers
                messages.error(request, f"We are having difficulty processing your image(s), \
                    check your post if everything is fine.")
                
            img_obj.image_thumb = str_result 
            img_obj.save()
            continue   

        else:
            img_obj.image_thumb = thumb_name
            img_obj.save()

    return True