from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.views.generic import TemplateView
from obrisk.classifieds.search import SearchListView, get_suggestions
from obrisk.classifieds.views import *
from obrisk.utils.images_upload import bulk_update_classifieds_thumb

app_name = 'classifieds'

urlpatterns = [
    url(r'^$',
        classified_list,
        name='list'),
    url(
        r'^write-new-classified/$',
        CreateClassifiedView.as_view(),
        name='write_new'),
    url(r'^tags-autocomplete/$',
        ClassifiedTagsAutoComplete.as_view(),
        name='tags_autocomplete'),
    url(
        r'^tag/([-\w]+)/$',
        classified_list_by_tags,
        name='list_by_tag'),
    url(
        r'^city/([-\w]+)/$',
        classified_list,
        name='list_by_city'),
    url(
        r'^classifieds-search-results/$',
        SearchListView.as_view(),
        name='classifieds_results'),
    url(
        r'^clsupdate/$',
        bulk_update_classifieds_thumb,
        name='bulk-update'
        ),
    url(
        r'^classifieds-suggestions/$',
        get_suggestions,
        name='classifieds_suggestions'),
    url(
        r'^orders/create-clsd-order/$',
        create_classified_order,
        name='create_order'),
    url(
        r'^orders/wxpy-complete/$',
        initiate_wxpy_info,
        name='initiate_wxpy_info'),
    url(
        r'^orders/wsguatpotlfwccdi/wxjs-success/$',
        wxpyjs_success,
        name='wxpyjs_success'),
    url(
        r'^wsguatpotlfwccdi/wxjsapipy/inwxpy-results/$',
        Wxpay_Result.as_view(),
        name='inwxpy_res'),
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
        r'^orders/wsguatpotlfwccdi/(?P<slug>[-\w]+)/$',
        ClassifiedOrderView.as_view(),
        name='order_detail'),
    url(
        r'^(?P<slug>[-\w]+)/$',
        DetailClassifiedView.as_view(),
        name='classified'),
]
