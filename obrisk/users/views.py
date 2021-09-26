import os
import re
import uuid
import ast
import base64
import datetime
import oss2
import boto3
import logging
import itertools
import time
from urllib.parse import urlsplit

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
        DetailView, ListView,
        RedirectView, UpdateView, FormView)
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.text import slugify as dj_slugify
from django.core.paginator import (
        Paginator, EmptyPage,
        PageNotAnInteger)

from django.http import (
    HttpResponseServerError,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    JsonResponse
)
from django.db.models import IntegerField, Case, When, Value

from allauth.account.views import (
    SignupView, LoginView,
    _ajax_response,
    PasswordResetFromKeyView as AllauthPasswordResetFromKeyView
)

from slugify import slugify
from allauth.account.forms import UserTokenForm
from allauth.account.utils import user_pk_to_url_str, url_str_to_user_pk
from allauth.utils import build_absolute_uri
from phonenumbers import PhoneNumber
from friendship.models import Friend, Follow
from rest_framework.decorators import api_view

from obrisk.users.serializers import UserSerializer
from obrisk.utils.helpers import ajax_required
from obrisk.utils.images_upload import bucket, bucket_name
from obrisk.users.wechat_authentication import WechatLogin
from obrisk.users.wechat_config import CHINA_PROVINCES
from obrisk.users.tasks import update_prof_pic_async
from .forms import (
        UserForm, EmailSignupForm, CusSocialSignupForm,
        PhoneRequestPasswordForm, PhoneResetPasswordForm,
        SocialSignupCompleteForm, VerifyAddressForm,
        AdminCreateUserForm)
from .models import User
from .phone_verification import send_sms
from obrisk.classifieds.models import Classified

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


SMS_SEND_RETRY = 0

class SocialPostView(FormView):
    form_class = CusSocialSignupForm
    template_name = 'socialaccount/signup.html'


#There is no need to override this view. 
#By default All-auth directly login users when they signup.
class EmailSignUp(SignupView):
    form_class = EmailSignupForm
    template_name = 'account/email_signup.html'


def aliyun_send_code(random, phone_number):

    params = " {\"code\":\""+ random + "\"} "
    __business_id = uuid.uuid1()
    ret = send_sms(
            __business_id, phone_number,
            os.getenv('SMS_SIGNATURE'),
            os.getenv('SMS_TEMPLATE'), params)
    ret = ret.decode("utf-8")

    #'SMSAPIresponse':ret["Message"],
    #'returnedCode':ret["Code"], 'requestId':ret["RequestId"]
    return ast.literal_eval(ret)


def aws_send_code(theme, random, phone_number):

    if len(phone_number) == 11:
        phone_number = '+86' + phone_number

    client = boto3.client(
        "sns",
        aws_access_key_id=os.getenv('AWS_SMS_ACCESS_KY'),
        aws_secret_access_key=os.getenv('AWS_SMS_S3KT_KY'),
        region_name=os.getenv('AWS_SMS_REGION')
    )

    if theme == "signup":
        msg = f"[Obrisk] Welcome, the code is {random}. Thank you for signing up!"

    elif theme == "password-reset" and user:
        msg = f"[Obrisk] Verification code:{random} and Username:{user}"
    else:
        msg = f"[Obrisk] The verification code is {random}, valid for 10 minutes!"

    # Send your sms message.
    ret = client.publish(
        PhoneNumber=str(phone_number),
        Message=msg,
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'String',
            },
            'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': os.getenv('AWS_SMS_SENDER_ID')
                }
            }
        )

    return ret['ResponseMetadata']


def send_code(phone_number, theme, user=None):
    random = get_random_string(length=6, allowed_chars='0123456789')
    cache.set(str(phone_number), random , 600)

    success_resp = JsonResponse({
        'success': True,
        'message': "Ding ding🔔 Pls wait for the code😊"
    })
    fail_resp = JsonResponse({
        'success': False,
        'error_message': "Sorry we couldn't send the code, try again later!"
    })

    if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
        print("Your phone number verification is....")
        print(random)
        return success_resp

    try:
        #try with Aliyun first
        ret = aliyun_send_code(random, phone_number)

        if ret['Code'] == 'OK':
            return success_resp

        time.sleep(3)
        SMS_SEND_RETRY += 1

        if SMS_SEND_RETRY > 4:
            logging.error(
                    f'Ali SMS failed 4 times. Code:{ret["Code"]}, ret: {ret}'
                )
            #retry with AWS
            response = aws_send_code(theme, random, phone_number)
            if response['HTTPStatusCode'] == 200:
                return success_resp

            logging.error(
                    f'AWS & Ali SMS failed. ALI:{ret}, AWS:{response}'
                )
            return fail_resp
        return send_code(phone_number, theme, user)

    except Exception as e:
        #retry with AWS
        try:
            response = aws_send_code(theme, random, phone_number)
            if response['HTTPStatusCode'] == 200:
                return success_resp

            #retry with Aliyun again
            ret = aliyun_send_code(random, phone_number)
            if ret['Code'] == 'OK':
                return success_resp

        except Exception as e:
            pass
        logging.error(
                f'AWS & Ali SMS failed. ALI:{ret}, AWS:{response}, e:{e}'
            )
        return fail_resp


def get_users(phone_number):
    """Given a phone number, return matching user(s) who should receive a reset.
    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    if len(phone_number) == 11:
        phone_number = '+86' + phone_number

    try:
        return get_user_model().objects.get(
                phone_number=phone_number,is_active=True
            )
    except get_user_model().DoesNotExist:
        return None


@require_http_methods(["GET", "POST"])
def phone_password_reset(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_no")

        if phone_number is not None and len(
                phone_number) == 11 and phone_number[0] == '1':

            user = get_users(phone_number)
            if user:
                return send_code(phone_number, "password-reset", user=user)

            else:
                return JsonResponse({'success': False,
                    'error_message': "This phone number doesn't exist!"})

        else:
            return JsonResponse({'success': False,
                'error_message': "The phone number is not correct please re-enter!"} )

    else:
        form = PhoneRequestPasswordForm()
        return render(request, 'account/phone_password_reset.html', {'form': form})


@method_decorator(ensure_csrf_cookie, name="get")
class UserDetailView(DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user
            sent_requests = Friend.objects.sent_requests(user)
            in_coming_reqst = Friend.objects.requests(user)

            context['pending'] = [u.to_user for u in sent_requests]
            context['pended'] = [u.from_user for u in in_coming_reqst]
            context['friends'] = Friend.objects.friends(user)

        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        updated_form_data = form.data.copy()
        if form['province_region'].value() == '':
            updated_form_data.update({
                'province_region': self.request.user.province_region,
                'city': self.request.user.city
            })
            form.data = updated_form_data
        else:
            if form['city'].value() == '':
                messages.error(
                        self.request,
                        'Province and city must be updated together'
                    )
                return self.form_invalid(form)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)



@require_http_methods(["GET"])
def user_classifieds_list(request, rq_user=None):

    user = User.objects.filter(username=rq_user)
    if user is None:
        classifieds_list = Classified.objects.get_active().values(
                        'title','price','city','slug', 'thumbnail'
                    ).order_by('-priority', '-timestamp')
    else:
        classifieds_list = Classified.objects.filter(
                user=user.first()).values(
                        'title','price','city','slug', 'thumbnail', 'status'
                    ).annotate(
                    order = Case (
                        When(status='A', then=Value(1)),
                        default=Value(2),
                        output_field=IntegerField(),
                    )
                ).order_by('order', '-priority', '-timestamp')

    if classifieds_list.exists():
        share_img = classifieds_list.first()['thumbnail']
    else:
        share_img = 'https://dist.obrisk.com/static/ver0106210002/img/favicon.ico'

    paginator = Paginator(classifieds_list, 6)  #6 @ page in mobile
    page = None

    try:
        page = request.GET.get('page')
        classifieds = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        classifieds = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return JsonResponse({
                 'end':'end'
                })
        else:
            classifieds = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return JsonResponse({
                'classifieds': list(classifieds)
            })

    return render(request, 'users/user_classifieds.html',
            {'page': page,
             'classifieds': classifieds,
             'user': user.first(),
             'share_img': share_img
            }
        )


@ajax_required
@login_required
@require_http_methods(["POST"])
def update_profile_pic(request):
    picture = request.POST.get("profile_pic")

    if not picture:
        return JsonResponse({
            'success': False,
            'error_message': "No profile picture submitted!"})

    else:
        if picture.startswith('media/images/profile_pics/') is False:
            return JsonResponse({'success': False,
                                'error_message': "Your picture, \
                                        wasn't uploaded successfully, \
                                        Please upload again!"})

        else:
            d = str(datetime.datetime.now())
            thumb_name = "media/images/profile_pics/" + slugify(
                    str(request.user)) + "/thumbnails/" + "thumb-" + d + ".jpeg"
            pic_name = "media/images/profile_pics/" + slugify(
                    str(request.user))+ "/thumbnails" + "dp-" + d + ".jpeg"
            style1 = 'image/resize,m_fill,h_60,w_60'
            style2 = 'image/resize,m_fill,h_250,w_250'

            try:
                process1 = "{0}|sys/saveas,o_{1},b_{2}".format(style1,
                                            oss2.compat.to_string(
                                                base64.urlsafe_b64encode(
                                                oss2.compat.to_bytes(thumb_name))),
                                            oss2.compat.to_string(
                                                base64.urlsafe_b64encode(
                                                    oss2.compat.to_bytes(bucket_name))))
                process2 = "{0}|sys/saveas,o_{1},b_{2}".format(style2,
                                            oss2.compat.to_string(base64.urlsafe_b64encode(
                                                oss2.compat.to_bytes(pic_name))),
                                            oss2.compat.to_string(
                                                base64.urlsafe_b64encode(
                                                    oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(picture, process1)
                bucket.process_object(picture, process2)
            except:
                #Since the image exists just save the profile, it is our problem.
                return JsonResponse({'success': False,
                                'error_message': "Sorry, your photo was not \
                                        uploaded successfully. Try again later!"})

            #Only save the new image when you have the thumbnail.
            profile = get_user_model().objects.get(username=request.user)
            profile.thumbnail = thumb_name
            profile.picture = pic_name
            profile.org_picture = picture
            profile.save()

            return JsonResponse({'success': True})


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(
                    "Hey, You are not authorized!",
                    content_type='text/plain')
        return super().dispatch(self, request, *args, **kwargs)


@ajax_required
@require_http_methods(["GET", "POST"])
def send_code_sms(request):
    if request.method == "GET":
        phone_no = request.GET.get("phone_no")

        if (phone_no is not None and len(phone_no) == 11
            and phone_no[0] == '1' and phone_no != '13300000000'):

            users = User.objects.filter(
                    phone_number= '+86' + phone_no
                )

            if users:
                if users.first().wechat_openid != None:
                    return JsonResponse(
                            {'success': False,
                                'error_message': "Number exists, try to login/reset password"
                            })
            return send_code(phone_no, "signup")


        else:
            return JsonResponse({
                'success': False,
                'error_message': "The phone number is not correct please re-enter!"})
    else:
        return JsonResponse({
            'success': False,
            'error_message':"This request is invalid!"
        })


@ajax_required
@require_http_methods(["GET", "POST"])
def phone_verify(request):
    if request.method == "GET":
        code = request.GET.get("code")
        phone_no = request.GET.get("phone_no")

        if phone_no is not None and code is not None:
            try:
                saved_code = cache.get(str(phone_no))
            except:
                return JsonResponse({
                    'error_message': "The verification code is invalid!"})
            else:
                if saved_code == code:
                    if str(request.META.get(
                            'HTTP_REFERER'
                            )).endswith("/users/phone-password-reset/"):
                        try:
                            user = get_users(phone_no)
                        except:
                            return JsonResponse({'success': False,
                                                'error_message': "Sorry \
                                                        there is a problem with this account. \
                                                        Please contact us!",
                                                'phone_no': phone_no })
                        else:
                            if user:
                                token = default_token_generator.make_token(user)
                                # current_site = get_current_site(request)
                                # save it to the password reset model
                                # password_reset = PasswordReset(user=user, temp_key=temp_key)
                                # password_reset.save()

                                # send the password reset email
                                path = reverse("users:phone_ps_reset_confirm",
                                            kwargs=dict(uidb36=user_pk_to_url_str(user),
                                                        key=token))
                                url = build_absolute_uri(request, path)
                                return JsonResponse({'success': True, 'url':url })
                            else:
                                return JsonResponse({'success': False,
                                                     'error_message': "Sorry \
                                                             there is a problem with this account. \
                                                             Please contact us!"})
                    else:
                        return JsonResponse({'success': True})

                else:
                    return JsonResponse({'success': False,
                        'error_message': "The verification code is not correct!"})
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False,
                'error_message': "The phone number or the code is empty!"})
    else:
        return JsonResponse({'success': False,
            'error_message': "This request is invalid!"})


class PasswordResetFromKeyView(AllauthPasswordResetFromKeyView):

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.key = key
        token_form = UserTokenForm(
            data={'uidb36': uidb36, 'key': self.key})

        if token_form.is_valid():
            # Store the key in the session and redirect to the
            # password reset form at a URL without the key. That
            # avoids the possibility of leaking the key in the
            # HTTP Referer header.
            # (Ab)using forms here to be able to handle errors in XHR #890
            token_form = UserTokenForm(
                data={'uidb36': uidb36, 'key': self.key})
            if token_form.is_valid():
                self.reset_user = token_form.reset_user
                # The super must be called with FormView or the link will be invalid. Ignore the linter
                return super(FormView, self).dispatch(request, uidb36, self.key, **kwargs)

        else:
            if str(request.META.get('HTTP_REFERER')).endswith("/users/phone-password-reset/"):
                self.reset_user = token_form.reset_user
                return super(FormView, self).dispatch(request, uidb36, self.key, **kwargs)

            self.reset_user = None
            response = self.render_to_response(
                self.get_context_data(token_fail=True)
            )

            return _ajax_response(self.request, response, form=token_form)


class PhonePasswordResetConfirmView(FormView):
    template_name = "account/phone_ps_reset_confirm.html"
    form_class = PhoneResetPasswordForm
    success_url = reverse_lazy("classifieds:list")

    def post(self, request, uidb36=None, key=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb36 is not None and key is not None  # checked by URLconf
        try:
            uid = url_str_to_user_pk(uidb36)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, key):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been updated!')
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return self.form_valid(form)

            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)



#ajax_required
@require_http_methods(["GET"])
def username_exists(request):
    """A function view to check if the username exists"""
    prefered_name = request.GET.get('username')
    if not User.objects.filter(username__iexact=prefered_name.lower()):
        return JsonResponse({
            "status": "200",
            "message": "This username is available"})
    else:
        return JsonResponse({
            "status": "201",
            "message": "This username is taken"
        })


class WechatViewSet(View):
    wechat_api = WechatLogin()


class AuthView(WechatViewSet):
    def get(self, request):
        nxt = request.GET.get("next", None)

        if request.COOKIES.get("active-chat") is not None:
            cache.set(
                f'chat_cookie_{request.session.get("visitor_id")}',
                request.COOKIES.get("active-chat"),
                1500
            )

        if nxt is not None and nxt != 'None':
            cache.set(
                f'nxt_{request.session.get("visitor_id")}',
                nxt,
                1500
            )
        if request.COOKIES.get("classified") is not None:
            cache.set(
                f'classified_{request.session.get("visitor_id")}',
                request.COOKIES.get("classified"),
                1500
            )
        url = self.wechat_api.get_code_url()
        return redirect(url)


def redirect_after_login(request, social_login=None):
    nxt = cache.get(
        f'nxt_{request.session.get("visitor_id")}'
    )
    classified = cache.get(
        f'classified_{request.session.get("visitor_id")}'
    )
    chat_cookie = cache.get(
       f'chat_cookie_{request.session.get("visitor_id")}'
    )


    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not is_safe_url(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        url = urlsplit(nxt)
        response = HttpResponseRedirect(
                url.path
            )
        if chat_cookie is not None:
            response.set_cookie('active-chat', chat_cookie, 30)

        if classified is not None:
            response.set_cookie('classified', classified , 30)
        return response


def ajax_redirect_after_login(request, social_login=None):
    nxt = cache.get(
        f'nxt_{request.session.get("visitor_id")}',
    )
    classified = cache.get(
        f'classified_{request.session.get("visitor_id")}',
    )
    chat_cookie = cache.get(
       f'chat_cookie_{request.session.get("visitor_id")}'
    )

    if nxt is None:
        return JsonResponse({
            'success': True,
             'nxt' : reverse(settings.LOGIN_REDIRECT_URL)
         })
    elif not is_safe_url(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return JsonResponse({
            'success': True,
             'nxt' : reverse(settings.LOGIN_REDIRECT_URL)
         })
    else:
        url = urlsplit(nxt)
        response = JsonResponse({
            'success': True,
             'nxt' : url.path
        })
        if chat_cookie is not None:
            response.set_cookie('active-chat', chat_cookie, 30)
        return response


class GetInfoView(WechatViewSet):
    http_method_names = ['get', 'post']

    def get(self, request):
        if 'code' in request.GET:
            try:
                code = request.GET['code']
                token, openid = self.wechat_api.get_access_token(code)
            except TypeError:
                return redirect('account_signup')

            else:
                if token is None or openid is None:
                    logging.error('Wechat auth failed')
                    return HttpResponseServerError('Get access or openid not provided')

                user_info, error = self.wechat_api.get_user_info(token, openid)

                if error:
                    logging.error(f'Wechat auth failed: {error}')
                    return HttpResponseServerError('get access_token error')

                user_data = {
                    'nck': user_info['nickname'],
                    'sx': user_info['sex'],
                    'pr': user_info['province'].encode('iso8859-1').decode('utf-8'),
                    'ct': user_info['city'].encode('iso8859-1').decode('utf-8'),
                    'cnt': user_info['country'].encode('iso8859-1').decode('utf-8'),
                    'ui': user_info['openid']
                }
                user = User.objects.filter(
                        wechat_openid=user_data['ui']
                    )

                if user.count() == 0:
                    cache.set(user_data['ui'], user_info['headimgurl'], 3000)

                    tentative_name = first_name = dj_slugify(
                            user_data['nck'],
                            allow_unicode=True
                        )

                    for x in itertools.count(1):
                        if not User.objects.filter(
                                username=tentative_name).exists():
                            break
                        tentative_name = '%s-%d' % (first_name, x)

                    in_china=False
                    if str(user_data['cnt']) == 'China':
                        in_china=True

                    form = SocialSignupCompleteForm(
                                initial={
                                    'username': tentative_name,
                                    'gender': user_data['sx'],
                                    'wechat_openid': user_data['ui'],
                                }
                            )
                    return render(request,
                            'users/wechat-auth.html',
                            {'form': form, 'in_china': in_china}
                        )
                else:
                    login(
                        request, user.first(),
                        backend='django.contrib.auth.backends.ModelBackend'
                    )

                    if cache.get(request.COOKIES.get("wx-rand")) is None:
                        cache.set(
                            request.COOKIES.get('wx-rand'),
                            user.first().wechat_openid,
                            getattr(settings, 'SESSION_COOKIE_AGE', 60 * 60 * 24 * 40)
                        )
                return redirect_after_login(request, social_login=True)
        else:
            return HttpResponseBadRequest(
                 content=_('Bad request')
             )


def wechat_getinfo_view_test(request):

    if request.method == 'GET':

        user_data = {
            'ui': 'thisisaveryuniqueopenid48',
            'sx': 1,
            'nck':'admin 乔舒亚',
            'cnt':  'China'
        }

        user = User.objects.filter(
                wechat_openid=user_data['ui']
            )
        if user.count() == 0:
            cache.set(
                user_data['ui'],
                'https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img/homepage-bg.jpg', #noqa
                3000)

            user_data['nck'] = first_name = dj_slugify(
                    user_data['nck'],
                    allow_unicode=True
                )

            for x in itertools.count(1):
                if not User.objects.filter(
                        username=user_data['nck']).exists():
                    break
                user_data['nck'] = '%s-%d' % (first_name, x)

            in_china=False
            if str(user_data['cnt']) == 'China':
                in_china=True

            form = SocialSignupCompleteForm(
                        initial={
                            'username': user_data['nck'],
                            'gender': user_data['sx'],
                            'wechat_openid': user_data['ui'],
                        }
                    )
            return render(request,
                    'users/wechat-auth.html',
                    {'form': form, 'in_china': in_china}
                )

        else:
            login(
                request, user.first(),
                backend='django.contrib.auth.backends.ModelBackend'
            )
            return redirect_after_login(request, social_login=True)
        return HttpResponseBadRequest(
             content=_('Bad request')
         )

    else:
        return HttpResponseBadRequest(
             content=_('Bad request')
         )


@ajax_required
@require_http_methods(["POST"])
def complete_wechat_reg(request, **kwargs):

    updated_request = request.POST.copy()
    req_phone_num = request.POST.get('phone_number')

    if req_phone_num:
        try:
            saved_code = cache.get(
                    str(req_phone_num).replace('+86', '')
                )
        except:
            return JsonResponse({
                'success': False,
                'error_message': "The verification code has expired or is invalid!"
            })
        else:
            request_code = str(request.POST.get('verify_code')).strip()

            if str(saved_code) == request_code:
                if not updated_request['phone_number'].startswith('+86'):
                    updated_request.update(
                            {'phone_number': '+86' + updated_request['phone_number']})

            else:
                return JsonResponse({
                    'success': False,
                    'error_message': "The verification code is incorrect"
                })

    else:
        return JsonResponse({
            'success': False,
            'error_message': "Sorry we failed to register you. Try again later!"
        })

    form = SocialSignupCompleteForm(updated_request)

    if form.is_valid():
        try:
            picture = cache.get(request.POST.get('wechat_openid'))
        except:
            return JsonResponse({
                'success': False,
                'error_message': "Sorry we failed to register you. Try again later!"
            })

        exist_users = User.objects.filter(
                phone_number = updated_request['phone_number']
            )

        if not exist_users:
            user = form.save(request, commit=False)
        else:
            if exist_users.first().wechat_openid is None:
                user = exist_users.first()
                user.wechat_openid = updated_request['wechat_openid']
            else:
                return JsonResponse({
                    'success': False,
                    'error_message': "Sorry we failed to register you. Try again later!"
                })

        thumbnail = picture[:-3] + '64'
        full_image = picture[:-3] + '0'

        user.save()
        update_prof_pic_async(
            user.id, thumbnail, picture, full_image
        )

        login(
            request, user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return ajax_redirect_after_login(request, social_login=True)

    else:
        error_msg = re.sub('<[^<]+?>', ' ', str(form.errors))
        return JsonResponse({
            'success': False,
            'error_message': _(
                f'Input error on {error_msg}')
            })


@ajax_required
@api_view(['GET'])
def complete_authentication(request):
    """
    This view is to upadate social users' phone number and password
    as they are required to be authorized completely
    """

    usr = request.user
    user = User.objects.get(username=usr)

    # getting socialusers without phone_number
    if user.socialaccount_set.all() and not user.phone_number:
        user_inputs = request.query_params
        serializer = UserSerializer(user, data=user_inputs)

        if serializer.is_valid():
            serializer.save()
            return redirect("classifieds:list")

        else:
            return JsonResponse({"status": "403",
                "message": "Please enter valid inputs"})

    else:
        return redirect_after_login(request)



class VerifyAddressView(LoginRequiredMixin, UpdateView):
    form_class = VerifyAddressForm
    template_name = 'users/verify_address.html'
    model = User

    def get_success_url(self):
        messages.success(request, 'Delivery address confirmed!')
        return reverse('classified:list')

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)



@login_required
def admin_create_user(request, *args, **kwargs):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponse(
                "Hey, You are not authorized!",
                content_type='text/plain')

    if request.method == 'GET':
        return render(
                request,
                'users/admin_create_user.html',
                {'form':AdminCreateUserForm(
                    initial={
                        'username': request.GET.get('nm'),
                        'city': request.GET.get('ct'),
                        'province_region': request.GET.get('pr'),
                        'country': request.GET.get('cn'),
                        'id': request.GET.get('pk')
                    }
                )}
            )

    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)

        if form.is_valid():
            #obj = User.objects.get(pk=form.cleaned_data['pk'])
            user = form.save(request, commit=True)
            #user.save()

    return redirect(
        ''.join(
            ['/', settings.ADMIN_URL.strip('^'),
            'users/wechatuser/']
        )
    )

@ajax_required
@require_http_methods(["GET"])
def wechat_auto_login(request, **kwargs):

    if request.COOKIES.get("wx-rand") is not None:
        openid = request.COOKIES.get("wx-rand")
    else:
        return JsonResponse({"success": False})

    user = User.objects.filter(
            wechat_openid=openid
        )
    if user.count() == 0:
        return JsonResponse({"success": False})

    login(
        request, user.first(),
        backend='django.contrib.auth.backends.ModelBackend'
    )

    nxt = request.META.get('HTTP_REFERER')
    cache.set(f'nxt_{request.session.get("visitor_id")}', nxt, 60)

    return ajax_redirect_after_login(request)


@login_required
@require_http_methods(["GET"])
def bulk_update_user_phone_no(request):
    """ A temporally view to create Conversations to users already chatted
    before Convervation model was created."""
    users = User.objects.all()
    for user in users:
        if isinstance(user.phone_number, PhoneNumber):
            if not user.phone_number.country_code:
                user.phone_number = '+8613300000000'
                user.save()

    return redirect('classifieds:list')
