from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User
from django.shortcuts import render, get_object_or_404, redirect
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest, Block
get_friendship_context_object_name = lambda: getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user")
get_friendship_context_object_list_name = lambda: getattr( settings, "FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME", "users")


#FRIENDSHIP
def view_friends(request, username, template_name="connections/friends.html"):
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
    request, to_username, template_name="connections/add_friends.html"
):
    """ Create a FriendshipRequest """
    ctx = {"to_username": to_username}

    if request.method == "POST":
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        if Friend.objects.can_request_send(from_user, to_user) == True:
            return render(request, 'connections/pending_request.html', ctx)
        else:

            try:
                Friend.objects.add_friend(from_user, to_user)
            except AlreadyFriendsError :
                return view_friends(request, from_user)
            except AlreadyExistsError : 
                return view_friends(request, from_user)
            else:
                return redirect("messager:contacts_list")

    return render(request, template_name, ctx)


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_received, id=friendship_request_id
        )
        f_request.accept()
        return redirect("connections:friendship_view_friends", username=request.user.username)

    return redirect(
        "connections:friendship_requests_detail", friendship_request_id=friendship_request_id
    )


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_received, id=friendship_request_id
        )
        f_request.reject()
        return redirect("connections:friendship_request_list")

    return redirect("connections:friendship_view_friends", username=request.user.username)

@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_sent, id=friendship_request_id
        )
        f_request.cancel()
        return redirect("connections:friendship_request_list")

    return redirect(
        "connections:friendship_requests_detail", friendship_request_id=friendship_request_id
    )

@login_required
def friendship_requested_list(
    request, template_name="connections/friend_requested_list.html"
):
    """ View unread and read friendship requests """
    to_user = get_object_or_404(user_model, pk=6)

    sent_requests = FriendshipRequest.objects.filter(from_user=request.user)
    
    return render(request, template_name, {"sent_requests": sent_requests})



@login_required
def friendship_request_list(
    request, template_name="connections/friend_requests_list.html"
):
    """ View unread and read friendship requests """
    friendship_requests = Friend.objects.requests(request.user)
    # This shows all friendship requests in the database
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    
    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_request_list_rejected(
    request, template_name="connections/requests_list.html"
):
    """ View rejected friendship requests """
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=False)

    return render(request, template_name, {"requests": friendship_requests})


@login_required
def friendship_requests_detail(
    request, friendship_request_id, template_name="connections/request.html"
):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {"friendship_request": f_request})


def followers(request, username, template_name="connections/followers.html"):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)
    ctx = {"followers": followers}
    return render(request, template_name, ctx)


def following(request, username, template_name="connections/following.html"):
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
    request, followee_username, template_name="connections/add_follower.html"
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
            return redirect("connections:friendship_following", username=follower.username)

    return render(request, template_name, ctx)


@login_required
def follower_remove(
    request, followee_username, template_name="connections/remove_follower.html"
):
    """ Remove a following relationship """
    if request.method == "POST":
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect("connections:friendship_following", username=follower.username)

    return render(request, template_name, {"followee_username": followee_username})


def all_users(request, template_name="friendship/user_actions.html"):
    users = user_model.objects.all()

    return render(
        request, template_name, {get_friendship_context_object_list_name(): users}
    )


def blockers(request, username, template_name="connections/blockers.html"):
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


def blocking(request, username, template_name="connections/blocking.html"):
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
def block_add(request, blocked_username, template_name="connections/add_block.html"):
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
            return redirect("connections:friendship_blocking", username=blocker.username)

    return render(request, template_name, ctx)


@login_required
def block_remove(
    request, blocked_username, template_name="connections/remove_block.html"
):
    """ Remove a following relationship """
    if request.method == "POST":
        blocked = user_model.objects.get(username=blocked_username)
        blocker = request.user
        Block.objects.remove_block(blocker, blocked)
        return redirect("connections:friendship_blocking", username=blocker.username)

    return render(request, template_name, {"blocked_username": blocked_username})