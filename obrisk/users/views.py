import uuid, os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from utils import mcache

from .forms import UserForm
from .models import User
from .phone_verification import send_sms


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


def send_sms_captcha(request):
    phone_no = request.GET.get("phone_number")

    __business_id = uuid.uuid1()
    
    random = get_random_string(length=6, allowed_chars='0123456789')
    params = " {\"code\":\""+ random + "\"} " 
    
    # id: fixed, mobile phone number receiving the verification code, signature name, template name, verification code
    ret = send_sms( __business_id , str(phone_no), os.getenv('SMS_SIGNATURE') , os.getenv('SMS_TEMPLATE'), params)
    print(ret)
    mcache.set_key(phone_no, random)
    return JsonResponse({'success': True})


