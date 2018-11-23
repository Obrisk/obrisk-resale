from django.conf.urls import url

from obrisk.classifieds.views import (ClassifiedsListView, DraftsListView,
                                     CreateClassifiedView, EditClassifiedView,
                                     DetailClassifiedView)
app_name = 'classifieds'
urlpatterns = [
    url(r'^$', ClassifiedsListView.as_view(), name='list'),
    url(r'^write-new-classified/$', CreateClassifiedView.as_view(), name='write_new'),
    url(r'^drafts/$', DraftsListView.as_view(), name='drafts'),
    url(r'^edit/(?P<pk>\d+)/$', EditClassifiedView.as_view(), name='edit_classified'),
    url(r'^(?P<slug>[-\w]+)/$', DetailClassifiedView.as_view(), name='classified'),
]
