from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _
from django.conf import settings

from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, PasswordField
from allauth.utils import (
    build_absolute_uri,
    get_username_max_length,
    set_form_field_order,
)
from allauth.account import app_settings
from phonenumber_field.formfields import PhoneNumberField
from obrisk.users import models

from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'country', 'city')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields

class UserForm(forms.ModelForm):
    bio = forms.CharField (widget=forms.Textarea(attrs={'rows': 3}), required=False) 
    province_region = forms.CharField (widget=forms.HiddenInput())
    city = forms.CharField (widget=forms.HiddenInput())
    oss_image = forms.CharField (widget=forms.HiddenInput(), required=False)
    class Meta:
        model = User
        fields = ('name', 'job_title', 'province_region', 'city', 'bio', 'instagram_account',
               'linkedin_account','snapchat_account', 'facebook_account' )
        help_texts = {
            "instagram_account": "(Optional) Please fill in your instagram username as it appears on your instagram profile page.\
                 Make sure it is spelled correctly",
            "linkedin_account": "(Optional) Please fill in your linkedin username as it appears on your linkedin profile page.\
                 Make sure it is spelled correctly",
            "facebook_account": "(Optional) Please fill in your facebook username as it appears on your facebook profile page.\
                 Make sure it is spelled correctly",
            "snapchat_account": "(Optional) Please fill in your snapchat username as it appears on your snapchat profile page.\
                 Make sure it is spelled correctly.",
        }
    

#This form inherits Allauth Signup Form 
class CustomSignupForm(SignupForm): 
    province_region = forms.CharField (widget=forms.HiddenInput())
    city = forms.CharField (widget=forms.HiddenInput())

    class Meta:
        model = User

def signup(self, request, user): 
    user.province_region = self.cleaned_data['province_region']
    user.city = self.cleaned_data['city']
    user.save() 
    return user 

#This form inherits all-auth. 
class PhoneSignupForm(SignupForm): 
    province_region = forms.CharField (widget=forms.HiddenInput())
    city = forms.CharField (widget=forms.HiddenInput())
    phone_number = PhoneNumberField(label=_("Phone number"),
                                    widget=forms.TextInput(
                                    attrs={'placeholder': _('e.g 13299887766'),
                                          'autofocus': 'autofocus'})
                            )

    class Meta:
        model = User
        help_texts = {
            'username': "At least 3 characters, no special characters",
        }
        fields = ( 'username', 'city', 'province_region', 'phone_number', 'password1', 'password2') 

    def __init__(self, *args, **kwargs):
        super(PhoneSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label=_("Password"))

        if getattr(settings, 'SIGNUP_PASSWORD_ENTER_TWICE', True):
            self.fields['password2'] = PasswordField(
                label=_("Password (again)"))

        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = "At least 8 character, can't be too common or entirely numeric"

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(PhoneSignupForm, self).save(request)

        user.province_region = self.cleaned_data['province_region']
        user.city = self.cleaned_data['city']
        user.phone_number = self.cleaned_data['phone_number']
        user.save() 

        # You must return the original result.
        return user


class EmailSignupForm(SignupForm): 
    province_region = forms.CharField (widget=forms.HiddenInput())
    city = forms.CharField (widget=forms.HiddenInput())

    class Meta:
        model = User
        help_texts = {
            'username': "At least 3 characters, no special characters",
        } 
        fields = ( 'username', 'city', 'province_region', 'phone_number', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(EmailSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
                                        label=_("E-mail"),required=True,
                                        widget=forms.TextInput(
                                            attrs={"type": "email",
                                                "size": "30",
                                                "placeholder": _('E-mail address')}
                                            )
                                        )
        self.fields['password1'] = PasswordField(label=_("Password"))

        if getattr(settings, 'SIGNUP_PASSWORD_ENTER_TWICE', True):
            self.fields['password2'] = PasswordField(
                label=_("Password (again)"))

        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = "At least 8 character, can't be too common or entirely numeric"

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(EmailSignupForm, self).save(request)

        user.province_region = self.cleaned_data['province_region']
        user.city = self.cleaned_data['city']
        user.save() 

        # You must return the original result.
        return user



class CustomLoginForm(LoginForm):
    error_messages = {
        'account_inactive':
        _("This account is currently inactive."),

        'username_password_mismatch':
        _("The username and/or password you specified are not correct."),

        'email_password_mismatch':
        _("The e-mail address and/or password you specified are not correct."),

    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        
        if settings.ACCOUNT_AUTHENTICATION_METHOD == 'email':
            login_widget = forms.TextInput(attrs={'type': 'email',
                                                  'placeholder':
                                                  _('E-mail address'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.EmailField(label=_("E-mail"),
                                           widget=login_widget)
        elif settings.ACCOUNT_AUTHENTICATION_METHOD \
                == 'username':
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length())
        else:
            assert settings.ACCOUNT_AUTHENTICATION_METHOD \
                == 'username_email'
            login_widget = forms.TextInput(attrs={'placeholder':
                                                    _('Username or Phone or Email'),
                                                    'autofocus': 'autofocus'})
        
            login_field = forms.CharField(label="Login", widget=login_widget)

        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if settings.SESSION_REMEMBER is not None:
            del self.fields['remember']

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)


class PhoneResetPasswordForm (forms.Form):
    phone_number = forms.IntegerField(
        label=_("Phone number"),
        required=True,
        widget=forms.TextInput(attrs={
            "type": "tel",
            "placeholder": _("Phone number you registered with"),
        })
    )