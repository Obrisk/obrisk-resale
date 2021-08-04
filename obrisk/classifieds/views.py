import logging
import re
import requests
import json
import urllib
import os
import ast
import decimal

from django.contrib import messages
from django.contrib.auth.mixins import (
        LoginRequiredMixin
    )
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
from django.core.cache import cache
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

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkgeoip.request.v20200101.DescribeIpv4LocationRequest import (
        DescribeIpv4LocationRequest
    )
from obrisk.utils.helpers import (
        ajax_required, AuthorRequiredMixin,
        OfficialUserRequiredMixin
    )
from obrisk.classifieds.models import (
        Classified, OfficialAd, ClassifiedOrder,
        ClassifiedImages, ClassifiedTags)
from obrisk.classifieds.forms import (
        ClassifiedForm, AdminClassifiedForm, OfficialAdForm,
        ClassifiedEditForm)
from obrisk.utils.images_upload import multipleImagesPersist
from obrisk.classifieds.tasks import add_tags
from obrisk.classifieds.wxpayments import get_jsapi_params, get_sign
from config.settings.base import env
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


API_KEY = env('WECHAT_API_KEY')


@require_http_methods(["GET"])
def classified_list(request, city=None):

    if request.user.is_authenticated:
        city = city or request.user.city

    else:
        city = city or cache.get(
                f'user_city_{request.session.get("visitor_id")}'
            )
        if city is None:
            client_ip, _ = get_client_ip(
                    request
                )
            if client_ip is None:
                city = ''
                logging.error(
                        f'Cannot get user client_ip on classifieds list'
                    )
            else:
                try:
                    access_key_id = os.getenv('RAM_USER_ID')
                    access_key_secret = os.getenv('RAM_USER_S3KT_KEY')
                    #Default timeout is 5 secs, but the server is far from aliyun
                    #This is north China, there are 3 more data centers. try others
                    client = AcsClient(
                            access_key_id, access_key_secret,
                            'cn-hangzhou',timeout=30, max_retry_time=3)

                    req = DescribeIpv4LocationRequest()
                    req.set_accept_format('json')
                    req.set_Ip(client_ip)

                    response = client.do_action_with_exception(req)
                    info = ast.literal_eval(str(response, encoding='utf-8'))

                    city = info['CityEn']
                    if info['CountryEn'] != 'China' and len(info['CountryEn']) > 1:
                        messages.error(
                            request,
                            "This platform is for China users, if you're, pls switch off the vpn🙄"
                        )
                except Exception as e:
                    logging.error(f'Aliyun Geoip failed', exc_info=e)
                    city = ''

            cache.set(
                f'user_city_{request.session.get("visitor_id")}',
                city,
                60 * 60 * 2
            )

    classifieds_list = Classified.objects.get_active().values(
                    'title','price','city','slug', 'thumbnail'
                ).annotate(
                    order = Case (
                        When(city=city, then=Value(1)),
                        default=Value(2),
                        output_field=IntegerField(),
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
                            'title','price','city','slug', 'thumbnail'
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

    return render(request, 'classifieds/classified_list.html',
            {'page': page, 'city': city,'classifieds': classifieds,
            'base_active': 'classifieds'}
        )



@require_http_methods(["GET"])
def classified_list_by_tags(request, tag_slug=None):
    tag = None
    if tag_slug:
        try:
            tag = get_object_or_404(ClassifiedTags, slug=tag_slug)
            classifieds = Classified.objects.get_active().filter(
                    tags__in=[tag]).values(
                            'title','price','city','slug', 'thumbnail'
                        ).order_by('-timestamp')
        except:
            pass

    paginator = Paginator(classifieds, 6)  #6 @ page in mobile
    page = request.GET.get('page')

    try:
        classifieds = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer deliver the first page
        classifieds = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            classifieds = Classified.objects.get_expired().filter(
                    tags__in=[tag]).values(
                            'title','price','city','slug', 'thumbnail'
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

    return render(request, 'classifieds/classified_list.html',
            {'page': page,  'classifieds': classifieds,
            'tag': tag, 'base_active': 'classifieds'}
        )



class CreateOfficialAdView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = OfficialAd
    message = _("Your item is ready to be bought✌️")
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
        classified.details = str(classified.details).strip()
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
    message = _("Your item is ready to go✌️ ")
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
        if user.phone_number != '':
            if user.phone_number.national_number != 13300000000:
                classified.phone_number = user.phone_number

        if not classified.english_address and user.english_address:
            classified.english_address = user.english_address

        if not classified.chinese_address and user.chinese_address:
            classified.chinese_address = user.chinese_address

        classified.save()
        add_tags.delay(classified.id)

        images_list = images_json.split(",")
        if multipleImagesPersist(
                self.request, images_list,
                'classifieds', classified):
            messages.success(self.request, self.message)
            data = {
                'status': '200',
                'success_message': _(
                    'Your item is ready to go✌️ '
                )
            }
            return JsonResponse(data)
        else:
            form = ClassifiedForm()
            return self.form_invalid(form,data=failure_data)



@login_required
def adminCreateClassified(request, *args, **kwargs):

    if not request.user.is_superuser:
        return HttpResponse(
                "Hey, You are not authorized!",
                content_type='text/plain')
    if request.method == 'GET':

        #form = AdminClassifiedForm()
        return render(
                request,
                'classifieds/admin_classified_create.html',
                {'form':AdminClassifiedForm()}
            )

    elif request.method == 'POST':
        form = AdminClassifiedForm(request.POST)
        data=None

        if form.is_valid():
            images_json = form.cleaned_data['images']
            img_errors = form.cleaned_data['img_error']

            if img_errors:
                #Send this email in a celery task to improve performance
                logging.error(
                        'JS ERRORS ON IMAGE UPLOADING:' + \
                        str(img_errors)
                    )

            #Phone number needs no backend verification, it is just a char field. 
            #user = self.request.user
            user = form.instance.user
            classified = form.save(commit=False)

            #Empty phone number is +8613300000000 for all old users around 150 users
            if user.phone_number != '':
                if user.phone_number.national_number != 13300000000:
                    classified.phone_number = user.phone_number

            if not classified.english_address and user.english_address:
                classified.english_address = user.english_address

            if not classified.chinese_address and user.chinese_address:
                classified.chinese_address = user.chinese_address

            classified.save()
            for tag in form.cleaned_data['tags']:
                classified.tags.add(tag)
            classified.save()


            images_list = images_json.split(",")
            if multipleImagesPersist(
                    request, images_list,
                    'classifieds', classified):
                messages.success(
                    request,
                    'Your item is ready to go✌️'
                )
                data = {
                    'status': '200',
                    'success_message': _(
                        'Your item is ready to go✌️ '
                    )
                }
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

    else:
        return HttpResponse(
                "Hey, You are not authorized!",
                content_type='text/plain')


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
    message = _("Ta-da! Everything is updated, as you wish😉")
    form_class = ClassifiedEditForm
    template_name = 'classifieds/classified_update.html'

    # In this form there is an image that is not saved
    #deliberately since you can't upload images.
    def form_valid(self, form):
        form.instance.user = self.request.user

        classified = form.save(commit=False)
        #Can do custom updates here
        classified.save()
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
            .exclude(id=self.object.id)

        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(
                classified=self.object.id
            )
        context['similar_classifieds'] = similar_classifieds.annotate(
                same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:8]

        return context


@require_http_methods(["GET"])
def create_classified_order(request, *args, **kwargs):
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
            slug=request.GET.get('sg', None)
        ).first()

    if classified:
        return render(
            request,
            'classifieds/create_classified_order.html',
            {'classified': classified}
        )

    else:
        messages.success(
            request,
            "Sorry the payment service can't be accessed now"
        )
        return redirect('classifieds:list')


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
            slug=request.GET.get('sg', None)
        ).first()

    if classified and isinstance(classified.price, decimal.Decimal):
        openid = request.user.wechat_openid
        if openid:
            return render(
                request,
                'classifieds/pay_order.html',
                {
                 'classified': classified,
                 'data': get_jsapi_params(
                     request,
                     openid,
                     re.sub('[\W_]+', ' ', classified.title),
                     re.sub('[\W_]+', ' ', classified.details),
                     classified.price
                  )
                }
            )
        else:
            messages.error(
                    request,
                    "You need to login with wechat to be able to pay"
                )
            return redirect('classifieds:classified', classified.slug)

    else:
        messages.error(
                request,
                "Sorry payment service is unavailable now"
            )
        return redirect('classifieds:list')


@login_required
@require_http_methods(["POST"])
def wxpyjs_success(request, *args, **kwargs):
    classified = Classified.objects.filter(
            slug=request.POST.get('sg', None)
        ).first()

    if classified:
        classified.status='E'
        classified.save()

        is_offline = False
        if request.POST.get('addr', None) is None:
            is_offline = True

        order = ClassifiedOrder.objects.create(
           buyer=request.user,
           classified=classified,
           is_offline=is_offline,
           recipient_chinese_address=request.POST.get('addr', None),
           recipient_phone_number=request.POST.get('phone', None)
        )
        return JsonResponse({
            'success': True,
            'order_slug': order.slug
        })
    else:
        return JsonResponse({
            'success': False
        })


class Wxpay_Result(View):
    """
    微信支付结果回调通知路由
    """
    def get(self, request, *args, **kwargs):
            return JsonResponse({
                'success': False,
                'message': 'Request is invalid'
            })

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
            logging.error(
                f'Payment succeeded with signature {sign}'
            )
            return HttpResponse(xmltodict.unparse(
                        {'return_code': 'SUCCESS', 'return_msg': 'OK'},
                        pretty=True
                    )
                )
        return HttpResponse(xmltodict.unparse(
                {'return_code': 'FAIL', 'return_msg': 'SIGNERROR'},
                pretty=True
            )
        )


class ClassifiedOrderView(DetailView):
    model = ClassifiedOrder

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(
                ClassifiedOrderView, self
            ).get_context_data(**kwargs)

        classified_tags_ids = self.object.classified.tags.values_list('id', flat=True)
        similar_classifieds = Classified.objects.get_active().filter(
                tags__in=classified_tags_ids)\
            .exclude(id=self.object.classified.id)

        # Add in a QuerySet of all the images
        context['images'] = ClassifiedImages.objects.filter(
                classified=self.object.classified.id
            )

        context['images_no'] = len(context['images'])
        context['similar_classifieds'] = similar_classifieds.annotate(
                same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:6]

        return context
