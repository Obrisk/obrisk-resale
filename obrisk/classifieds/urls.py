from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.views.generic import TemplateView
from obrisk.classifieds.search import SearchListView, get_suggestions
from obrisk.classifieds.views import (
        classified_list, TagsAutoComplete,
        CreateClassifiedView, EditClassifiedView,
        ClassifiedDeleteView, ReportClassifiedView,
        DetailClassifiedView)

app_name = 'classifieds'

urlpatterns = [
    url(r'^$', classified_list, name='list'),
    url(
        r'^write-new-classified/$',
        CreateClassifiedView.as_view(),
        name='write_new'),
    url(r'^tags-autocomplete/$',
        TagsAutoComplete.as_view(),
        name='tags_autocomplete'),
    url(
        r'^tag/([-\w]+)/$',
        classified_list,
        name='list_by_tag'),
    url(
        r'^classifieds-search-results/$',
        SearchListView.as_view(),
        name='classifieds_results'),
    url(
        r'^classifieds-suggestions/$',
        get_suggestions,
        name='classifieds_suggestions'),
    url(
        r'^report/(?P<pk>\d+)/$',
        ReportClassifiedView.as_view(),
        name='report_classified'),
    url(
        r'^edit/(?P<pk>\d+)/$',
        EditClassifiedView.as_view(),
        name='edit_classified'),
    url(
        r'^delete/(?P<pk>[-\w]+)/$',
        ClassifiedDeleteView.as_view(),
        name='delete_classified'),
    url(
        r'^(?P<slug>[-\w]+)/$',
        DetailClassifiedView.as_view(),
        name='classified'),
]
