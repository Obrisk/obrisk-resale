from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
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


send_upload_success.short_description = 'Send upload success'

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
    #readonly_fields = ('phone_number',)


admin.site.register(WechatUser)
