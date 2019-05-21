from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from friendship import models
from friendship.models import (Block, Follow, Friend,
                               FriendshipRequest)
from requests_unixsocket import request
from werkzeug.utils import html

from .forms import UserForm
from .models import User


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




def friends_list(request):
    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)
    return all_friends
def follower_list(request):
    
    # List of this user's followers
    all_followers = Follow.objects.followers(request.user)
    return all_followers
def following_list(request):
    
    # List of who this user is following
    following = Follow.objects.following(request.user)
    return following
def manage_friends(request):
    
    ### Managing friendship relationships
    other_user = User.objects.get(pk=1)
    new_relationship = Friend.objects.add_friend(request.user, other_user)
    Friend.objects.are_friends(request.user, other_user) == True
    Friend.objects.remove_friend(other_user, request.user)
    return (other_user, new_relationship)

    # Can optionally save a message when creating friend requests
    #some_other_user = User.objects.get(pk=2)
    #message_relationship = Friend.objects.add_friend(
    #    from_user=request.user,
    #    to_user=some_other_user,
    #    message='Hi, I would like to be your friend',
    #)
    #return render(request, context=(some_other_user, message_relationship))

def friends_view(request):
    # Create request.user follows other_user relationship
    other_user = User.objects.get(pk=1)
    following_created = Follow.objects.add_follower(request.user, other_user)
    return following_created

def remove_follower(request):
    other_user = User.objects.get(pk=1)
    was_following = Follow.objects.remove_follower(request.user, other_user)
    return (was_following, other_user)

def block_friend(request):
    other_user = User.objects.get(pk=1)
    # Create request.user blocks other_user relationship
    block = Block.objects.add_block(request.user, other_user)
    return block

def unblock_friend(request):
    other_user = User.objects.get(pk=1)
    # Remove request.user blocks other_user relationship
    unblock = Block.objects.remove_block(request.user, other_user)
    return unblock