from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView
from django.views.generic.edit import BaseFormView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

from taggit.models import Tag
from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, OfficialAd, ClassifiedImages, OfficialAdImages
from obrisk.classifieds.forms import ClassifiedForm, OfficialAdForm

# For images
import json
import re
import os
import base64
import datetime

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from obrisk.helpers import ajax_required

from dal import autocomplete

# The following code shows the usage of STS, including role-playing to get the temporary user's key and using the temporary user's key to access the OSS.

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


@login_required
@require_http_methods(["GET"])
def classified_list(request, tag_slug=None):
    classifieds_list = Classified.objects.get_active().filter(city=request.user.city)
    popular_tags = Classified.objects.get_counted_tags()
    images = ClassifiedImages.objects.all()
    other_classifieds = Classified.objects.none()
    official_ads = OfficialAd.objects.all() 

    paginator = Paginator(classifieds_list, 30)  # 30 classifieds in each page
    page = request.GET.get('page')

    try:
        classifieds = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        classifieds = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():            
            # If the request is AJAX and the page is out of range
            # return an empty page            
            return HttpResponse('')
        # If page is out of range deliver last page of results
        classifieds = paginator.page(paginator.num_pages) 
    # When the last page user can see only fifty classifieds in other cities. To improve this near future.
    if page:
        if int(page) == paginator.num_pages:
            other_classifieds = Classified.objects.exclude(city=request.user.city)[:30]
    else:
        #If the page is the first one and it is the only one show other_classifieds
        if paginator.num_pages == 1:
            other_classifieds = Classified.objects.exclude(city=request.user.city)[:30]
        
    # Deal with tags in the end to override other_classifieds.
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        classifieds = Classified.objects.get_active().filter(tags__in=[tag])
        other_classifieds = ClassifiedImages.objects.none()
    
    if request.is_ajax():        
       return render(request,'classifieds/classified_list_ajax.html',
                    {'page': page, 'classifieds': classifieds, 'other_classifieds': other_classifieds, 'official_ads': official_ads,
                   'images': images,'base_active': 'classifieds'})   
    
    return render(request, 'classifieds/classified_list.html',
                  {'page': page, 'classifieds': classifieds, 'other_classifieds': other_classifieds, 'official_ads': official_ads,
                   'tag': tag, 'images': images, 'popular_tags': popular_tags, 'base_active': 'classifieds'})

# class ExpiredListView(ClassifiedsListView):
#     """Overriding the original implementation to call the expired classifieds
#     list."""

#     def get_queryset(self, **kwargs):
#         return Classified.objects.get_expired()

class CreateOfficialAdView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = OfficialAd
    message = _("Your classified has been created.")
    form_class = OfficialAdForm
    template_name = 'classifieds/official_ad_create.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def Classified(self, request, *args, **kwargs):
        """
        Handles Classified requests, instantiating a form instance and its inline
        formsets with the passed Classified variables and then checking them for
        validity.
        """
        form = OfficialAdForm(self.request.Classified)

        if form.is_valid():
            return self.form_valid(form)
        else:
            # ret = dict(errors=form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        classified.user = self.request.user
        classified.save()

        bucket = oss2. Bucket(oss2. Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        images_json = form.cleaned_data['images']

        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")

        for index, str_result in enumerate(images_list):
            if index == 0:
                continue
            img = ClassifiedImages(image=str_result)
            img.classified = classified

            d = str(datetime.datetime.now())
            thumb_name = "Official-ads/" + str(classified.user) + "/" + \
                str(classified.title) + "/thumbnails/" + d + str(index)
            style = 'image/resize,m_fill,h_156,w_156'
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                          oss2.compat.to_string(base64.urlsafe_b64encode(
                                                              oss2.compat.to_bytes(thumb_name))),
                                                          oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
            bucket.process_object(str_result, process)
            img.image_thumb = thumb_name

            img.save()

        return super(CreateClassifiedView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class CreateClassifiedView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = Classified
    message = _("Your classified has been created.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_create.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)
        

    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        classified.user = self.request.user
        classified.save()

        bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        images_json = form.cleaned_data['images']

        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")

        try:
            for index, str_result in enumerate(images_list):
                if index == 0:
                    continue
                img = ClassifiedImages(image=str_result)
                img.classified = classified

                d = str(datetime.datetime.now())
                thumb_name = "classifieds/" + str(classified.user) + "/" + \
                    str(classified.title) + "/thumbnails/" + d + str(index)
                style = 'image/resize,m_fill,h_156,w_156'
                process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                              oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                  oss2.compat.to_bytes(thumb_name))),
                                                              oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(str_result, process)
                img.image_thumb = thumb_name

                img.save()

            return super(CreateClassifiedView, self).form_valid(form)

        except oss2.exceptions.ServerError as e:
            messages.error(self.request, "Oops we are very sorry. \
            It looks like it took long to upload the images for your ad. \
            Please ensure your internet connection is stable and try again. "
                           + 'status={0}, request_id={1}'.format(e.status, e.request_id))
            # return self.form_invalid(form)
            classified.update(status="Expired")
            return redirect ('classifieds:list')
        
        except:
            messages.error(self.request, "Oops we are very sorry! your classified ad \
            was not created successfully. Please try again later")
            # return self.form_invalid(form)
            classified.update(status="Expired")
            return redirect ('classifieds:list')

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


@login_required
@require_http_methods(["GET"])
def get_oss_auth(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
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


@method_decorator(login_required, name='dispatch')
class TagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class EditClassifiedView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing classifieds."""
    model = Classified
    message = _("Your classified has been updated.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_update.html'

    # In this form there is an image that is not saved, deliberately since you can't upload images.
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

        classified_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_classified = Classified.objects.filter(tags__in=classified_tags_ids)\
            .exclude(id=self.object.id)

        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(classified=self.object.id)
        context['all_images'] = ClassifiedImages.objects.all()

        context['images_no'] = len(context['images'])
        context['similar_classifieds'] = similar_classified.annotate(same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:6]

        return context
