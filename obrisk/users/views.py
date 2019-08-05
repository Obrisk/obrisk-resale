import uuid, os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView, ListView, RedirectView, UpdateView, FormView
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator    
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

import os
import base64
import datetime
import oss2
import ast
import boto3
import json

from allauth.account.views import LoginView, PasswordResetView 
from obrisk.helpers import bucket, bucket_name
from .forms import UserForm, EmailSignupForm,  PhoneResetPasswordForm
from .models import User
from .phone_verification import send_sms, verify_counter

    
#There is no need to override this view. By default All-auth auto login users without password
@method_decorator(csrf_exempt, name='dispatch')
class EmailSignUp(CreateView):
    form_class = EmailSignupForm
    success_url = reverse_lazy('classifieds:list')
    template_name = 'account/phone_signup.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles User requests, instantiating a form instance and
        User variables and then checking them for validity."""

        form = EmailSignupForm(self.request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            # ret = dict(errors=form.errors) #Handle custom errors here.
            return self.form_invalid(form)


    def form_valid(self, form):
        form.save()
        
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')  
        try:
            user = authenticate(self.request, username=username, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect ('classifieds:list')
                else:
                    return super(SignUp, self).form_valid(form)     
            else:
                #if the user is not successfully authenticated return the normal form_valid response.
                return super(SignUp, self).form_valid(form)     
                    
        except:
            return super(SignUp, self).form_valid(form)     




def send_code(full_number):
    random = get_random_string(length=6, allowed_chars='0123456789')

    #if settings.DEBUG=True (default=False)
    if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
        print("Your phone number verification is....")
        print(random)
        cache.set(str(full_number), random , 600)
        return JsonResponse({
            'success': True,
            'message': "The code has been sent, please wait for it. It is valid for 10 minutes!"
        })

    else:
            # Create an SNS client
        client = boto3.client(
            "sns",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        # Send your sms message.
        ret = client.publish(
            PhoneNumber=str(full_number),
            Message=f"[Obrisk] Welcome, your code is {random}. Thank you for signing up!",
            MessageAttributes={
                'string': {
                    'DataType': 'String',
                    'StringValue': 'String',
                },
                'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': os.getenv('AWS_SENDER_ID')
                    }
                }
            )

        #For alibaba.
        #params = " {\"code\":\""+ random + "\"} " 
        # __business_id = uuid.uuid1()                                        
        # ret = send_sms( __business_id , str(phone_no), os.getenv('SMS_SIGNATURE') , os.getenv('SMS_TEMPLATE'), params)
        #ret = ret.decode("utf-8")
        #ret = ast.literal_eval(ret)
        #if ret['Code'] == 'OK'
        
        response = ret['ResponseMetadata'] 

        if response['HTTPStatusCode'] == 200:
            cache.set(str(full_number), random , 600)
            return JsonResponse({
                'success': True,
                'message': "The code has been sent, please wait for it. It is valid for 10 minutes!"
            })
            
        else:
            return JsonResponse({
                'success': False,
                'error_message': "Sorry we couldn't send the verification code please signup with your email at the bottom of this page!", 
                'messageId':ret["MessageId"], 'returnedCode':response["HTTPStatusCode"], 'requestId':response["RequestId"], 
                'retries': response["RetryAttempts"]
            })  
            #'SMSAPIresponse':ret["Message"], 'returnedCode':ret["Code"], 'requestId':ret["RequestId"] 


def get_users(full_number):
    """Given an phone number, return matching user(s) who should receive a reset.
    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    return get_user_model().objects.get(phone_number=full_number,is_active=True)
     

@require_http_methods(["GET", "POST"])
def phone_password_reset(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_no")

        if phone_number is not None and len(phone_number) == 11 and phone_number[0] == '1':
            
            full_number = "+86" + phone_number
            check_phone = User.objects.filter(phone_number=full_number).exists()

            if check_phone is True:
                return send_code(full_number)

            else:
                return JsonResponse({'success': False, 'error_message': "This phone number doesn't exist!"})
        
        else:
            return JsonResponse({'success': False, 'error_message': "The phone number is not correct please re-enter!"} )
    
    else:
        form = PhoneResetPasswordForm()
        return render(request, 'account/phone_password_reset.html', {'form': form})
        

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)
        

    def form_valid(self, form):
        picture = form.cleaned_data['oss_image']
        form.instance.user = self.request.user
        profile = form.save(commit=False)
        profile.user = self.request.user

        if not picture:
            profile.save()
            return super(UserUpdateView, self).form_valid(form)

        else:
            if picture.startswith('media/profile_pics/') == False:
                profile.save()                
                messages.error(self.request, "Oops! your profile picture, \
                wasn't uploaded successfully, please upload again!")
                return super(UserUpdateView, self).form_valid(form)   
            
            else:
                d = str(datetime.datetime.now())
                thumb_name = "media/profile_pics/" + str(profile.user) + "/thumbnails/" + "thumb-" + d 
                style = 'image/resize,m_fill,h_60,w_60'

                try:
                    process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                                oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                    oss2.compat.to_bytes(thumb_name))),
                                                                oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
                    bucket.process_object(picture, process)
                except:
                    #Since the image exists just save the profile, it is our problem. 
                    profile.save()
                    messages.error(self.request, "Oops we are sorry! Your image \
                            was not uploaded successfully. please upload again!.")
                    #return self.form_invalid(form)
                    #I am not returning form errors because this is our problem and not user's
                    return redirect ('users:detail', username=self.request.user.username)

                #Only save the new image when you have the thumbnail.
                profile.thumbnail = thumb_name
                profile.picture = picture
                profile.save()
                       
                return super(UserUpdateView, self).form_valid(form)



    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)



    

class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


@require_http_methods(["GET", "POST"])
def send_code_sms(request):
    if request.method == "GET":
        phone_no = request.GET.get("phone_no")
        
        if phone_no is not None and len(phone_no) == 11 and phone_no[0] == '1':
            
            full_number = "+86" + phone_no
            check_phone = User.objects.filter(phone_number=full_number).exists()

            if check_phone is False:
                return send_code(full_number)

            else:
                return JsonResponse({'success': False, 'error_message': "This phone number already exists!"} )

        else:
            return JsonResponse({'success': False, 'error_message': "The phone number is not correct please re-enter!"})
    else:
        return JsonResponse({'success': False, 'error_message':"This request is invalid!"} )

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
                return JsonResponse({'error_message': "The verification code has expired!" } )
            else:
                if saved_code == code:
                    if str(request.META.get('HTTP_REFERER')).endswith("/users/phone-password-reset/") == True:
                        try:
                            user = get_users(full_number)
                        except:
                            return JsonResponse({'success': False, 'error_message': "The user registered with this phone number is not found!"})
                        else:
                            if user:
                                token = default_token_generator.make_token(user)
                                url = f"https://www.obrisk.com/accounts-authorization/password/reset/key/{token}" 

                                return JsonResponse({'success': True, 'url':url })
                            else:
                                return JsonResponse({'success': False, 'error_message': "The user registered with this phone number is not found!"})
                    else:
                        return JsonResponse({'success': True})
                
                else:
                    return JsonResponse({'success': False, 'error_message': "The verification code is not correct!" })                    
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False, 'error_message': "The phone number or the code is empty!"} )
    else:
        return JsonResponse({'success': False, 'error_message': "This request is invalid!"} )
    
        



