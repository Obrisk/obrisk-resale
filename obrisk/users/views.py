import  os
import uuid
import ast
import base64
import datetime
import oss2
import boto3
import logging
import itertools

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
        DetailView, ListView,
        RedirectView, UpdateView, FormView)
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import (
    HttpResponseServerError,
    HttpResponseRedirect,
    HttpResponseBadRequest
)
from allauth.account.views import (
    SignupView, LoginView,
    _ajax_response,
    PasswordResetFromKeyView as AllauthPasswordResetFromKeyView
)
from allauth.account.forms import UserTokenForm
from allauth.account.utils import user_pk_to_url_str, url_str_to_user_pk
from allauth.utils import build_absolute_uri
from slugify import slugify
from phonenumbers import PhoneNumber
from friendship.models import Friend, Follow
from rest_framework.decorators import api_view

from obrisk.users.serializers import UserSerializer
from obrisk.utils.helpers import ajax_required
from obrisk.utils.images_upload import bucket, bucket_name
from obrisk.users.wechat_authentication import WechatLogin
from obrisk.users.tasks import update_profile_picture
from .forms import (
        UserForm, EmailSignupForm, CusSocialSignupForm,
        PhoneRequestPasswordForm, PhoneResetPasswordForm)
from .models import User
from .phone_verification import send_sms

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class SocialPostView(FormView):
    form_class = CusSocialSignupForm
    template_name = 'socialaccount/signup.html'


#There is no need to override this view. 
#By default All-auth directly login users when they signup.
class EmailSignUp(SignupView):
    form_class = EmailSignupForm
    template_name = 'account/email_signup.html'


def aliyun_send_code(random, full_number):
    phone_no = str(full_number).strip('+86')
    params = " {\"code\":\""+ random + "\"} "
    __business_id = uuid.uuid1()
    ret = send_sms(
            __business_id, phone_no,
            os.getenv('SMS_SIGNATURE'),
            os.getenv('SMS_TEMPLATE'), params)
    ret = ret.decode("utf-8")

    #'SMSAPIresponse':ret["Message"],
    #'returnedCode':ret["Code"], 'requestId':ret["RequestId"]
    return ast.literal_eval(ret)


def aws_send_code(theme, random, full_number):

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
        msg = f"[Obrisk] the verification code is {random}, valid for 10 minutes!"

    # Send your sms message.
    ret = client.publish(
        PhoneNumber=str(full_number),
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


def send_code(full_number, theme, user=None):
    random = get_random_string(length=6, allowed_chars='0123456789')

    #if settings.DEBUG=True (default=False)
    if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
        print("Your phone number verification is....")
        print(random)
        cache.set(str(full_number), random , 600)
        return JsonResponse({
            'success': True,
            'message': "We've sent the code, it is valid for 10 minutes!"
        })

    else:
        try:
            #try with Aliyun first
            ret = aliyun_send_code(random, full_number)

            if ret['Code'] == 'OK':
                cache.set(str(full_number), random , 600)

                return JsonResponse({
                    'success': True,
                    'message': "We've sent the code It is valid for 10 minutes!"
                })
            else:
                #retry with AWS
                response = aws_send_code(theme, random, full_number)
                if response['HTTPStatusCode'] == 200:
                    cache.set(str(full_number), random , 600)

                    return JsonResponse({
                        'success': True,
                        'message': "Code sent, valid for 10 minutes"
                    })

                else:
                    logging.error(
                            f'AWS & Ali SMS failed. ALI:{ret}, AWS:{response}'
                        )
                    return JsonResponse({
                        'success': False,
                        'error_message': "Sorry we couldn't send the code, try again later!"
                    })

        except Exception as e:
            #retry with AWS
            response = aws_send_code(theme, random, full_number)
            if response['HTTPStatusCode'] == 200:
                cache.set(str(full_number), random , 600)

                return JsonResponse({
                    'success': True,
                    'message': "Code sent, valid for 10 minutes!"
                })

            else:
                #retry with Aliyun again
                ret = aliyun_send_code(random, full_number)
                if ret['Code'] == 'OK':
                    cache.set(str(full_number), random , 600)

                    return JsonResponse({
                        'success': True,
                        'message': "Code sent, valid for 10 minutes!"
                    })

                else:
                    logging.error(
                            f'AWS & Ali SMS failed. ALI:{ret}, AWS:{response}, e:{e}'
                        )
                    return JsonResponse({
                        'success': False,
                        'error_message': "Sorry we couldn't send the code, try again later!"
                    })


def get_users(full_number):
    """Given an phone number, return matching user(s) who should receive a reset.
    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    try:
        return get_user_model().objects.get(phone_number=full_number,is_active=True)
    except get_user_model().DoesNotExist:
        return None


@require_http_methods(["GET", "POST"])
def phone_password_reset(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_no")

        if phone_number is not None and len(
                phone_number) == 11 and phone_number[0] == '1':

            full_number = "+86" + phone_number
            user = get_users(full_number)
            if user:
                return send_code(full_number, "password-reset", user=user)

            else:
                return JsonResponse({'success': False,
                    'error_message': "This phone number doesn't exist!"})

        else:
            return JsonResponse({'success': False,
                'error_message': "The phone number is not correct please re-enter!"} )

    else:
        form = PhoneRequestPasswordForm()
        return render(request, 'account/phone_password_reset.html', {'form': form})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # pk = kwargs.get('pk')pk=self.object.pk
        context = super(UserDetailView, self).get_context_data(**kwargs)
        """
        this prints the other user
        user = get_object_or_404(user_model, pk=self.object.pk)
        """
        user = self.request.user
        friends = Friend.objects.friends(user)
        following = Follow.objects.following(user)
        followers = Follow.objects.followers(user)
        # pending = FriendshipRequest.objects.filter(from_user=user)
        sent_requests = Friend.objects.sent_requests(user)
        in_coming_reqst = Friend.objects.requests(user)
        pending = [u.to_user for u in sent_requests]
        pended = [u.from_user for u in in_coming_reqst]

        context['friends'] = friends
        context['followers'] = followers
        context['following'] = following
        context['pending'] = pending
        context['pended'] = pended

        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


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
        if picture.startswith('media/profile_pics/') is False:
            return JsonResponse({'success': False,
                                'error_message': "Your picture, \
                                        wasn't uploaded successfully, \
                                        Please upload again!"})

        else:
            d = str(datetime.datetime.now())
            thumb_name = "media/profile_pics/" + slugify(
                    str(request.user)) + "/thumbnails/" + "thumb-" + d
            pic_name = "media/profile_pics/" + slugify(
                    str(request.user))+ "/thumbnails" + "dp-" + d
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
                                'error_message': "Sorry! Your image was not \
                                        uploaded successfully. Try again later!."})

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


@ajax_required
@require_http_methods(["GET", "POST"])
def send_code_sms(request):
    if request.method == "GET":
        phone_no = request.GET.get("phone_no")

        if (phone_no is not None and len(phone_no) == 11
            and phone_no[0] == '1' and phone_no != '13300000000'):

            full_number = "+86" + phone_no
            check_phone = User.objects.filter(
                    phone_number=full_number
                ).exists()

            if check_phone is False:
                return send_code(full_number, "signup")

            else:
                return JsonResponse(
                        {'success': False,
                            'error_message': "This phone number already exists!"
                        })

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
        full_number = "+86" + phone_no

        if phone_no is not None and code is not None:
            try:
                saved_code = cache.get(str(full_number))
            except:
                return JsonResponse({
                    'error_message': "The verification code has expired or it is invalid!"})
            else:
                if saved_code == code:
                    if str(request.META.get(
                            'HTTP_REFERER'
                            )).endswith("/users/phone-password-reset/"):
                        try:
                            user = get_users(full_number)
                        except:
                            return JsonResponse({'success': False,
                                                'error_message': "Sorry \
                                                        there is a problem with this account. \
                                                        Please contact us!",
                                                'phone_no': full_number })
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


class AutoLoginView(LoginView):
    pass


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

    return redirect('stories:list')


@ajax_required
@require_http_methods(["GET"])
def username_exists(request):
    """A function view to check if the username exists"""
    prefered_name = request.GET.get('username')
    if User.objects.filter(username__contains=prefered_name.lower()):
        return JsonResponse({
            "status": "201",
            "username":prefered_name,
            "message": "This username is taken"
        })
    else:
        return JsonResponse({
            "status": "200",
            "username":prefered_name,
            "message": "This username is available"})


class WechatViewSet(View):
    wechat_api = WechatLogin()


class AuthView(WechatViewSet):
    def get(self, request):
        url = self.wechat_api.get_code_url()
        return redirect(url)


class GetInfoView(WechatViewSet):
    def get(self, request):
        if 'code' in request.GET:
            code = request.GET['code']
            token, openid = self.wechat_api.get_access_token(code)
            if token is None or openid is None:
                logging.error('Wechat auth failed')
                return HttpResponseServerError('get access or openid not provided')
            user_info, error = self.wechat_api.get_user_info(token, openid)

            if error:
                logging.error(f'Wechat auth failed: {error}')
                return HttpResponseServerError('get access_token error')

            user_data = {
                'nickname': user_info['nickname'],
                'sex': user_info['sex'],
                'province': user_info['province'].encode('iso8859-1').decode('utf-8'),
                'city': user_info['city'].encode('iso8859-1').decode('utf-8'),
                'country': user_info['country'].encode('iso8859-1').decode('utf-8'),
                'avatar': user_info['headimgurl'],
                'openid': user_info['openid']
            }
            user = User.objects.filter(
                    wechat_openid=user_data['openid']
                )
            if user.count() == 0:

                username_cnd = first_name = slugify(
                        user_data['nickname'],
                        max_length=16
                    )

                for x in itertools.count(1):
                    if not User.objects.filter(username=username_cnd).exists():
                        break
                    username_cnd = '%s-%d' % (first_name, x)

                if user_data['province'] in (
                        'Shanghai', 'Beijing', 'Chongqing', 'Tianjin'):
                    user_data['city'] = user_data['province']

                try:
                    user = User.objects.create(
                            username=username_cnd,
                            city=user_data['city'],
                            province_region=user_data['province'],
                            country=user_data['country'],
                            gender=str(user_data['sex']),
                            picture=user_data['avatar'],
                            thumbnail=user_data['avatar'][:-3] + '64',
                            org_picture=user_data['avatar'][:-3] + '0',
                            wechat_openid=user_data['openid']

                        )

                    update_profile_picture.delay(user.id, 'wechat')
                except IntegrityError:
                    return HttpResponseServerError(
                            'Sorry we could not register you. Please try again later!'
                        )

                #Redirect to a page to complete phone number & City
                login(
                    request, user,
                    backend='django.contrib.auth.backends.ModelBackend')
            else:
                login(
                    request, user.first(),
                    backend='django.contrib.auth.backends.ModelBackend'
                )
            return HttpResponseRedirect(reverse('stories:list'))

        else:
            return HttpResponseBadRequest(
                 content=_('No code or state provided')
             )


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
            return redirect("stories:list")

        else:
            return JsonResponse({"status": "403", "message": "Please enter valid inputs"})

    else:

        return redirect("stories:list")
