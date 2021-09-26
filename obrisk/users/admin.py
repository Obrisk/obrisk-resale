import logging
import itertools
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.db import IntegrityError
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
        upload_success_wxtemplate(user)


def create_obrisk_user(modeladmin, request, queryset):
    for user in queryset:
        try:
            user = User.objects.create(
                wechat_openid=user.wechat_openid,
                thumbnail = user.thumbnail,
                picture = user.mid,
                org_picture = user.full,
                gender=user.gender,
                city=user.city,
                province_region=user.province_region,
                country=user.country
            )

        except IntegrityError:
            return
        except Exception as e:
            logging.error('Creating the Obrisk user failed', exc_info=e)
            return

        username = first_name = dj_slugify(
                user.username,
                allow_unicode=True
            )

        for x in itertools.count(1):
            if not User.objects.filter(username=username).exists():
                break
            username = '%s-%d' % (first_name, x)
        user.username = username
        user.save()

        return HttpResponseRedirect(
            '/users/wsguatpotlfwccdi/admin-create-user/?pk=%s&nm=%s&ct=%s&pr=%s&cn=%s' % (
                str(user.id), username,
                user.city, user.province_region, user.country
            )
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
    list_display = ('name', 'city', 'province_region')
    search_fields = ['name', 'wechat_openid']
    actions = [create_obrisk_user,]
