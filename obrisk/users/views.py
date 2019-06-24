import uuid, os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView, ListView, RedirectView, UpdateView
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.conf import settings
import ast

from .forms import UserForm, PhoneSignupForm
from .models import User
from .phone_verification import send_sms, verify_counter


class SignUp(CreateView):
    form_class = PhoneSignupForm
    success_url = reverse_lazy('classifieds:list')
    template_name = 'account/phone_signup.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles User requests, instantiating a form instance and
        User variables and then checking them for validity."""

        form = PhoneSignupForm(self.request.POST)

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
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect ('classifieds:list')
            else:
                return super(SignUp, self).form_valid(form)     
                    
        except:
            return super(SignUp, self).form_valid(form)     

                    


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
            
            check_no = "+86" + phone_no
            check_phone = User.objects.filter(phone_number=check_no).exists()

            if check_phone is False:
                random = get_random_string(length=6, allowed_chars='0123456789')

                #if settings.DEBUG=True (default=False)
                if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
                    print("Your phone number verification is....")
                    print(random)
                    cache.set(str(phone_no), random , 600)
                    return JsonResponse({
                        'success': True,
                        'message': "The code has been sent, please wait for it. It is valid for 10 minutes!"
                    })

                else:
                    __business_id = uuid.uuid1()
                    params = " {\"code\":\""+ random + "\"} " 
                    
                    # try:
                    #     verify_counter = cache.get(str(phone_no))
                    #     if verify_counter is not None:
                    #         verify_counter += 1
                    # except:
                    #     verify_counter = 1
                    #Only send the sms when the verify_counter is less than 3;
                    
                    # id, phone number, signature name, template name, template variables
                    
                    ret = send_sms( __business_id , str(phone_no), os.getenv('SMS_SIGNATURE') , os.getenv('SMS_TEMPLATE'), params)

                    ret = ret.decode("utf-8")
                    ret = ast.literal_eval(ret)
                    
                    if ret["Code"] == "OK":
                        cache.set(str(phone_no), random , 600)
                        return JsonResponse({
                            'success': True,
                            'message': "The code has been sent, please wait for it. It is valid for 10 minutes!"
                        })
                        
                    else:
                        return JsonResponse({
                            'success': False,
                            'error_message': "Sorry we couldn't send the verification code please contact us at support@obrisk.com!", 
                            'SMSAPIresponse':ret["Message"], 'returnedCode':ret["Code"], 'requestId':ret["RequestId"]
                        })                        
            else:
                return JsonResponse({'success': False, 'error_message': "This phone number already exists!"} )

        else:
            return JsonResponse({'success': False, 'error_message': "The phone number is not correct please re-enter!"} )
    else:
        return JsonResponse({'success': False, 'error_message':"This request is invalid!"} )

@require_http_methods(["GET", "POST"])
def phone_verify(request):
    if request.method == "GET":
        code = request.GET.get("code")
        phone_no = request.GET.get("phone_no")
        
        if phone_no is not None and code is not None:
            try:
                if cache.get(str(phone_no)) == code:
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error_message': "The verification code is not correct!" })                    
            except:
                return JsonResponse({'message': "The verification code has expired!" } )
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False, 'error_message': "The phone number or the code is empty!"} )
    else:
        return JsonResponse({'success': False, 'error_message': "This request is invalid!"} )
    
        



