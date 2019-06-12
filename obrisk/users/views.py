from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

<<<<<<< HEAD

#from friendship.views import friendship_request_list
=======
>>>>>>> b89b97e26440ee34af1a6c0c2a1d1be2a8a78a59
from friendship.exceptions import AlreadyExistsError
from friendship import models
from friendship.models import (Block, Follow, Friend,
                               FriendshipRequest)
from werkzeug.utils import html

from .forms import UserForm
from .models import User

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')

from django.conf import settings

from django.contrib.auth import get_user_model
user_model = get_user_model

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


# friendship followship

def view_friends(request, username, template_name='friendship/friend/user_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)
    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


@login_required
def friendship_add_friend(request, to_username, template_name='friendship/friend/add.html'):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username}

    if request.method == 'POST':
        to_user =get_user_model().objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('friendship_request_list')

    return render(request, template_name, ctx)


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.reject()
        return redirect('friendship_request_list')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_sent,
            id=friendship_request_id)
        f_request.cancel()
        return redirect('friendship_request_list')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)



@login_required
def followers(request, username, template_name='friendship/follow/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })

@login_required
def following(request, username, template_name='friendship/follow/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


@login_required
def follower_add(request, followee_username, template_name='friendship/follow/add.html'):
    """ Create a following relationship """
    ctx = {'followee_username': followee_username}

    if request.method == 'POST':
        followee = get_user_model().objects.get(username=followee_username)
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('friendship_following', username=follower.username)

    return render(request, template_name, ctx)


@login_required
def follower_remove(request, followee_username, template_name='friendship/follow/remove.html'):
    """ Remove a following relationship """
    if request.method == 'POST':
        followee = get_user_model().objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect('friendship_following', username=follower.username)

    return render(request, template_name, {'followee_username': followee_username})


@login_required
def all_users(request, template_name="friendship/user_actions.html"):
    users = get_user_model().objects.all()

    return render(request, template_name, {get_friendship_context_object_list_name(): users})


@login_required
def blocking(request, username, template_name='friendship/block/blockers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    blockers = Block.objects.blocked(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


@login_required
def blockers(request, username, template_name='friendship/block/blocking_list.html'):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    blocking = Block.objects.blocking(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


@login_required
def block_add(request, blocked_username, template_name='friendship/block/add.html'):
    """ Create a following relationship """
    ctx = {'blocked_username': blocked_username}

    if request.method == 'POST':
        blocked = get_user_model().objects.get(username=blocked_username)
        blocker = request.user
        try:
            Block.objects.add_block(blocker, blocked)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('friendship_blocking', username=blocker.username)

    return render(request, template_name, ctx)


@login_required
def block_remove(request, blocked_username, template_name='friendship/block/remove.html'):
    """ Remove a following relationship """
    if request.method == 'POST':
        blocked = get_user_model().objects.get(username=blocked_username)
        blocker = request.user
        Block.objects.remove_block(blocker, blocked)
        return redirect('friendship_blocking', username=blocker.username)

    return render(request, template_name, {'blocked_username': blocked_username})

@login_required
def friends_list(request):
    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)
    return render(request, 'friends_list.html', {"all_friends":all_friends})

@login_required

def follower_list(request):
    
    # List of this user's followers
    all_followers = Follow.objects.followers(request.user)
    return render(request, 'follower_list.html', {"all_followers":all_followers})

@login_required

def following_list(request):

    # List of who this user is following
    following = Follow.objects.following(request.user)
    return render(request, 'following_list.html', {"following":following})

@login_required
def friendship_request_list(
    request, template_name="friendship/friend/requests_list.html"
):
    """ View unread and read friendship requests """
    friendship_requests = Friend.objects.requests(request.user)
    # This shows all friendship requests in the database
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {"requests": friendship_requests})