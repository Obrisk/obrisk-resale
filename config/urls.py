from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from graphene_django.views import GraphQLView
from obrisk.messager import views
from obrisk.classifieds import views as images_views
from obrisk.posts import views as posts_views
from obrisk.posts.views import JobsCreateView, JobsListView, DetailJobsView, EventsListView, CreateEventsView, DetailEventsView

urlpatterns = [
    url(r'^create-jobs/$', JobsCreateView.as_view(), name='create_jobs'),
    url(r'^list-jobs/$', JobsListView.as_view(), name='list_jobs'),
    #url(r'^detail-jobs/$', DetailJobsView .as_view(), name='detail_jobs'),
    url(r'^create-events/$', CreateEventsView.as_view(), name='create_events'),
    url(r'^list-events/$', EventsListView.as_view(), name='list_events'),
    #url(r'^detail-events/$', DetailEventsView.as_view(), name='detail_events'),
    url(r'^(?P<events_id>\d+)$', DetailEventsView.as_view(), name='detail_events'),
    url(r'^(?P<events_id>\d+)$', DetailJobsView.as_view(), name='detail_jobs'),
    # url(r'^detail-events/(?P<events_id>\d+)/(?P<slug>[-\w]+)$', DetailEventsView.as_view()),
    #url(r'^detail-jobs/(?P<jobs_id>\d+)/(?P<slug>[-\w]+)$', DetailJobsView.as_view()),



    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^get-oss-auth/$', images_views.get_oss_auth, name='get_oss_auth'),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^terms-and-conditions/$',
        TemplateView.as_view(template_name='pages/terms.html'), name='terms_and_conditions'),
    url(r'^privacy-policy/$',
        TemplateView.as_view(template_name='pages/privacy.html'), name='privacy_policy'),
    url(r'^contacts/$',
        TemplateView.as_view(template_name='pages/contacts.html'), name='contacts'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    # User management
    url(r'^users/', include('obrisk.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    # Third party apps here
    url(r'^comments/', include('django_comments.urls')),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
    url(r'^markdownx/', include('markdownx.urls')),
    # Local apps here
    url(r'^ws/notifications/',
        include('obrisk.notifications.urls', namespace='notifications')),
    url(r'^classifieds/',
        include('obrisk.classifieds.urls', namespace='classifieds')),
    url(r'^posts/',
        include('obrisk.posts.urls', namespace='posts')),
    url(r'^stories/', include('obrisk.stories.urls', namespace='stories')),
    url(r'^ws/messages/',
        include('obrisk.messager.urls', namespace='messager')),
    url(r'^qa/', include('obrisk.qa.urls', namespace='qa')),
    url(r'^search/', include('obrisk.search.urls', namespace='search')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns