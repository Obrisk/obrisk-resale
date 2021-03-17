from django.conf.urls import url
from obrisk.connections.search import SearchListView

# friendship
from obrisk.connections.views import (
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

app_name = "connections"
urlpatterns = [
    # friendship
    url(
        r"^users-search-results/$",
        SearchListView.as_view(),
        name="users_search_results",
    ),
    url(regex=r"^users/$", view=all_users, name="friendship_view_users"),
    url(regex=r"^friends/$", view=view_friends, name="friendship_view_friends",),
    url(
        regex=r"^friend/add/(?P<to_username>[\w-]+)/$",
        view=friendship_add_friend,
        name="friendship_add_friend",
    ),
    url(
        regex=r"^request/accept/(?P<friendship_request_id>\d+)/$",
        view=friendship_accept,
        name="friendship_accept",
    ),
    url(
        regex=r"^request/reject/(?P<friendship_request_id>\d+)/$",
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
    url(regex=r"^followers/$", view=followers, name="friendship_followers",),
    url(regex=r"^following/$", view=following, name="friendship_following",),
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
]
