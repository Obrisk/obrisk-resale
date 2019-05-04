from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView
from django.views.generic.edit import BaseFormView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django import forms

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.classifieds.forms import ClassifiedForm
import json
import re
import os

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

import oss2

#For images
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from obrisk.helpers import ajax_required

import oss2
import base64




# The following code shows the usage of STS, including role-playing to get the temporary user's key and using the temporary user's key to access the OSS.

# STSGetting Started Tutorial See https://yq.aliyun.com/articles/57895
# STS's official documentation can be found at https://help.aliyun.com/document_detail/28627.html

# Initialize the information such as AccessKeyId, AccessKeySecret, and Endpoint.
# Get through environment variables, or replace something like "< your AccessKeyId>" with a real AccessKeyId.
# Note: AccessKeyId and AccessKeySecret are the keys of the sub-users.
# RoleArn can be viewed in the console under Access Control > Role Management > Administration > Basic Information > Arn.
#
# Taking the Hangzhou area as an example, the Endpoint can be:
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# Access by HTTP and HTTPS respectively.


access_key_id = os.getenv('OSS_STS_ID')
access_key_secret = os.getenv('OSS_STS_KEY')
bucket_name = os.getenv('OSS_BUCKET')
endpoint = os.getenv('OSS_ENDPOINT')
sts_role_arn = os.getenv('OSS_STS_ARN')

# Confirm that the above parameters are filled in correctly.
for param in (access_key_id, access_key_secret, bucket_name, endpoint, sts_role_arn):
    print(param)


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
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    req = AssumeRoleRequest.AssumeRoleRequest()

    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('oss-python-sdk-example')

    body = clt.do_action_with_exception(req)

    j = json.loads(oss2.to_unicode(body))

    token = StsToken()

    token.access_key_id = j['Credentials']['AccessKeyId']
    token.access_key_secret = j['Credentials']['AccessKeySecret']
    token.security_token = j['Credentials']['SecurityToken']
    token.request_id = j['RequestId']
    token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

    return token

class ClassifiedsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published classifieds list."""
    model = Classified
    paginate_by = 15
    context_object_name = "classifieds"

    def get_context_data(self, *args, **kwargs):
        context = super(ClassifiedsListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Classified.objects.get_counted_tags()
        context['images'] = ClassifiedImages.objects.all()
        context['other_classifieds'] = Classified.objects.exclude(city= self.request.user.city)
        context['image_thumb'] = ClassifiedImages.image_thumb
        context['image_medium'] = ClassifiedImages.image_medium
        return context

    def get_queryset(self, **kwargs):
        return Classified.objects.get_active().filter(city= self.request.user.city)


class ExpiredListView(ClassifiedsListView):
    """Overriding the original implementation to call the expired classifieds
    list."""
    def get_queryset(self, **kwargs):
        return Classified.objects.get_expired()


class CreateClassifiedView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = Classified
    message = _("Your classified has been created.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_create.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        form = ClassifiedForm(self.request.POST)
    
        if form.is_valid():
            return self.form_valid(form)
        else:
            #ret = dict(errors=form.errors)
            print(form.errors)
            return self.form_invalid(form)


                  
    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        classified.user = self.request.user
        classified.save()

        bucket = oss2. Bucket(oss2. Auth(access_key_id, access_key_secret), endpoint, bucket_name)

        for img in form.cleaned_data['images']:
                  
            img = ClassifiedImages(image = img)
            img.classified = classified

            style = 'image/crop,w_140,h_140,x_140,y_140,r_1'
            bucket_name = img
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style, 
            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))),
            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
            img.image_thumb = bucket.process_object(img, process)
            
            style = 'image/crop,w_250,h_250,x_250,y_250,r_1'
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style, 
            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))),
            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
            img.image_medium = bucket.process_object(img, process)
        
            img.save()
        
        return super(CreateClassifiedView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')

@login_required
@ajax_required
@require_http_methods(["POST"])
def get_oss_auth(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
    
    return render(request, 'messager/single_message.html', {
        'accessKeyId': access_key_id,
        'accessKeySecret':access_key_secret, 
        'SecurityToken': token
    })

class EditClassifiedView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing classifieds."""
    model = Classified
    message = _("Your classified has been updated.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_update.html'

    #In this form there is an image that is not saved, deliberately since you can't upload images.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')

class ReportClassifiedView(LoginRequiredMixin, View):
    """This class has to inherit FormClass model but failed to implement that
    Update view will use the model Classified which is not a nice implementation.
    There is no need of a model here just render a form and the send email. """

    message = _("Your report has been submitted.")
    template_name = 'classifieds/classified_report.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class DetailClassifiedView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual classified."""
    model = Classified

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailClassifiedView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(classified=self.object.id)
        return context
