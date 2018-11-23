from django.conf.urls import url

from obrisk.posts.views import (PostsListView, DraftsListView,
                                     CreatePostView, EditPostView,
                                     DetailPostView)
app_name = 'posts'
urlpatterns = [
    url(r'^$', PostsListView.as_view(), name='list'),
    url(r'^write-new-post/$', CreatePostView.as_view(), name='write_new'),
    url(r'^drafts/$', DraftsListView.as_view(), name='drafts'),
    url(r'^edit/(?P<pk>\d+)/$', EditPostView.as_view(), name='edit_post'),
    url(r'^(?P<slug>[-\w]+)/$', DetailPostView.as_view(), name='post'),
]
