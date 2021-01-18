import logging
import re
import requests
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
        CreateView, UpdateView,
        DetailView, DeleteView)
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.http import (
        JsonResponse, HttpResponse, HttpResponseRedirect
    )
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.paginator import (
        Paginator, EmptyPage,
        PageNotAnInteger)
from django.db.models import (
        OuterRef, Subquery, Case,
        When, Value, IntegerField, Count)
from django.views.decorators.csrf import ensure_csrf_cookie

from dal import autocomplete
from ipware import get_client_ip
from obrisk.utils.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import (
        Classified, OfficialAd,
        ClassifiedImages, ClassifiedTags)
from obrisk.classifieds.forms import (
        ClassifiedForm, OfficialAdForm,
        ClassifiedEditForm)
from obrisk.utils.images_upload import multipleImagesPersist


TAGS_TIMEOUT = getattr(settings, 'TAGS_CACHE_TIMEOUT', DEFAULT_TIMEOUT)


def set_popular_tags():
    popular_tags = Classified.objects.get_active(
            ).get_counted_tags()[:10]

    cache.set('popular_tags_mb',
                list(popular_tags), timeout=TAGS_TIMEOUT
            )

    return HttpResponse(
            "Successfully sorted the popular tags!",
            content_type='text/plain')


@require_http_methods(["GET"])
def classified_list(request, tag_slug=None):

    if request.user.is_authenticated:
        city = request.user.city
    else:
        city = cache.get(
                f'user_city_{request.COOKIES.get("visitor_id")}'
            )
        if city is None:
            client_ip, _ = get_client_ip(
                    request,
                    proxy_count=2,
                    proxy_trusted_ips=['63.0.0.5','63.1']
                )
            logging.error(f'Client ip is {client_ip}')
            if client_ip is None:
                city = ""
            else:
                info = requests.get(f'https://geolocation-db.com/json/{client_ip}')
                city = json.loads(info.text)['city']
                city = cache.set(
                        f'user_city_{request.COOKIES.get("visitor_id")}',
                        city,
                        60 * 60 * 3
                    )


    #Try to Get the popular tags from cache
    popular_tags = cache.get('popular_tags_mb')

    if popular_tags is None:
        popular_tags = Classified.objects.get_active(
                ).get_counted_tags()[:10]
        cache.set('popular_tags_mb',
                    list(popular_tags), timeout=TAGS_TIMEOUT
                )

    #Get classifieds
    classifieds_list = Classified.objects.get_active().values(
                    'title','price','city','slug'
                ).annotate(
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

    paginator = Paginator(classifieds_list, 6)  #6 @ page in mobile
    page = request.GET.get('page')

    try:
        classifieds = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        classifieds = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            classifieds = Classified.objects.get_expired().values(
                            'title','price','city','slug'
                        ).annotate (
                            image_thumb = Subquery (
                                ClassifiedImages.objects.filter(
                                    classified=OuterRef('pk'),
                                ).values(
                                    'image_thumb'
                                )[:1]
                            )
                        ).order_by('-timestamp')

            return JsonResponse({
                'classifieds': list(classifieds), 'end':'end'
                })
        else:
            classifieds = paginator.page(paginator.num_pages)

    # Deal with tags in the end to override other_classifieds.
    tag = None
    if tag_slug:

        tag = get_object_or_404(ClassifiedTags, slug=tag_slug)
        classifieds = Classified.objects.get_active().filter(
                tags__in=[tag]).annotate (
            image_thumb = Subquery (
                ClassifiedImages.objects.filter(
                    classified=OuterRef('pk'),
                ).values(
                    'image_thumb'
                )[:1]
            )
        ).order_by('-timestamp')

    if request.is_ajax():
        return JsonResponse({
                'classifieds': list(classifieds)
            })

    return render(request, 'classifieds/classified_list.html',
            {'page': page, 'popular_tags': popular_tags,
            'city': city,'classifieds': classifieds,
            'tag': tag, 'base_active': 'classifieds'})


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
        Handles Classified requests, instantiate a form instance
        and its inline formsets with the passed Classified
        variables and then checking them for
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


@method_decorator(login_required, name='post')
class CreateClassifiedView(CreateView):
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
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        #For now, invalid form doesn't refresh the whole page so images is retained. 
        #To-do: images of the users must be stored and when form has errors
        #They must be updated on the front-end to avoid users to re-upload.
        #self.classified_images = form['images']
        #self.redo_upload = False
        #In the front-end if redo_upload = False, don't trigger upload when submit btn 
        #is clicked. Just submit the form.
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form, data=None):
        '''Render the invalid form messages as json responses
        instead of html form. '''
        if data:
            if data['status'] == '400':
                return JsonResponse(data)
        if form.errors:
            error_msg = re.sub('<[^<]+?>', ' ', str(form.errors))
            data = {
                'status': '400',
                'error_message': _(
                    f'Form error on {error_msg}')
            }
        else:
            data = {
                'status': '400',
                'error_message': _(
                    'Sorry we can\'t process your post \
                        please try again later')
            }
        return JsonResponse(data)

    def form_valid(self, form):
        images_json = form.cleaned_data['images']
        img_errors = form.cleaned_data['img_error']
        show_phone = form.cleaned_data['show_phone']
        user = self.request.user

        failure_data = {
            'status': '400',
            'error_message': _(
                'Sorry, the image(s) were not successfully uploaded, \
                    please try again')
        }

        if not images_json:
            #The front-end will add the default images in case of errors 
            #Empty images_json means this form bypassed our front-end upload.
            return self.form_invalid(form, data=failure_data)

        if img_errors:
            #Send this email in a celery task to improve performance
            logging.error(
                    'JS ERRORS ON IMAGE UPLOADING:' + \
                    str(img_errors)
                )

        #Phone number needs no backend verification, it is just a char field. 
        form.instance.user = user
        classified = form.save(commit=False)

        #Empty phone number is +8613300000000 for all old users around 150 users
        if user.phone_number is not '' and show_phone:
            if (not classified.phone_number and
                    user.phone_number.national_number != 13300000000):
                classified.phone_number = user.phone_number

        if not classified.address and user.address:
            classified.address = user.address

        classified.save()

        images_list = images_json.split(",")
        if multipleImagesPersist(
                self.request, images_list,
                'classifieds', classified):
            messages.success(self.request, self.message)
            data = {
                'status': '200',
                'success_message': _(
                    'Successfully created a new classified post'
                )
            }
            return JsonResponse(data)
        else:
            form = ClassifiedForm()
            return self.form_invalid(form,data=failure_data)

    #def get_success_url(self):
        #This method is never called


class ClassifiedTagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ClassifiedTags.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class EditClassifiedView(
        LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing classifieds."""
    model = Classified
    message = _("Your classified has been updated.")
    form_class = ClassifiedEditForm
    template_name = 'classifieds/classified_update.html'

    # In this form there is an image that is not saved
    #deliberately since you can't upload images.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class ReportClassifiedView(LoginRequiredMixin, View):
    """This class has is not working as expected
    No need of a model just render a form, send email. """

    message = _("Your report has been submitted.")
    template_name = 'classifieds/classified_report.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class ClassifiedDeleteView(
        LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView
    overriding the delete method to
    allow a no-redirect response to use with AJAX call."""
    model = Classified
    message = _(
            "Your classified post has been deleted successfully!")
    success_url = reverse_lazy("classifieds:list")


    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object
        and then redirect to the
        success URL. This method is called by post.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status="E"
        self.object.save()
        return HttpResponseRedirect(success_url)


class DetailClassifiedView(DetailView):
    """Basic DetailView implementation
    to call an individual classified."""
    model = Classified

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(
                DetailClassifiedView, self
            ).get_context_data(**kwargs)

        classified_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_classifieds = Classified.objects.get_active().filter(
                tags__in=classified_tags_ids)\
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
        context['images'] = ClassifiedImages.objects.filter(
                classified=self.object.id
            )

        context['images_no'] = len(context['images'])
        context['similar_classifieds'] = similar_classifieds.annotate(
                same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:6]

        return context
