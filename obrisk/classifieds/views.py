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


# def gallery(request):
#     list = ClassifiedImages.objects.filter(is_visible=True).order_by('-created')
#     paginator = Paginator(list, 10)

#     page = request.GET.get('page')
#     try:
#         albums = paginator.page(page)
#     except PageNotAnInteger:
#         albums = paginator.page(1) # If page is not an integer, deliver first page.
#     except EmptyPage:
#         albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

#     return render(request, 'gallery.html', { 'albums': list })


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
            classified = form.save(commit=False)
            classified.user = self.request.user
            classified.save()
                
            img = ClassifiedImages(image = str_result)
            img.classified = classified
            img.save()
            return self.form_valid(form) 
        else:
            #ret = dict(errors=form.errors)
            # print(form.errors)
            return self.form_invalid(form)
                  
    def form_valid(self, form):
        new_post = form.cleaned_data['classified']
        for each in form.cleaned_data['image']:
            ClassifiedImages.objects.create(file=each, post = new_post)
        # form.instance.user = self.request.user
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


