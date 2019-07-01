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
from slugify import slugify

from taggit.models import Tag
from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, OfficialAd, ClassifiedImages, OfficialAdImages
from obrisk.classifieds.forms import ClassifiedForm, OfficialAdForm
from obrisk.classifieds import ststoken

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
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        classified.user = self.request.user
        classified.save()

        bucket = ststoken.bucket
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
            slugify(str(classified.title), allow_unicode=True, to_lower=True) + "/thumbnails/" + d + str(index)
            style = 'image/resize,m_fill,h_156,w_156'
            process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                          oss2.compat.to_string(base64.urlsafe_b64encode(
                                                              oss2.compat.to_bytes(thumb_name))),
                                                          oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(ststoken.bucket_name))))
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
        images_json = form.cleaned_data['images']

        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")

        if (images_list[1] == None):
            messages.error(self.request, "Sorry, the images were not uploaded successfully. \
                Please add the images again and submit the form!")
            return self.form_invalid(form)
        
        else:
            form.instance.user = self.request.user
            classified = form.save(commit=False)
            classified.user = self.request.user
            classified.save()

            for index, str_result in enumerate(images_list):
                if index == 0:
                    continue
                img = ClassifiedImages(image=str_result)
                img.classified = classified

                d = str(datetime.datetime.now())
                thumb_name = "classifieds/" + str(classified.user) + "/" + \
                slugify(str(classified.title), allow_unicode=True, to_lower=True) + "/thumbnails/" + d + str(index)
                style = 'image/resize,m_fill,h_156,w_156'
                
                try:
                    bucket = ststoken.bucket
                    process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                                oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                    oss2.compat.to_bytes(thumb_name))),
                                                                oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(ststoken.bucket_name))))
                    bucket.process_object(str_result, process)
                    img.image_thumb = thumb_name

                    img.save()

                    return super(CreateClassifiedView, self).form_valid(form)

                except oss2.exceptions.ServerError as e:
                    img.save()
                    messages.error(self.request, "Oops we are very sorry. \
                    Your images where not uploaded successfully. Please ensure that, \
                    your internet connection is stable and edit your item to add images. "
                                + 'status={0}, request_id={1}'.format(e.status, e.request_id))
                    # return self.form_invalid(form)
                    return redirect ('classifieds:list')
                
                except:
                    img.save()
                    messages.error(self.request, "Oops we are sorry! Your images \
                        where not uploaded successfully. Please select your item, then edit, \
                        and try again to upload the images.")
                    #return self.form_invalid(form)
                    return redirect ('classifieds:list')
        

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


@method_decorator(login_required, name='dispatch')
class TagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

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
