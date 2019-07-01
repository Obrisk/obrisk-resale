from django.conf.urls import url
from obrisk.posts import views as posts_views
from obrisk.posts.views import JobsCreateView, JobsListView, DetailJobsView, EventsListView, CreateEventsView, DetailEventsView
from obrisk.posts.views import (PostsListView, DraftsListView,
                                     CreatePostView, EditPostView,
                                     DetailPostView)
app_name = 'posts'
urlpatterns = [
    url(r'^create-jobs/$', JobsCreateView.as_view(), name='create_jobs'),   
    url(r'^list-jobs/$', JobsListView.as_view(), name='list_jobs'),
    url(r'^create-events/$', CreateEventsView.as_view(), name='create_events'),
    url(r'^list-events/$', EventsListView.as_view(), name='list_events'),
    # url(r'^detail-events/(?P<events_id>\d+)/$', DetailEventsView.as_view(), name='detail_events'),
    url(r'^detail-events/(?P<pk>[0-9]+)/$', DetailEventsView.as_view(), name='detail_events'),

    url(r'^detail-jobs/(?P<pk>\d+)/$', DetailJobsView.as_view(), name='detail_jobs'),

    url(r'^$', PostsListView.as_view(), name='list'),
    url(r'^write-new-post/$', CreatePostView.as_view(), name='write_new'),
    url(r'^drafts/$', DraftsListView.as_view(), name='drafts'),
    url(r'^edit/(?P<pk>\d+)/$', EditPostView.as_view(), name='edit_post'),
    url(r'^(?P<slug>[-\w]+)/$', DetailPostView.as_view(), name='post'),
]