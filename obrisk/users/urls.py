from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    url(regex=r'^signup/$', view=views.SignUp.as_view(), name='signup'),
    url(regex=r'^verification-code/$', view=views.send_code_sms, name='verification_code'),
    url(regex=r'^phone-verify/$', view=views.phone_verify, name='phone_verify'),
    url(regex=r'^phone-password-reset/$', view=views.phone_password_reset, name='phone_password_reset'),
    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(), name='update'),
    url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
]
