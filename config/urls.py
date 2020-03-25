from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView

from graphene_django.views import GraphQLView
from pwa_webpush.views import save_info
from obrisk.users.views import PasswordResetFromKeyView, AutoLoginView
from obrisk.utils.images_upload import get_oss_auth
from obrisk.classifieds.sitemaps import ClassifiedsSitemap
from obrisk.posts.sitemaps import PostsSitemap
from obrisk.qa.sitemaps import QASitemap
from config.sitemaps import StaticSitemap
from obrisk.utils.sentry import trigger_error


sitemaps = {
    "pages": StaticSitemap,
    "classifieds": ClassifiedsSitemap,
    "posts": PostsSitemap,
    "questions": QASitemap,
}


urlpatterns = [
    url(r"", include("pwa_webpush.urls")),
    url(r"^$", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    url(
        r"^download-pwa/$",
        TemplateView.as_view(template_name="pages/download.html"),
        name="download_pwa",
    ),
    url(
        r"^offline/$",
        TemplateView.as_view(template_name="offline.html"),
        name="offline",
    ),
    url(r"^get-oss-auth/$", get_oss_auth, name="get_oss_auth"),
    url(r"^get-oss-auth/([\w\.%+-]+)/$", get_oss_auth, name="get_oss_auth_with_object"),
    url(
        r"^about/$",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    url(
        r"^terms-and-conditions/$",
        TemplateView.as_view(template_name="pages/terms.html"),
        name="terms_and_conditions",
    ),
    url(
        r"^privacy-policy/$",
        TemplateView.as_view(template_name="pages/privacy.html"),
        name="privacy_policy",
    ),
    url(
        r"^contacts/$",
        TemplateView.as_view(template_name="pages/contacts.html"),
        name="contacts",
    ),
    url(r"^webpush/save_information", save_info, name="save_push_info"),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    url(
        r"^auth/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    # User management
    url(
        r'^accounts-authorization/signup/', 
        RedirectView.as_view(
            pattern_name='account_signup', permanent=False)
    ),
    url(
        r'^accounts-authorization/login/', 
        RedirectView.as_view(
            pattern_name='account_login', permanent=False)
    ),
    url(r"^users/", include("obrisk.users.urls", namespace="users")),
    url(r"^auth/", include("allauth.urls")),
    url(
        r"^auto-login-obdev2018-wsguatpotlfwccdi/",
        AutoLoginView.as_view(),
        name="auto_login",
    ),
    # Third party apps here
    url(r"^graphql", GraphQLView.as_view(graphiql=True)),
    url(r"^markdownx/", include("markdownx.urls")),
    # Local apps here
    url(r"^connections/", include("obrisk.connections.urls", namespace="connections")),
    url(
        r"^ws/notifications/",
        include("obrisk.notifications.urls", namespace="notifications"),
    ),
    url(r"^classifieds/", include("obrisk.classifieds.urls", namespace="classifieds")),
    url(r"^posts/", include("obrisk.posts.urls", namespace="posts")),
    url(r"^stories/", include("obrisk.stories.urls", namespace="stories")),
    url(r"^ws/messages/", include("obrisk.messager.urls", namespace="messager")),
    url(r"^qa/", include("obrisk.qa.urls", namespace="qa")),
    url(r"^search/", include("obrisk.search.urls", namespace="search")),
    url(
        r"^obdev2018-wsguatpotlfwccdi-sentry-error/", trigger_error, name="sentry_debug"
    ),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development
    urlpatterns += [
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns

