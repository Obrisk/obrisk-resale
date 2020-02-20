from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _
from django.conf import settings

from allauth.account.forms import (
    SignupForm,
    LoginForm,
    ResetPasswordForm,
    PasswordField,
)
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
        fields = ("username", "country", "city")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class UserForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
    province_region = forms.CharField(widget=forms.HiddenInput())
    city = forms.CharField(widget=forms.HiddenInput())
    job_title = forms.CharField(required=False, label=("Occupation"))
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("name", "job_title", "province_region", "city", "bio", "address")
        help_texts = {
            # "linkedin_account": "Your linkedin username as it appears on your linkedin profile page.\
            #     Make sure it is spelled correctly",
            "bio": "A short introduction about yourself",
            "address": "English address is preferred, don't include your City and Province",
        }


# This form inherits all-auth.
class PhoneSignupForm(SignupForm):
    province_region = forms.CharField(widget=forms.HiddenInput())
    city = forms.CharField(widget=forms.HiddenInput())
    phone_number = PhoneNumberField(
        label=_("Phone number"),
        widget=forms.TextInput(attrs={"autofocus": "autofocus", "maxlength": "11"}),
    )

    class Meta:
        model = User
        help_texts = {
            "username": "At least 3 characters, no special characters",
        }
        fields = (
            "username",
            "city",
            "province_region",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(PhoneSignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(label=_("Password"))

        if getattr(settings, "SIGNUP_PASSWORD_ENTER_TWICE", True):
            self.fields["password2"] = PasswordField(label=_("Password (again)"))

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

        for fieldname in ["password1"]:
            self.fields[
                fieldname
            ].help_text = (
                "At least 8 character, can't be too common or entirely numeric"
            )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(PhoneSignupForm, self).save(request)

        user.province_region = self.cleaned_data["province_region"]
        user.city = self.cleaned_data["city"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save()

        # You must return the original result.
        return user


class EmailSignupForm(SignupForm):
    province_region = forms.CharField(widget=forms.HiddenInput())
    city = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        help_texts = {
            "username": "At least 3 characters, no special characters",
        }
        fields = (
            "username",
            "city",
            "province_region",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(EmailSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"] = forms.EmailField(
            label=_("E-mail"),
            required=True,
            widget=forms.TextInput(
                attrs={
                    "type": "email",
                    "size": "30",
                    "placeholder": _("E-mail address"),
                }
            ),
        )
        self.fields["password1"] = PasswordField(label=_("Password"))

        if getattr(settings, "SIGNUP_PASSWORD_ENTER_TWICE", True):
            self.fields["password2"] = PasswordField(label=_("Password (again)"))

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

        for fieldname in ["password1"]:
            self.fields[
                fieldname
            ].help_text = (
                "At least 8 character, can't be too common or entirely numeric"
            )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(EmailSignupForm, self).save(request)

        user.province_region = self.cleaned_data["province_region"]
        user.city = self.cleaned_data["city"]
        user.save()

        # You must return the original result.
        return user


class CustomLoginForm(LoginForm):
    password = PasswordField(label=_(""))

    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        # This error message includes both username or phone number
        "username_password_mismatch": _(
            "The phone number/username or password you specified are not correct."
        ),
        "email_password_mismatch": _(
            "The e-mail address or password you specified are not correct."
        ),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        assert settings.ACCOUNT_AUTHENTICATION_METHOD == "username_email"
        login_widget = forms.TextInput(
            attrs={"placeholder": _(""), "autofocus": "autofocus",}
        )

        login_field = forms.CharField(
            label="Phone or username or email", widget=login_widget
        )

        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)


class PhoneRequestPasswordForm(forms.Form):
    phone_number = forms.IntegerField(
        label=_("Phone number"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "tel", "placeholder": _("Phone number you registered with"),}
        ),
    )


class PhoneResetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label=("New password confirmation"), widget=forms.PasswordInput
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages["password_mismatch"], code="password_mismatch",
                )
        return password2
