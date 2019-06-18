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
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate

from .forms import UserForm, PhoneSignupForm
from .models import User
from .phone_verification import send_sms


class SignUp(CreateView):
    form_class = PhoneSignupForm
    success_url = reverse_lazy('classifieds:list')
    template_name = 'account/phone_signup.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def User(self, request, *args, **kwargs):
        """
        Handles User requests, instantiating a form instance and its inline
        formsets with the passed User variables and then checking them for
        validity.
        """
        form = PhoneSignupForm(self.request.User)

        if form.is_valid():
            return self.form_valid(form)
        else:
            # ret = dict(errors=form.errors) #Handle custom errors here.
            print(form.errors)
            return self.form_invalid(form)


    def form_valid(self, form):

        user = form.save(commit=False)
        print(self.request.POST.get("verified_phone"))

        user.phone_number = self.request.POST.get("verified_phone")
        user.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')  
        login_user = authenticate(username=username, password=raw_password)
        login(self.request, login_user)

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
    print("we hit here....")
    if request.method == "POST":
        phone_no = request.POST.get("phone_number")
        print(phone_no)
        if len(phone_no) == 11 and phone_no[0] == '1':
            try:
                check_phone = User.objects.get(phone_number=phone_no)
            except:
                check_phone = None

            if check_phone is not None:
                return JsonResponse({'success': False, 'error': "This number exists"} )
            __business_id = uuid.uuid1()
            
            random = get_random_string(length=6, allowed_chars='0123456789')
            params = " {\"code\":\""+ random + "\"} " 
            
            # id: fixed, mobile phone number receiving the verification code, signature name, template name, verification code
            #ret = send_sms( __business_id , str(phone_no), os.getenv('SMS_SIGNATURE') , os.getenv('SMS_TEMPLATE'), params)
            print(random)
            cache.set(str(phone_no), random , 60)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': "This number is wrong!"} )
    else:
        return JsonResponse({'success': False})

@require_http_methods(["GET", "POST"])
def phone_verify(request):
    print("We are verifying....")
    if request.method == "POST":
        code = request.POST.get("code")
        print(request.POST)
        
        phone_no = request.POST.get("cached_phone")
        print(phone_no)
        print(cache.get(str(phone_no)))
        #print(verify_queue[str(phone_no)])

        try:
            if cache.get(str(phone_no)) == code:
                return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False, 'error':"The verification code is invalid or has expired"})
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False, 'error':"Invalid request"})
    
        



