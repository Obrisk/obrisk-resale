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
from werobot.contrib.django import make_view

from obrisk.users.wechat.wx_chatbot import wxbot
from obrisk.users.views import (
    PasswordResetFromKeyView,
    GetInfoView
)
from obrisk.utils.images_upload import get_oss_auth
from obrisk.utils.wx_config import request_wx_credentials
from obrisk.classifieds.sitemaps import ClassifiedsSitemap
from obrisk.posts.sitemaps import PostsSitemap
from obrisk.qa.sitemaps import QASitemap
from config.sitemaps import StaticSitemap
from obrisk.utils.sentry import trigger_error


sitemaps = {
    "pages": StaticSitemap,
    "classifieds": ClassifiedsSitemap,
    "questions": QASitemap,
    "posts": PostsSitemap
}


urlpatterns = [
    url(r"", include("pwa_webpush.urls")),
    url(r"^$",
        TemplateView.as_view(template_name="pages/home.html"),
        name="home"
    ),
    url(r'^i18n/',
        include('django.conf.urls.i18n')
    ),
    # Redirect all classifieds to i/ url pattern
    url(r"^i/",
        include("obrisk.classifieds.urls",
            namespace="classifieds")
    ),
    url(r"^classifieds/",
        include("obrisk.classifieds.urls",
            namespace="old_classifieds_url")
    ),
    url(r'^MP_verify_HTQQQmxtxv6VNTtN.txt$',
        TemplateView.as_view(template_name="MP_verify_HTQQQmxtxv6VNTtN.txt",
        content_type="text/plain"), name="MP_verify_HTQQQmxtxv6VNTtN.txt"
    ),
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
    url(r'^wx-auth/$',
        GetInfoView.as_view(),
        name='wechat_info'
    ),
    url(r'^obdev2018-wsguatpotlfwccdi-wx-auth/$',
        request_wx_credentials,
        name='wx_req_cred'
    ),
    url(r"^get-oss-auth/$", get_oss_auth, name="get_oss_auth"),
    url(r"^get-oss-auth/([\w\.%+-]+)/$",
        get_oss_auth,
        name="get_oss_auth_with_object"
    ),
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
    url(r"^users/", include("obrisk.users.urls", namespace="users")),
    url(r"^auth/", include("allauth.urls")),

    # Third party apps here
    url(r"^graphql", GraphQLView.as_view(graphiql=True)),
    url(r"^markdownx/", include("markdownx.urls")),
    # Local apps here
    url(r"^connections/",
        include("obrisk.connections.urls",
        namespace="connections")
        ),
    url(
        r"^ws/notifications/",
        include("obrisk.notifications.urls", namespace="notifications"),
    ),
    url(r"^ws/messages/",
        include("obrisk.messager.urls",
        namespace="messager")),
    url(r"^qa/",
        include("obrisk.qa.urls",
        namespace="qa")),
    url(r"^posts/",
        include("obrisk.posts.urls",
        namespace="posts")),
    url(r"^search/",
        include("obrisk.search.urls",
        namespace="search")),
    url(
        r"^obdev2018-wsguatpotlfwccdi-sentry-error/",
        trigger_error, name="sentry_debug"
    ),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    url(
        r"^biR07IOg1Xgy66Hpypet-wsguatpotlfwccdi-wxbot/",
        make_view(wxbot), name="wechat_users"
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

        urlpatterns = [url
            (
                r"^__debug__/",
                include(debug_toolbar.urls)
            ),] + urlpatterns

