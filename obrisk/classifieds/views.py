from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
        CreateView, UpdateView,
        DetailView, DeleteView)
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import (
        Paginator, EmptyPage,
        PageNotAnInteger)
from django.db.models import (
        OuterRef, Subquery, Case,
        When, Value, IntegerField, Count)
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie

from taggit.models import Tag
from obrisk.utils.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import (
        Classified, OfficialAd,
        ClassifiedImages, ClassifiedTags)
from obrisk.classifieds.forms import (
        ClassifiedForm, OfficialAdForm,
        ClassifiedEditForm)
from obrisk.utils.images_upload import multipleImagesPersist

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from dal import autocomplete

TAGS_TIMEOUT = getattr(settings, 'TAGS_CACHE_TIMEOUT', DEFAULT_TIMEOUT)

def set_popular_tags():
    popular_tags = Classified.objects.get_counted_tags()[:30]

    cache.set('popular_tags', list(popular_tags), timeout=TAGS_TIMEOUT)

    return HttpResponse(
            "Successfully sorted the popular tags!",
            content_type='text/plain')

#People can view without login
@ensure_csrf_cookie
@require_http_methods(["GET"])
def classified_list(request, tag_slug=None):

    if request.user.is_authenticated:
        city = request.user.city
    else:
        #Find the way to get their city using IP Address
        #request.user.IPAddress find in cities tables.
        #If not in China?
        city = "Hangzhou"

    #Try to Get the popular tags from cache
    popular_tags = cache.get('popular_tags')

    if popular_tags is None:
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
            data = {
                'status': '400',
                'error_message': f'Your form is having invalid input on: {form.errors} Correct your input and submit again'
            }
        else:
            data = {
                'status': '400',
                'error_message': 'We are having trouble to process your post, please try again later' 
            }
        return JsonResponse(data)
     
    def form_valid(self, form):
        images_json = form.cleaned_data['images']
        img_errors = form.cleaned_data['img_error']
        show_phone = form.cleaned_data['show_phone']
        
        failure_data = {
            'status': '400',
            'error_message': 'Sorry, the image(s) were not successful uploaded, please try again'
        }
        if not images_json:
            #The front-end will add the default images in case of errors 
            #Empty images_json means this form bypassed our front-end upload.
            return self.form_invalid(form, data=failure_data)
        
        if img_errors:
            #Send this email in a celery task to improve performance
            send_mail('JS ERRORS ON IMAGE UPLOADING', str(img_errors) , 'errors@obrisk.com', ['admin@obrisk.com',])

        #Phone number needs no backend verification, it is just a char field. 
        form.instance.user = self.request.user
        classified = form.save(commit=False)
        
        #Empty phone number is +8613300000000 for all old users around 150 users
        if self.request.user.phone_number is not '' and show_phone:
            if not classified.phone_number and self.request.user.phone_number.national_number != 13300000000:
                classified.phone_number = self.request.user.phone_number
            
        if not classified.address and self.request.user.address:
            classified.address = self.request.user.address
        
        classified.save()
        
        # split one long string of images into a list of string each for one JSON obj
        images_list = images_json.split(",")
        if multipleImagesPersist(self.request, images_list, 'classifieds', classified):    
            messages.success(self.request, self.message)
            data = {
                'status': '200',
                'success_message': 'Successfully created a new classified post'
            }
            return JsonResponse(data)
        else:
            form = ClassifiedForm()
            return self.form_invalid(form,data=failure_data)

    #def get_success_url(self):
        #This method is never called

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
        similar_classifieds = Classified.objects.get_active().filter(tags__in=classified_tags_ids)\
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
