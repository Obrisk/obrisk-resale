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

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.classifieds.forms import ClassifiedForm, ClassifiedReportForm 

import json
import re
from cloudinary import CloudinaryResource


class ClassifiedsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published classifieds list."""
    model = Classified
    paginate_by = 15
    context_object_name = "classifieds"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['popular_tags'] = Classified.objects.get_counted_tags()
        context['image'] = str(ClassifiedImages.objects.all())
       
        return context

    def get_queryset(self, **kwargs):
        qs = Classified.objects.get_active()
        return qs

class DraftsListView(ClassifiedsListView):
    """Overriding the original implementation to call the drafts classifieds
    list."""
    def get_queryset(self, **kwargs):
        return Classified.objects.get_expireds()


class CreateClassifiedView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = Classified
    message = _("Your classified has been created.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_create.html'

    def __init__(self, **kwargs):
        # i think self.object could be as self.request.user
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
            classified = form.save(commit=False)
            classified.user = self.request.user
            classified.save()

            # split one long string of JSON objects into a list of string each for one JSON obj 
            cloudinary_list = re.findall ( r'\{.*?\}', form.cleaned_data['images'])

            for image_obj in cloudinary_list:
                #convert the obj from string into JSON.
                json_response = json.loads(image_obj)

                #Populate a CloudinaryResource object using the upload response
                result = CloudinaryResource(public_id=json_response['public_id'], type=json_response['type'], resource_type=json_response['resource_type'], version=json_response['version'], format=json_response['format'])

                str_result = result.get_prep_value()  # returns a CloudinaryField string e.g. "image/upload/v123456789/test.png" 

                img = ClassifiedImages(images= str_result)
                img.classified = classified
                img.save()
            return self.form_valid(form) 
        else:
            #ret = dict(errors=form.errors)
            print(form.errors)
            return self.form_invalid(form)
                  
    def form_valid(self, form):
        form.instance.user = self.request.user
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
    form_class = ClassifiedReportForm
    template_name = 'classifieds/classified_report.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


    """ If it was a FormView then,
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(self, request, *args, **kwargs)

    def get_object ()

    def form_valid(self, form):
        self.request.user = None
        return super().form_valid(form)

    def post(self , request , *args , **kwargs):
        return super().post(self, request, *args, **kwargs)"""


class DetailClassifiedView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual classified."""
    model = Classified

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(DetailClassifiedView, self).get_context_data(**kwargs)
    #     # Add in a QuerySet of all the images
    #     context['images'] = ClassifiedImages.objects.filter(classified=self.object.id)
    #     return context


