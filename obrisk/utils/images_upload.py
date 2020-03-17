from django.contrib import messages
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from slugify import slugify

import json
import base64
import re
import os
import datetime

import logging
import boto3
from botocore.exceptions import ClientError

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
        return False
    
    else:
        try:
            #converting the clt results to json
            req = AssumeRoleRequest.AssumeRoleRequest()
            req.set_accept_format('json')
            req.set_RoleArn(role_arn)
            req.set_RoleSessionName('obriskdev-1330-oss-sts')
            body = clt.do_action_with_exception(req)
            j = json.loads(oss2.to_unicode(body))
        except:
            return False
        
        else:
            #Using the clt results to create an STSToken
            token = StsToken()

            token.access_key_id = j['Credentials']['AccessKeyId']
            token.access_key_secret = j['Credentials']['AccessKeySecret']
            token.security_token = j['Credentials']['SecurityToken']
            token.request_id = j['RequestId']
            token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

            return token


bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)



def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response



def create_presigned_url_expanded(client_method_name, method_parameters=None,
                                  expiration=3600, http_method=None):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(ClientMethod=client_method_name,
                                                    Params=method_parameters,
                                                    ExpiresIn=expiration,
                                                    HttpMethod=http_method)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response



@login_required
@require_http_methods(["GET"])
def get_oss_auth(request, object_name=None):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    
    if os.getenv('AWS_S3_MEDIA'):
        if object_name is None:
            data = {'status': 'failed',
                    'errorMessage': 'The request requires the object name to be uploaded \
                    but no name was supplied'}
            return JsonResponse(data)

        data = create_presigned_post(os.getenv('AWS_S3_MEDIA_BUCKET_NAME'), object_name,
                            fields=None, conditions=None, expiration=3600)
        
        return JsonResponse(data)

    else:
        token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
        
        if token == False:
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
    and it validates the images list and stores them to the database. 
    It returns images objects list if the images where saved to the db
    False if there is a validation problem '''

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
    img_mid_name = None
    saved_objs = []
    
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
            img_mid_name = "classifieds/" + slugify(str(obj.user)) + "/" + \
                    slugify(str(obj.title), allow_unicode=True, to_lower=True) + "/mid-size/" + d + str(index)
            style = 'image/resize,m_fill,h_156,w_156'
            style_mid = 'image/resize,m_fill,h_400'

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
        
            if app == 'classifieds':
                process = "{0}|sys/saveas,o_{1},b_{2}".format(style_mid,
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                oss2.compat.to_bytes(img_mid_name))),
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(str_result, process)
        
        except oss2.exceptions.NoSuchKey as e:
            obj.delete()
            return False

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
            if img_mid_name:
                img_obj.image_mid_size = str_result
            img_obj.save()
            saved_objs.append(img_obj)
            continue   

        else:
            img_obj.image_thumb = thumb_name
            if img_mid_name:
                img_obj.image_mid_size = img_mid_name
            img_obj.save()
            saved_objs.append(img_obj)

    return saved_objs 

def videoPersist(request, video, app, obj):
    ''' Function takes the request, video string, app name (string) and app object
    and it validates the video string and stores them to the database. 
    It returns True if the video is authentic
    False if there is a validation problem '''

    if video.startswith(f'{app}/videos/{request.user.username}') == False or len(video) < 10:
        obj.delete()
        return False

    try:
        simplifiedmeta = bucket.get_object_meta(video)
        print(simplifiedmeta.headers['Last-Modified'])
        print(simplifiedmeta.headers['Content-Length'])
    
    except oss2.exceptions.NoSuchKey:
        obj.delete() 
        return False

    except Exception:
        obj.video = video
        obj.save()
        return True

    obj.video = video
    obj.save()
    return True

@login_required
@require_http_methods(["GET"])
def bulk_update_classifieds_mid_images(request):
    """Function to update all images objects to have 
    the mid size image."""
    imgs = ClassifiedImages.objects.all()

    for index, img in enumerate(imgs):
        d = str(datetime.datetime.now())
        
        img_mid_name = "classifieds/" + slugify(str(img.classified.user)) + "/" + \
                slugify(str(img.classified.title), allow_unicode=True, to_lower=True) + "/mid-size/" + d + str(index)
        
        style_mid = 'image/resize,m_fill,h_400'

        try:
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style_mid,
                                                        oss2.compat.to_string(base64.urlsafe_b64encode(
                                                            oss2.compat.to_bytes(img_mid_name))),
                                                        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
            bucket.process_object(img.image, process)

        
        except oss2.exceptions.NoSuchKey as e:
            messages.error(request, f"Object with details doesn't exist {e}")
            return HttpResponse("Error in updating mid-size-classifieds images!", content_type='text/plain')
        except Exception as e:
            messages.error(request, "This is trouble, restart the process!")
            return HttpResponse("Error in updating mid-size-classifieds images!", content_type='text/plain')
        else:
            img.image_mid_size = img_mid_name 
            img.save()

    return redirect('classifieds:list')






