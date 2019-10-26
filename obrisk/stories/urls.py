from django.conf.urls import url

from obrisk.stories import views

app_name = 'stories'
urlpatterns = [
    url(r'^$', views.StoriesListView.as_view(), name='list'),
    url(r'^delete/(?P<pk>[-\w]+)/$',
        views.StoriesDeleteView.as_view(), name='delete_stories'),
    url(r'^post-stories/$', views.post_stories, name='post_stories'),
    url(r'^story-images/$', views.get_images_stories, name='story_images'), 
    url(r'^like/$', views.like, name='like_post'),
    url(r'^get-thread/$', views.get_thread, name='get_thread'),
    url(r'^post-comment/$', views.post_comment, name='post_comments'),
    url(r'^update-interactions/$', views.update_interactions, name='update_interactions'),
]
