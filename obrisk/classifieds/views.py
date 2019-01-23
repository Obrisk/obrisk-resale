from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView
from django.views.generic.edit import BaseFormView
from django.urls import reverse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.forms.utils import ErrorList
from django import forms

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.classifieds.forms import ClassifiedForm, ClassifiedReportForm #ImagesCreateFormSet

import json
import six
from cloudinary.forms import cl_init_js_callbacks
from cloudinary import CloudinaryResource


def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


class ClassifiedsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published classifieds list."""
    model = Classified
    paginate_by = 15
    context_object_name = "classifieds"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['popular_tags'] = Classified.objects.get_counted_tags()        
        return context

    def get_queryset(self, **kwargs):
        return Classified.objects.get_published()

    # def list(self, request):
    #     defaults = dict(format="jpg", height=150, width=150)
    #     defaults["class"] = "thumbnail inline"

    #     # The different transformations to present
    #     samples = [
    #         dict(crop="fill", radius=10),
    #         dict(crop="scale"),
    #         dict(crop="fit", format="png"),
    #         dict(crop="thumb", gravity="face"),
    #         dict(format="png", angle=20, height=None, width=None, transformation=[
    #             dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
    #         ]),
    #     ]
    #     samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    #     return render(request, 'classified/classified_list.html', dict(images=ClassifiedImages.objects.all(), samples=samples))


class DraftsListView(ClassifiedsListView):
    """Overriding the original implementation to call the drafts classifieds
    list."""
    def get_queryset(self, **kwargs):
        return Classified.objects.get_drafts()


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

        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # context['user'] = self.object
        #context = dict(images_formset = ImagesCreateFormSet())
        #cl_init_js_callbacks(context['images_formset'], self.request)
        return context
    
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

            images_list = form.cleaned_data['images'].split(',')
            print (images_list)

            #I no longer need the img_size in the form of Classified. I should update that.
            for img_url in images_list:
                img = ClassifiedImages(imageUrl=img_url)
                img.classified = classified
                img.save()
            return self.form_valid(form) 
        else:
            #ret = dict(errors=form.errors)
            return self.form_invalid(form)
            #return HttpResponse(json.dumps(ret), content_type='application/json')
                
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

class ReportClassifiedView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """This class has to inherit FormClass model but failed to implement that
    Update view will use the model Classified which is not a nice implementation.
    There is no need of a model here just render a form and the send email. """

    message = _("Your report has been submitted.")
    model = Classified
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailClassifiedView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(classified=self.object.id)
        return context


