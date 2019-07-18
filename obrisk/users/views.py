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
# from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator    
import ast
from friendship.models import Friend, Follow, FriendshipRequest, Block
from django.shortcuts import render, get_object_or_404, redirect

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')

from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# user_model = get_user_model


try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User



from .forms import UserForm, PhoneSignupForm
from .models import User
from .phone_verification import send_sms, verify_counter

@method_decorator(csrf_exempt, name='dispatch')
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
            
            full_number = "+86" + phone_no
            check_phone = User.objects.filter(phone_number=full_number).exists()

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
                        Message=f"[Obrisk] Welcome, your verification code is {random}. Thank you for signing up!",
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
                        cache.set(str(phone_no), random , 600)
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
    
        

#FRIENDSHIP
def view_friends(request, username, template_name="users/friends.html"):
    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)
    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name(),
        'friends': friends,
    })


@login_required
def friendship_add_friend(
    request, to_username, template_name="users/add_friends.html"
):
    """ Create a FriendshipRequest """
    ctx = {"to_username": to_username}

    if request.method == "POST":
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyFriendsError :
            return view_friends(request, from_user)
        except AlreadyExistsError : 
            return view_friends(request, from_user)
        else:
            return redirect("users:friendship_request_list")

    return render(request, template_name, ctx)


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_received, id=friendship_request_id
        )
        f_request.accept()
        return redirect("users:friendship_view_friends", username=request.user.username)

    return redirect(
        "users:friendship_requests_detail", friendship_request_id=friendship_request_id
    )


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_received, id=friendship_request_id
        )
        f_request.reject()
        return redirect("users:friendship_request_list")

    return redirect(
        "users:friendship_requests_detail", friendship_request_id=friendship_request_id
    )


@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_sent, id=friendship_request_id
        )
        f_request.cancel()
        return redirect("users:friendship_request_list")

    return redirect(
        "users:friendship_requests_detail", friendship_request_id=friendship_request_id
    )


@login_required
def friendship_request_list(
    request, template_name="users/friend_requests_list.html"
):
    """ View unread and read friendship requests """
    friendship_requests = Friend.objects.requests(request.user)
    # This shows all friendship requests in the database
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_request_list_rejected(
    request, template_name="users/requests_list.html"
):
    """ View rejected friendship requests """
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=False)

    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_requests_detail(
    request, friendship_request_id, template_name="users/request.html"
):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {"friendship_request": f_request})


def followers(request, username, template_name="users/followers.html"):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)
    ctx = {"followers": followers}
    return render(request, template_name, ctx)


def following(request, username, template_name="users/following.html"):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)
    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name(),
        'following': following,
    })


@login_required
def follower_add(
    request, followee_username, template_name="users/add_follower.html"
):
    """ Create a following relationship """
    ctx = {"followee_username": followee_username}

    if request.method == "POST":
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
        except AlreadyExistsError :
            return following(request, followee)
        else:
            return redirect("users:friendship_following", username=follower.username)

    return render(request, template_name, ctx)


@login_required
def follower_remove(
    request, followee_username, template_name="users/remove_follower.html"
):
    """ Remove a following relationship """
    if request.method == "POST":
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect("users:friendship_following", username=follower.username)

    return render(request, template_name, {"followee_username": followee_username})


def all_users(request, template_name="friendship/user_actions.html"):
    users = user_model.objects.all()

    return render(
        request, template_name, {get_friendship_context_object_list_name(): users}
    )


def blockers(request, username, template_name="users/blockers.html"):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    blockers = Block.objects.blocked(user)

    return render(
        request,
        template_name,
        {
            get_friendship_context_object_name(): user,
            "friendship_context_object_name": get_friendship_context_object_name(),
        },
    )


def blocking(request, username, template_name="users/blocking.html"):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    blocking = Block.objects.blocking(user)

    return render(
        request,
        template_name,
        {
            get_friendship_context_object_name(): user,
            "friendship_context_object_name": get_friendship_context_object_name(),
        },
    )


@login_required
def block_add(request, blocked_username, template_name="users/add_block.html"):
    """ Create a following relationship """
    ctx = {"blocked_username": blocked_username}

    if request.method == "POST":
        blocked = user_model.objects.get(username=blocked_username)
        blocker = request.user
        try:
            Block.objects.add_block(blocker, blocked)
        except AlreadyExistsError :
            return blocking(request, blocking)
        else:
            return redirect("users:friendship_blocking", username=blocker.username)

    return render(request, template_name, ctx)


@login_required
def block_remove(
    request, blocked_username, template_name="users/remove_block.html"
):
    """ Remove a following relationship """
    if request.method == "POST":
        blocked = user_model.objects.get(username=blocked_username)
        blocker = request.user
        Block.objects.remove_block(blocker, blocked)
        return redirect("users:friendship_blocking", username=blocker.username)

    return render(request, template_name, {"blocked_username": blocked_username})


