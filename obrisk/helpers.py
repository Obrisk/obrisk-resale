from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import json
import re
import os
import time

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods


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
        self.request_id = ''


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

#@login_required
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
        #No one will try to hunt our code in this beginning.
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


def paginate_data(qs, page_size, page, paginated_type, **kwargs):
    """Helper function to turn many querysets into paginated results at
    dispose of our GraphQL API endpoint."""
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)

    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def ajax_required(f):
    """Not a mixin, but a nice decorator to validate than a request is AJAX"""
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class AuthorRequiredMixin(View):
    """Mixin to validate than the loggedin user is the creator of the object
    to be edited or updated."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)



