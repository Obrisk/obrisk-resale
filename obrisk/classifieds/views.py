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
from django.http import HttpResponseRedirect

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified
from obrisk.classifieds.forms import ClassifiedForm, ClassifiedReportForm


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

class ReportClassifiedView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    """Basic EditView implementation to edit existing classifieds."""
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
        self.object = None
        return super().form_valid(form)

    def post(self , request , *args , **kwargs):
        return super().post(self, request, *args, **kwargs)"""


class DetailClassifiedView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual classified."""
    model = Classified
