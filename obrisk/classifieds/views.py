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

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.classifieds.forms import ClassifiedForm, ClassifiedReportForm #ImageDirectForm #ImagesCreateFormSet

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

        # context = dict(formset = ImageDirectForm())
        # #This callback is needed in  cloudinary/forms.py
        # cl_init_js_callbacks(context['formset'], self.request)
        context['form'] = ClassifiedForm()
        return context
                  
    def form_valid(self, form):

        classified = form.save()

        images_list = json.loads(self.request.body)

        for _ in images_list:
            get_public_id = self.request.POST.get('public_id')
            get_type = self.request.POST.get('type')
            get_resource_type = self.request.POST.get('resource_type')
            get_version = self.request.POST.get('version')
            get_format = self.request.POST.get('format')

            json_response = {"public_id":get_public_id, "type":get_type, "resource_type":get_resource_type, "version":get_version, "format": get_format}

            # Populate a CloudinaryResource object using the upload response
            result = CloudinaryResource(public_id=json_response['public_id'], type=json_response['type'], resource_type=json_response['resource_type'], version=json_response['version'], format=json_response['format'])

            str_result = result.get_prep_value()  # returns a CloudinaryField string e.g. "image/upload/v123456789/test.png" 

            img = ClassifiedImages(image= str_result)
            img.classified = classified
            img.save()

            #Response is useful for debugging only.
            cloudinaryResponse = dict(image_id=form.instance.id) 
            print (json.dumps(cloudinaryResponse))
              
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


