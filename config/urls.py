from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name='about'),
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
    url(r'^notifications/',
        include('obrisk.notifications.urls', namespace='notifications')),
    url(r'^classifieds/',
        include('obrisk.classifieds.urls', namespace='classifieds')),
     url(r'^posts/',
        include('obrisk.posts.urls', namespace='posts')),
    url(r'^stories/', include('obrisk.stories.urls', namespace='stories')),
    url(r'^messages/',
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
