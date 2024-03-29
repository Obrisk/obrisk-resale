import uuid
import json
import base64
import os
import datetime
import logging
import requests

from django.contrib import messages
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from slugify import slugify

import boto3
from botocore.exceptions import ClientError

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from obrisk.classifieds.models import ClassifiedImages, Classified
from obrisk.stories.models import StoryImages, Stories
from config.settings.base import env


# Initialize info e.g AccessKeyId, AccessKeySecret, and Endpoint.
# Get through environment variables,
# or replace something like "< your AccessKeyId>" with a real AccessKeyId.
# Note: AccessKeyId and AccessKeySecret are the keys of the sub-users.
# RoleArn can be viewed in the console under 
# Access Control > Role Management > Administration > Basic Information > Arn.
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
    :param int expiration: UNIX time, secs from UTC zero/Jan 1, 1970
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
        #Default timeout is 5 secs, but the server is far from aliyun
        #This is north China, there are 3 more data centers. try others
        clt = client.AcsClient(
                access_key_id, access_key_secret,
                'cn-beijing',timeout=30, max_retry_time=3)

    except Exception as e:
        logging.error(e)
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

        except Exception as e:
            logging.error(e)
            return False

        else:
            #Using the clt results to create an STSToken
            token = StsToken()

            token.access_key_id = j['Credentials']['AccessKeyId']
            token.access_key_secret = j['Credentials']['AccessKeySecret']
            token.security_token = j['Credentials']['SecurityToken']
            token.request_id = j['RequestId']
            token.expiration = oss2.utils.to_unixtime(
                    j['Credentials']['Expiration'],
                    '%Y-%m-%dT%H:%M:%SZ'
                )
            return token


bucket = oss2.Bucket(oss2.Auth(
        access_key_id, access_key_secret
    ), endpoint, bucket_name)


def generate_sts_credentials(request):
    '''By default it returns the sts to perform put on s3 bucket'''

    # create an STS client object that represents a live connection to the 
    # STS service
    sts_client = boto3.client('sts',
          aws_access_key_id=os.getenv('AWS_STATIC_S3_KEY_ID'),
          aws_secret_access_key=os.getenv('AWS_STATIC_S3_S3KT'),
          region_name=os.getenv('AWS_S3_REGION_NAME')
      )

    try:
        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        session_name = slugify(f"{request.user.username}-{uuid.uuid4().hex[:8]}")

        assumed_role_object=sts_client.assume_role(
            RoleArn=os.getenv('AWS_S3_MEDIA_BUCKET_ARN'),
            RoleSessionName=session_name,
            ExternalId=os.getenv('AWS_S3_ROLE_EXTERNALID'),
            DurationSeconds=1800
        )

    except ClientError as e:
        logging.error(e)
        return None
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    # credentials are as a Python dictionary, so can be served to JS directly
    return assumed_role_object['Credentials']


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
    s3_client = boto3.client('s3',
          aws_access_key_id=os.getenv('AWS_STATIC_S3_KEY_ID'),
          aws_secret_access_key=os.getenv('AWS_STATIC_S3_S3KT'),
          region_name=os.getenv('AWS_S3_REGION_NAME')
    )
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields return response


@login_required
@require_http_methods(["GET"])
def get_oss_auth(request, app_name=None):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""

    error_data = {
        'status': 'failed',
        'errorMessage': 'The request requires the object name to be uploaded \
        but no name was supplied'
    }

    if app_name == 'stories.video' and env.bool('VIDEO_USE_AWS_MEDIA'):
        data = generate_sts_credentials(request)

        if data is None:
            return JsonResponse(error_data)
        return JsonResponse(data)

    else:
        token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)

        if token is False:
            #This is very bad, but we'll do it until we move the servers to China.
            #logging this event
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
    ''' This func takes request, images list,
    app name (string) and app object
    and it validates the images list and stores them to the database.
    It returns images objects list if the images where saved to the db
    False if there is a validation problem '''

    #The code from here onwards assume the first element of images list is undefined.
    #This variable will be used in the end of this code.
    tot_img_objs = len(images_list)

    if tot_img_objs < 1:
        obj.delete()
        return False

    #from here if you return form invalid
    #then you have to prior delete the obj, obj.delete()
    #The current implementation will sucessfully create obj
    #even when there are error on images
    #This is just to help to increase the app post on the website.
    img_mid_name = None
    saved_objs = 0
    display_img= None
    username = slugify(request.user.username, to_lower=True)
    title = slugify(obj.title, to_lower=True)

    for index, str_result in enumerate(images_list):
        if str_result.startswith(
                f'media/images/{app}/') is False:
            #Check if it was default image as it has no username.
            #This is the same default on all multiple upload apps
            #Though form shouldn't be submitted without images
            if (str_result != 'classifieds/error-img.jpg'):
                obj.delete()
                return False

        d = str(datetime.datetime.now())

        if app == 'classifieds':
            img_obj = ClassifiedImages(classified=obj, image=str_result)
            thumb_name = "media/images/classifieds/" + username + "/" + title + "/" + d + "/thumbnails/" + str(index) + ".jpeg" #noqa
            img_mid_name = "media/images/classifieds/" + username + "/" + title + "/" + d + "/mid-size/" + str(index) + ".jpeg" #noqa
            style = 'image/resize,m_fill,h_156,w_156'
            style_mid = 'image/resize,m_pad,h_400'
            #style_mid = 'image/resize,m_fill,h_400'

        elif app == 'stories':
            #The image here is full url to the OSS bucket
            #because of how it is consumed in the front-end
            img_obj = StoryImages(
                story=obj,
                image='https://obrisk.oss-cn-hangzhou.aliyuncs.com/'+ str_result #noqa
            )
            thumb_name = "media/images/stories/" + username + "/thumbnails/" + d + str(index)
            style = 'image/resize,m_fill,h_456,w_456'

        else:
            return False

        if env.bool('USE_AWS_S3_MEDIA', default=False):
            #First verify that the lambda has finish creating thumbnail
            #Then save
            #img_obj.image_thumb = thumb_name
            if img_mid_name:
                img_obj.image_mid_size = img_mid_name
            img_obj.save()
            saved_objs += 1
            return  'https://obrisk.oss-cn-hangzhou.aliyuncs.com/'+ images_list[0]

        else:
            try:
                process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                    oss2.compat.to_string(base64.urlsafe_b64encode(
                        oss2.compat.to_bytes(thumb_name))),
                    oss2.compat.to_string(
                        base64.urlsafe_b64encode(
                            oss2.compat.to_bytes(bucket_name)
                        )
                    )
                )
                bucket.process_object(str_result, process)

                if app == 'classifieds':
                    process = "{0}|sys/saveas,o_{1},b_{2}".format(style_mid,
                        oss2.compat.to_string(base64.urlsafe_b64encode(
                            oss2.compat.to_bytes(img_mid_name))),
                        oss2.compat.to_string(
                            base64.urlsafe_b64encode(
                                oss2.compat.to_bytes(bucket_name)
                                )
                            )
                        )
                    bucket.process_object(str_result, process)

            except oss2.exceptions.NoSuchKey as e:
                obj.delete()
                return False

            except Exception as e:
                #If there is a problem with the thumbnail generation,
                #our code is wrong
                if index+1 == tot_img_objs:
                    #To-do 
                    #retry thumbnail creation
                    #Send email to the developers
                    logging.error(e)
                    messages.error(
                        request, f"We are having difficulty processing your image(s), \
                        check your post if everything is fine.")

                img_obj.image_thumb = str_result
                if img_mid_name:
                    img_obj.image_mid_size = str_result
                img_obj.save()
                saved_objs += 1
                continue

            else:
                img_obj.image_thumb = thumb_name
                if saved_objs == 0:
                    obj.thumbnail = thumb_name
                    obj.save()
                if img_mid_name:
                    img_obj.image_mid_size = img_mid_name
                img_obj.save()
                saved_objs += 1

    if app == 'stories':
        obj.images_count = saved_objs
        obj.save()
        return 'https://obrisk.oss-cn-hangzhou.aliyuncs.com/'+ images_list[0]
    else:
        return True


def videoPersist(request, video, app, obj):
    ''' Takes the request, video str, app name (str) and app object
    and it validates the video string and stores them to the database.
    It returns True if the video is authentic
    False if there is a validation problem '''

    if env.bool('VIDEO_USE_AWS_MEDIA'):
        if video.startswith(
                f'media/videos/{app}/{request.user.username}/'
            ) is False:
            obj.delete()
            return False

        response = client.head_object(
            Bucket=os.getenv('AWS_S3_MEDIA_BUCKET_NAME'),
            Key=video,
        )

        #if something in print(response)
        obj.video = video
        obj.save()
        return True

    else:
        #For Aliyun OSS:
        try:
            #simplifiedmeta = bucket.get_object_meta(video)
            #print(simplifiedmeta.headers['Last-Modified'])
            #if int(simplifiedmeta.headers['Content-Length']) > 0:

            display_pic = requests.get(
                "https://obrisk.oss-cn-hangzhou.aliyuncs.com/" + \
                video + "?x-oss-process=video/snapshot,t_5000,f_jpg,w_800,h_600,m_fast", # noqa
                timeout=5
            )

        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
            return False
            logging.error("Can't request thumbnail from video" + e)

        # naming them in our oss
        pic_name = f'media/images/{app}/' + slugify(
                str(request.user.username)
            ) + "/video-display-thumb-" + uuid.uuid4().hex[:16]

        # upoad them in our oss
        try:
            bucket.put_object(pic_name, display_pic.content)

        except (oss2.exceptions.ClientError,
                oss2.exceptions.RequestError) as e:
            logging.error("Can't upload thumbnail for video" + e)

        else:
            StoryImages.objects.create(
                 story=obj,
                 image = pic_name,
                 image_thumb = pic_name
            )

        obj.video = video
        obj.save()
        return pic_name


@login_required
@require_http_methods(["GET"])
def bulk_update_classifieds_thumb(request):
    """Function to update all images objects to have
    the mid size image."""
    cls = Classified.objects.all()

    for cl in cls:
        img = ClassifiedImages.objects.filter(classified=cl).first()
        if img is not None:
            cl.thumbnail = img.image_thumb
            cl.save()

    return redirect('classifieds:list')


@login_required
@require_http_methods(["GET"])
def bulk_update_vid_images(request):
    """Function to update all images objects to have
    the mid size image."""
    strs = Stories.objects.exclude(
            video__isnull=True
        ).exclude(video__exact='')

    for story in strs:
        try:
            #simplifiedmeta = bucket.get_object_meta(video)
            #print(simplifiedmeta.headers['Last-Modified'])
            #if int(simplifiedmeta.headers['Content-Length']) > 0:
            video = story.video
            app = 'stories'

            display_pic = requests.get(
                "https://obrisk.oss-cn-hangzhou.aliyuncs.com/" + \
                video + "?x-oss-process=video/snapshot,t_5000,f_jpg,w_800,h_600,m_fast", # noqa
                timeout=5
            )

        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
            logging.error("Can't request thumbnail from video" + e)

        # naming them in our oss
        pic_name = f'media/images/{app}' + slugify(
                str(story.user.username)
            ) + '/video-display-thumb-' + uuid.uuid4().hex[:12]

        # upoad them in our oss
        try:
            bucket.put_object(pic_name, display_pic.content)

        except (oss2.exceptions.ClientError,
                oss2.exceptions.RequestError) as e:
            logging.error("Can't upload thumbnail for video" + e)

        else:
            StoryImages.objects.create(
                 story=story,
                 image_thumb = pic_name
            )

    return redirect('classifieds:list')
