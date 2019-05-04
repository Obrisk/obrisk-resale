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
import oss2
import os
import os
import base64

# Create a bucket object, all Object related interfaces can be done through the Bucket object
# token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
# auth = oss2.StsAuth(token.access_key_id, token.access_key_secret, token.security_token)
# bucket = oss2.Bucket(auth, endpoint, bucket_name)


# Upload a string. The object name is motto.txt, and the content is a famous quote.
# bucket.put_object('motto.txt', 'Never give up. - Jack Ma')


# Download to local file
# Bucket.get_object_to_file('motto.txt', 'local motto.txt')


# Delete the object named motto.txt
# bucket.delete_object('motto.txt')


# Clear local files
# Os.remove(u'local motto.txt')

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

    def thumb_generator():
        style = 'image/crop,w_150,h_100,x_100,y_100,r_1'
        target_image_name = 'photo-crop.jpg'
        process = "{0}|sys/saveas,o_{1},b_{2}".format(style, 
        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(target_image_name))),
        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(taget_bucket_name))))
        result = bucket.process_object(source_image_name, process)
        print(result)


    def medium_generator():
        style = 'image/crop,w_350,h_550,x_100,y_100,r_1'
        target_image_name = 'photo-crop.jpg'
        process = "{0}|sys/saveas,o_{1},b_{2}".format(style, 
        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(target_image_name))),
        oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(taget_bucket_name))))
        result = bucket.process_object(source_image_name, process)
        print(result)

                  
    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        classified.user = self.request.user
        classified.save()

        for img in form.cleaned_data['images']:
                  
            img = ClassifiedImages(image = img, image_thumb = img, image_medium = img)
            img.classified = classified
            img.image_thumb =  thumb_generator
            img.image_medium = medium_generator        
            img.save()
        
        

        return super(CreateClassifiedView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


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


"""Access code used to generate a signed image processing URL"""
def oss_access():

    # Endpoint以杭州为例，其它Region请按实际情况填写。
    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    access_key_id = '<yourAccessKeyId>'
    access_key_secret = '<yourAccessKeySecret>'
    bucket_name = '<yourBucketName>'
    key = 'photo.jpg'

    # 创建存储空间实例，所有文件相关的方法都需要通过存储空间实例来调用。
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    # 上传示例图片。
    bucket.put_object_from_file(key, 'photo.jpg')

    # 生成带签名的URL，并指定过期时间为10分钟。过期时间单位是秒。
    style = 'image/resize,m_fixed,w_100,h_100/rotate,90'
    url = bucket.sign_url('GET', key, 10 * 60, params={'x-oss-process': style})
    print(url)
