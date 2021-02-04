import logging
import re
import requests
import json
import urllib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
        CreateView, UpdateView,
        DetailView, DeleteView)
from django.urls import reverse, reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.http import (
        JsonResponse, HttpResponse,
        HttpResponseRedirect, HttpResponseBadRequest
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

import xmltodict
from dal import autocomplete
from ipware import get_client_ip
from obrisk.utils.helpers import ajax_required, AuthorRequiredMixin
from obrisk.classifieds.models import (
        Classified, OfficialAd, ClassifiedOrder,
        ClassifiedImages, ClassifiedTags)
from obrisk.classifieds.forms import (
        ClassifiedForm, OfficialAdForm,
        ClassifiedEditForm)
from obrisk.utils.images_upload import multipleImagesPersist
from obrisk.classifieds.wxpayments import get_jsapi_params
from config.settings.base import env
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


API_KEY = env('WECHAT_API_V3_KEY')
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
        city = "Hangzhou"
        '''city = cache.get(
                f'user_city_{request.COOKIES.get("visitor_id")}'
            )
        if city is None:
            client_ip, _ = get_client_ip(
                    request,
                    proxy_count=2,
                    proxy_trusted_ips=['63.0.0.5','63.1']
                )

            if client_ip is None:
                city = "Hangzhou"
            else:
                info = requests.get(f'https://geolocation-db.com/json/{client_ip}')
                city = json.loads(info.text)['city']

            city = cache.set(
                    f'user_city_{request.COOKIES.get("visitor_id")}',
                    city,
                    60 * 60 * 2
                )'''

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

    if request.is_ajax():
        return JsonResponse({
                'classifieds': list(classifieds)
            })

    #Try to Get the popular tags from cache
    popular_tags = cache.get('popular_tags_mb')

    if popular_tags is None:
        popular_tags = Classified.objects.get_active(
                ).get_counted_tags()[:10]
        cache.set('popular_tags_mb',
                    list(popular_tags), timeout=TAGS_TIMEOUT
                )

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

        if not classified.english_address and user.english_address:
            classified.english_address = user.english_address

        if not classified.chinese_address and user.chinese_address:
            classified.chinese_address = user.chinese_address

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


@login_required
@require_http_methods(["GET"])
def initiate_wxpy_info(request, *args, **kwargs):
    """
    用户点击一个路由或者扫码进入这个views.py中的函数，首先获取用户的openid,
    使用jsapi方式支付需要此参数
    :param self:
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    classified = Classified.objects.filter(
            sg=request.GET.get('sg', None)
        ).first()

    if classified:
        openid = request.user.wechat_openid
        details = classified.title
        total_fee = classified.price

        if openid:
            return render(
                request,
                'classifieds/create_classified_order.html',
                {
                 'classified': classified,
                 'data': get_jsapi_params(openid, details, total_fee)
                }
            )
            #3 hours cache in case Wechat delays to notify us of a
            #successful payment
            cache.set(f'wxpy_order_{openid}', classified.id, 10800)
        else:
            messages.success(
                    request,
                    "You need to login with wechat to be able to pay"
                )
            return redirect('classifieds:classified', classified.slug)

    else:
        return HttpResponseBadRequest(
                content=_('The request is invalid'))


class Wxpay_Result(View):
    """
    微信支付结果回调通知路由
    """
    def post(self, request, *args, **kwargs):
        """
        微信支付成功后会自动回调
        返回参数为：
        {'mch_id': '',
        'time_end': '',
        'nonce_str': '',
        'out_trade_no': '',
        'trade_type': '',
        'openid': '',
         'return_code': '',
         'sign': '',
         'bank_type': '',
         'appid': '',
         'transaction_id': '',
          'cash_fee': '',
          'total_fee': '',
          'fee_type': '', '
          is_subscribe': '',
          'result_code': 'SUCCESS'}

        :param request:
        :param args:
        :param kwargs:
        :return:
        Check the status of the corresponding business data
        to determine whether the notification has been processed.
        If it has not been processed, then proceed with the processing.
        If it has been processed, the result will be returned directly.
        Processing payment success logic
        """

        # 回调数据转字典 # print('支付回调结果', data_dict)
        data_dict = xmltodict.parse(request.body)
        sign = data_dict.pop('sign')  # 取出签名
        back_sign = get_sign(data_dict, API_KEY)  # 计算签名

        #Return the received result to WeChat otherwise
        #WeChat will send a post request every 8 minutes
        if sign == back_sign and data_dict['return_code'] == 'SUCCESS':
            classified = cache.get(f"wxpy_order_{data_dict['openid']}")
            if classified:
                ClassifiedOrder.objects.create(
                   buyer=user_model.objects.filter(openid=data_dict['openid']).first(),
                   classified=Classified.objects.filter(id=classified).first(),
                   buyer_transaction_id = data_dict['transaction_id']
                )
                return HttpResponse(xmltodict.unparse(
                            {'return_code': 'SUCCESS', 'return_msg': 'OK'},
                            pretty=True
                        )
                    )
            else:
                logging.error(
                    f'Payment succeeded but classified is not cached {data_dict}'
                )
        return HttpResponse(xmltodict.unparse(
                {'return_code': 'FAIL', 'return_msg': 'SIGNERROR'},
                pretty=True
            )
        )


class ClassifiedOrderView(DetailView):
    model = ClassifiedOrder
