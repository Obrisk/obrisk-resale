from django.conf.urls import url
from django.views.generic import TemplateView


from obrisk.classifieds.views import (ClassifiedsListView, ExpiredListView,
                                     CreateClassifiedView, EditClassifiedView, 
                                     ReportClassifiedView, DetailClassifiedView)
app_name = 'classifieds'
urlpatterns = [
    url(r'^$', ClassifiedsListView.as_view(), name='list'),
    url(r'^write-new-classified/$', CreateClassifiedView.as_view(), name='write_new'),
    url(r'^expired/$', ExpiredListView.as_view(), name='expired'),
    url(r'^report/(?P<pk>\d+)/$', ReportClassifiedView.as_view(), name='report_classified'),
    url(r'^edit/(?P<pk>\d+)/$', EditClassifiedView.as_view(), name='edit_classified'),
    url(r'^(?P<slug>[-\w]+)/$', DetailClassifiedView.as_view(), name='classified'),

]
