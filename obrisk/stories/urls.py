from django.conf.urls import url

from obrisk.stories import views
from obrisk.stories.search import SearchListView, get_suggestions
app_name = 'stories'
urlpatterns = [
    url(r'^$', views.StoriesListView.as_view(), name='list'),
    url(r'^delete/(?P<pk>[-\w]+)/$',
        views.StoriesDeleteView.as_view(), name='delete_stories'),
    url(r'^post-stories/$', views.post_stories, name='post_stories'),
    url(r'^story-images/$', views.get_story_images, name='story_images'), 
    url(r'^like/$', views.like, name='like_post'),
    url(r'^get-thread/$', views.get_thread, name='get_thread'),
    url(r'^story-likers/$', views.get_story_likers, name='get_likers'),
    url(r'^update-reaction-counts/$', views.update_reactions_count, name='one-time-update'),
    url(r'^post-comment/$', views.post_comment, name='post_comments'),
    url(r'^update-interactions/$', views.update_interactions, name='update_interactions'),
    url(r'^stories-search-reslts/$', SearchListView.as_view(), name='results'),
    url(r'^stories-suggestions/$', get_suggestions, name='suggestions'),
    
]
