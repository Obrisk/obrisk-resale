from django.conf.urls import url
from obrisk.posts import views
from obrisk.posts.views import (PostsListView, DraftsListView,
                                    CreatePostView, EditPostView,
                                    DetailPostView,CreateJobsView,
                                    CreateEventsView, DetailJobsView,
                                    DetailEventsView,JobsListView,
                                    EventsListView)
app_name = 'posts'
urlpatterns = [
    url(r'^$', PostsListView.as_view(), name='list'),
    url(r'^new-jobs/$', views.CreateJobsView, name='new_jobs'),
    url(r'^new-events/$', views.CreateEventsView, name='new_events'),
    url(r'^write-new-post/$', CreatePostView.as_view(), name='write_new'),
    url(r'^drafts/$', DraftsListView.as_view(), name='drafts'),
    url(r'^edit/(?P<pk>\d+)/$', EditPostView.as_view(), name='edit_post'),
    
    url(r'^(?P<slug>[-\w]+)/$', DetailJobsView.as_view(), name='jobs'),
    url(r'^(?P<slug>[-\w]+)/$', DetailEventsView.as_view(), name='events'),
    url(r'^(?P<slug>[-\w]+)/$', DetailPostView.as_view(), name='post'),
]
