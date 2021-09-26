from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'),

    url(regex=r'^social-form-final/$',
        view=views.SocialPostView.as_view(),
        name='social_final_form'),

    url(regex=r'^signup/$',
        view=views.EmailSignUp.as_view(),
        name='email_signup'),

    url(regex=r'^complete_login/$',
        view=views.complete_authentication,
        name='complete_auth'),

    url(regex=r'^verification-code/$',
        view=views.send_code_sms,
        name='verification_code'),

    url(regex=r'^phone-verify/$',
        view=views.phone_verify,
        name='phone_verify'),

    url(r'^wechat-auth/$',
        views.AuthView.as_view(),
        name='wechat_auth'),

    url(r'^wechat-test/$',
        views.wechat_getinfo_view_test,
        name='wechat_test'),

    url(regex=r'^cmplt-wx-reg-149eb8766awswdff224fgo029k12ol8/$',
        view=views.complete_wechat_reg,
        name='complete_wechat'),

    url(regex=r'^wx-auto-login-149eb8766awswdff224fgo029k12ol8/$',
        view=views.wechat_auto_login,
        name='wx_auto'),

    url(regex=r'^username-exists/$',
        view=views.username_exists,
        name='username_exists'),

    url(regex=r'^bulk-phone-update/$',
        view=views.bulk_update_user_phone_no,
        name='bulk_phone_update'),

    url(regex=r'^phone-password-reset/$',
        view=views.phone_password_reset,
        name='phone_password_reset'),

    url(regex=r'^phone-password-reset-form/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        view=views.PhonePasswordResetConfirmView.as_view(),
        name='phone_ps_reset_confirm'),

    url(regex=r'^update-profile-pic/$',
        view=views.update_profile_pic,
        name='update_profile_pic'),

    url(regex=r'^wsguatpotlfwccdi/admin-create-user/$',
        view=views.admin_create_user,
        name='update_profile_pic'),

    url(regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'),

    url(regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'),

    url(regex=r'^~update/$',
        view=views.VerifyAddressView.as_view(),
        name='update_address'),

    url(regex=r'^i/(?P<rq_user>[\w.@+-]+)/$',
        view=views.user_classifieds_list,
        name='user_classifieds'),

    url(regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'),
]
