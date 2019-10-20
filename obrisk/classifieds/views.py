from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import BaseFormView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.db.models import OuterRef, Subquery, Case, When, Value, IntegerField
from django.urls import reverse_lazy
from django.core.mail import send_mail
from slugify import slugify

from taggit.models import Tag
from obrisk.utils.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, OfficialAd, ClassifiedImages, OfficialAdImages
from obrisk.classifieds.forms import ClassifiedForm, OfficialAdForm, ClassifiedEditForm
from obrisk.utils.images_upload import multipleImagesPersist

# For images
import json
import re
import base64
import datetime

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from obrisk.utils.helpers import ajax_required

from dal import autocomplete

TAGS_TIMEOUT = getattr(settings, 'TAGS_CACHE_TIMEOUT', DEFAULT_TIMEOUT)

@login_required
@require_http_methods(["GET"])
def set_popular_tags(request):
    popular_tags = Classified.objects.get_counted_tags()[:30]

    cache.set('popular_tags', list(popular_tags), timeout=TAGS_TIMEOUT)

    return HttpResponse("Successfully sorted the popular tags!", content_type='text/plain')


#People can view without login
@require_http_methods(["GET"])
def classified_list(request, tag_slug=None):
    if request.user.is_authenticated:
        city = request.user.city
    else:
        city = "Hangzhou"
    
    #Try to Get the popular tags from cache
    popular_tags = cache.get('popular_tags')

    if popular_tags == None:
        popular_tags = Classified.objects.get_counted_tags()
    
    #Get classifieds
    classifieds_list = Classified.objects.get_active().annotate(
        order = Case (
            When(city=city, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).annotate (
        image_thumb = Subquery (
            ClassifiedImages.objects.filter(
                classified=OuterRef('pk'),
            ).values(
                'image_thumb'
            )[:1]
        )
    ).order_by('order', '-priority', '-timestamp')

    #official_ads = OfficialAd.objects.all() 

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
        
    # Deal with tags in the end to override other_classifieds.
    tag = None
    if tag_slug:

        tag = get_object_or_404(Tag, slug=tag_slug)
        classifieds = Classified.objects.get_active().filter(tags__in=[tag]).annotate (
            image_thumb = Subquery (
                ClassifiedImages.objects.filter(
                    classified=OuterRef('pk'),
                ).values(
                    'image_thumb'
                )[:1]
            )
        ).order_by('-timestamp')
    
    if request.is_ajax():        
       return render(request,'classifieds/classified_list_ajax.html',
                    {'page': page, 'popular_tags': popular_tags,
                    'classifieds': classifieds, 'base_active': 'classifieds'})   
    
    return render(request, 'classifieds/classified_list.html', 
                {'page': page, 'popular_tags': popular_tags,
                'classifieds': classifieds, 'tag': tag, 'base_active': 'classifieds'})

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

        images_json = form.cleaned_data['images']

        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")

        if multipleImagesPersist(self.request, images_list, 'classifieds', classified):
            return super(CreateOfficialAdView, self).form_valid(form)
        else:
            return self.form_invalid(form)

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
        img_errors = form.cleaned_data['img_error']

        form.instance.user = self.request.user
        classified = form.save(commit=False)
        classified.user = self.request.user
        
        if self.request.user.address: 
            classified.address = self.request.user.address
        else:
            classified.address = form.cleaned_data['address']
        
        classified.save()

        if img_errors:
            #In the near future, send a message like sentry to our mailbox to notify about the error!
            send_mail('JS ERRORS ON IMAGE UPLOADING', str(img_errors) , 'errors@obrisk.com', ['admin@obrisk.com',])
        
        if not images_json:
            #For security Images must be there even if there is an error
            return self.form_invalid(form)

        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")

        if multipleImagesPersist(self.request, images_list, 'classifieds', classified):    
            return super(CreateClassifiedView, self).form_valid(form)
        else:
            return self.form_invalid(form)

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
    form_class = ClassifiedEditForm
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



class ClassifiedDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""
    model = Classified
    message = _("Your classified post has been deleted successfully!")
    success_url = reverse_lazy("classifieds:list")


    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. This method is called by post.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status="E"
        self.object.save()
        return HttpResponseRedirect(success_url)



class DetailClassifiedView(DetailView):
    """Basic DetailView implementation to call an individual classified."""
    model = Classified

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailClassifiedView, self).get_context_data(**kwargs)

        classified_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_classifieds = Classified.objects.filter(tags__in=classified_tags_ids)\
            .exclude(id=self.object.id).annotate (
                image_thumb = Subquery (
                    ClassifiedImages.objects.filter(
                        classified=OuterRef('pk'),
                    ).values(
                        'image_thumb'
                    )[:1]
                )
            )

        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(classified=self.object.id)
        
        context['images_no'] = len(context['images'])
        context['similar_classifieds'] = similar_classifieds.annotate(same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:6]

        return context
