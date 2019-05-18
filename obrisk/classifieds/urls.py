from django.conf.urls import url
from django.views.generic import TemplateView

from obrisk.classifieds.views import (classified_list, CreateOfficialAdView, 
                                     CreateClassifiedView, EditClassifiedView, 
                                     ReportClassifiedView, DetailClassifiedView)
app_name = 'classifieds'
urlpatterns = [
    url(r'^$', classified_list, name='list'),
    url(r'^write-new-classified/$', CreateClassifiedView.as_view(), name='write_new'),
    url(r'^new-official-classified/$', CreateOfficialAdView.as_view(), name='write_new_official'),
    #url(r'^expired/$', ExpiredListView.as_view(), name='expired'),
    url(r'^tag/([-\w]+)/$', classified_list, name='list_by_tag'),
    url(r'^report/(?P<pk>\d+)/$', ReportClassifiedView.as_view(), name='report_classified'),
    url(r'^edit/(?P<pk>\d+)/$', EditClassifiedView.as_view(), name='edit_classified'),
    url(r'^(?P<slug>[-\w]+)/$', DetailClassifiedView.as_view(), name='classified'),
]
