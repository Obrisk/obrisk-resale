from django.conf.urls import url
from obrisk.stories import views
from obrisk.stories.search import (
        SearchListView, get_suggestions)
from obrisk.utils.images_upload import bulk_update_vid_images

app_name = 'stories'
urlpatterns = [
    url(r'^$', views.stories_list, name='list'),
    url(
        r'^post-stories/$',
        views.post_stories,
        name='post_stories'),
    url(
        r'^story-images/$',
        views.get_story_images, name='story_images'),
    url(
        r'^like/$',
        views.like,
        name='like_post'),
    url(
        r'^get-thread/$',
        views.get_thread,
        name='get_thread'),
    url(
        r'^story-update-vids/$',
        bulk_update_vid_images,
        name='get_vids'),
    url(
        r'^story-likers/$',
        views.get_story_likers,
        name='get_likers'),
    url(
        r'^update-reaction-counts/$',
        views.update_reactions_count,
        name='one-time-update'),
    url(
        r'^post-comment/$',
        views.post_comment,
        name='post_comments'),
    url(
        r'^update-interactions/$',
        views.update_interactions,
        name='update_interactions'),
    url(
        r'^stories-search-reslts/$',
        SearchListView.as_view(),
        name='results'),
    url(
        r'^stories-suggestions/$',
        get_suggestions,
        name='suggestions'),
    url(
        r'^delete/(?P<pk>[-\w]+)/$',
        views.StoriesDeleteView.as_view(),
        name='delete_stories'),
    url(
        r'^tag/([-\w]+)/$',
        views.stories_list,
        name='list_by_tag'),
    url(r'^i/(?P<slug>[-\w]+)/$',
        views.stories_list,
        name='story'),
]
