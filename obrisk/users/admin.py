import logging
import itertools
from django.urls import reverse
from django import forms
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils.text import slugify as dj_slugify
from .forms import CustomUserCreationForm, CustomUserChangeForm

from obrisk.users.models import User, WechatUser
from obrisk.messager.send_wxtemplate import upload_success_wxtemplate


class MyUserChangeForm(CustomUserChangeForm):
    class Meta(CustomUserChangeForm.Meta):
        model = User


class MyUserCreationForm(CustomUserCreationForm):

    error_message = CustomUserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(CustomUserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)

        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])


def send_upload_success(modeladmin, request, queryset):
    for user in queryset:
        if not user.is_authenticated:
            login(
                request, user,
                backend='django.contrib.auth.backends.ModelBackend'
            )

        upload_success_wxtemplate(user)


def create_obrisk_user(modeladmin, request, queryset):
    for user in queryset:
        username = user.name = dj_slugify(
                user.name,
                allow_unicode=True
            )
        if User.objects.filter(username=username).exists():
            for x in itertools.count(1):
                if not User.objects.filter(username=username).exists():
                    break
                username = '%s-%d' % (user.name, x)
            user.name = username

        try:
            user = User.objects.create(
                username=user.name,
                wechat_openid=user.wechat_openid,
                thumbnail = user.thumbnail,
                picture = user.picture,
                org_picture = user.org_picture,
                gender=user.gender,
                country='China'
            )

        except Exception as e:
            logging.error(
                'Creating the Obrisk user failed',
                exc_info=e
            )
            return

        return HttpResponseRedirect(
                   f'/users/wsguatpotlfwccdi/admin-create-user/{user.pk}/'
                )


send_upload_success.short_description = 'Send upload success'
create_obrisk_user.short_description = 'Create Obrisk user'


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    ordering = ('-date_joined', )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile',
                {'fields':
                    ('name', 'is_official', 'is_seller', 'points', 'city',
                        'province_region', 'country', 'phone_number', 'picture',
                        'thumbnail', 'org_picture', 'linkedin_account', 'wechat_id', 'notes',
                        'english_address', 'chinese_address', 'gender', 'wechat_openid',
                    )
                }
            ),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'last_login', 'date_joined',
        'city', 'province_region', 'thumbnail', 'points')
    search_fields = ['username', 'phone_number', 'email', 'city']
    actions = [send_upload_success,]


@admin.register(WechatUser)
class MyUserAdmin(admin.ModelAdmin):
    def obrisk_user(self, obj):
        if obj.wechat_openid is not None:
            if User.objects.filter(wechat_openid=obj.wechat_openid).exists():
                return 'YES'
        return 'NO'

    list_display = ('name', 'obrisk_user', 'city', 'province_region')
    search_fields = ['name', 'wechat_openid']
    actions = [create_obrisk_user,]
