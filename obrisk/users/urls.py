from django.conf.urls import url

from . import views

#friendship
from obrisk.users.views import (
    view_friends,
    friendship_add_friend,
    friendship_accept,
    friendship_reject,
    friendship_cancel,
    friendship_request_list,
    friendship_request_list_rejected,
    friendship_requests_detail,
    followers,
    following,
    follower_add,
    follower_remove,
    all_users,
    block_add,
    block_remove,
    blockers,
    blocking,
)

app_name = 'users'
urlpatterns = [
    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    url(regex=r'^signup/$', view=views.SignUp.as_view(), name='signup'),
    url(regex=r'^verification-code/$', view=views.send_code_sms, name='verification_code'),
    url(regex=r'^phone-verify/$', view=views.phone_verify, name='phone_verify'),
    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(), name='update'),
    url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    
     #friendship
    url(regex=r"^users/$", view=all_users, name="friendship_view_users"),
    url(
        regex=r"^friends/(?P<username>[\w-]+)/$",
        view=view_friends,
        name="friendship_view_friends",
    ),
    url(
        regex=r"^friend/add/(?P<to_username>[\w-]+)/$",
        view=friendship_add_friend,
        name="friendship_add_friend",
    ),
    url(
        regex=r"^friend/accept/(?P<friendship_request_id>\d+)/$",
        view=friendship_accept,
        name="friendship_accept",
    ),
    url(
        regex=r"^friend/reject/(?P<friendship_request_id>\d+)/$",
        view=friendship_reject,
        name="friendship_reject",
    ),
    url(
        regex=r"^friend/cancel/(?P<friendship_request_id>\d+)/$",
        view=friendship_cancel,
        name="friendship_cancel",
    ),
    url(
        regex=r"^friend/requests/$",
        view=friendship_request_list,
        name="friendship_request_list",
    ),
    url(
        regex=r"^friend/requests/rejected/$",
        view=friendship_request_list_rejected,
        name="friendship_requests_rejected",
    ),
    url(
        regex=r"^friend/request/(?P<friendship_request_id>\d+)/$",
        view=friendship_requests_detail,
        name="friendship_requests_detail",
    ),
    url(
        regex=r"^followers/(?P<username>[\w-]+)/$",
        view=followers,
        name="friendship_followers",
    ),
    url(
        regex=r"^following/(?P<username>[\w-]+)/$",
        view=following,
        name="friendship_following",
    ),
    url(
        regex=r"^follower/add/(?P<followee_username>[\w-]+)/$",
        view=follower_add,
        name="follower_add",
    ),
    url(
        regex=r"^follower/remove/(?P<followee_username>[\w-]+)/$",
        view=follower_remove,
        name="follower_remove",
    ),
    url(
        regex=r"^blockers/(?P<username>[\w-]+)/$",
        view=blockers,
        name="friendship_blockers",
    ),
    url(
        regex=r"^blocking/(?P<username>[\w-]+)/$",
        view=blocking,
        name="friendship_blocking",
    ),
    url(
        regex=r"^block/add/(?P<blocked_username>[\w-]+)/$",
        view=block_add,
        name="block_add",
    ),
    url(
        regex=r"^block/remove/(?P<blocked_username>[\w-]+)/$",
        view=block_remove,
        name="block_remove",
    ),
    url(
        regex=r"^followers/(?P<username>[\w-]+)/$",
        view=followers,
        name="friendship_followers",
    ),
  
]
