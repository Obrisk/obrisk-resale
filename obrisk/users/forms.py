from django import forms
from django.contrib.auth.forms import (
        UserCreationForm, UserChangeForm
    )
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import validators
from django.forms.widgets import Select, SelectMultiple
from django.contrib.auth import get_user_model

from allauth.account.forms import (
    SignupForm, LoginForm, PasswordField)
from allauth.utils import (
    set_form_field_order)
from allauth.socialaccount.forms import (
        SignupForm as SocialSignupForm
    )
from phonenumber_field.formfields import PhoneNumberField

from obrisk.users.wechat_config import CHINA_PROVINCES

User = get_user_model()



class SelectWidget(Select):
    """
    Select With Option Attributes:
        subclass of Django's Select widget that allows attributes in options,
        like disabled="disabled", title="help text", class="some classes",
              style="background: color;"...

    Pass a dict instead of a string for its label:
        choices = [ ('value_1', 'label_1'),
                    ...
                    ('value_k', {'label': 'label_k', 'foo': 'bar', ...}),
                    ... ]
    The option k will be rendered as:
        <option value="value_k" foo="bar" ...>label_k</option>
    """

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else:
            opt_attrs = {}
        option_dict = super(SelectWOA, self).create_option(name, value,
            label, selected, index, subindex=subindex, attrs=attrs)
        for key,val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict


class ProvinceChoiceField(forms.ChoiceField):

    def validate(self, value):
        if value not in CHINA_PROVINCES:
            raise forms.ValidationError(
                    "We currently support users in China mainland only!"
                )


class CityChoiceField(forms.ChoiceField):

    def validate(self, value):
        pass


# This form inherits all-auth.
class PhoneSignupForm(SignupForm):

    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "username_password_mismatch": _(
            "Phone no./username or password is not correct."
        ),
    }

    username = forms.CharField(label=_("Username"),
                   min_length=getattr(settings,
                       'ACCOUNT_USERNAME_MIN_LENGTH', 3),
                   max_length=getattr(settings,
                       'ACCOUNT_USERNAME_MAX_LENGTH', 16),
                   widget=forms.TextInput(
                       attrs={'placeholder':
                              _('< 16 letters. No spaces'),
                              'autofocus': 'autofocus'}))
    province_region = ProvinceChoiceField(
        widget = SelectWidget(attrs={
                    'id': 'province',
                    'class': 'custom-select',
                    'name': 'province_region',
                    'autocomplete': 'on'
            })
        )
    city = CityChoiceField(
        widget = SelectWidget(attrs={
                    'id': 'city',
                    'class': 'custom-select',
                    'name': 'city',
                    'autocomplete': 'on'
            })
        )
    phone_number = PhoneNumberField(
        label=_('Phone number'),
        widget=forms.TextInput(
            attrs={
                'placeholder' : _('E.g 13291863081'),
                'autofocus': "autofocus",
                'maxlength': '11',
                'minlength':'11',
                'type':'tel',
                'pattern':'[0-9]{11}',
            }
        ),
        required=False,
    )

    unverified_phone = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    notes = forms.CharField(
        required=False
    )

    gender = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )

    verify_code = forms.IntegerField(
            widget=forms.TextInput(attrs={
                'id':'verify-code',
                'class':'col-10',
                'maxlength':'6',
                'minlength':'6',
                'type':'tel',
                'pattern':'[0-9]{6}',
                'name':'code'
                }),
            required=False
        )

    class Meta:
        model = User
        fields = (
            "username",
            "city",
            "province_region",
            "phone_number",
            "password1",
            "password2",
            "gender",
            "notes",
            "unverified_phone"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username_field = self.fields['username']
        username_field.max_length = getattr(settings,
            'ACCOUNT_USERNAME_MAX_LENGTH', 16)
        username_field.validators.append(
            validators.MaxLengthValidator(username_field.max_length))
        username_field.widget.attrs['maxlength'] = str(
            username_field.max_length)

        if getattr(settings, "SIGNUP_PASSWORD_ENTER_TWICE", False):
            self.fields["password2"] = PasswordField(
                    label=_("Password (again)")
                )
        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)


    def save(self, request, *args, **kwargs):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(PhoneSignupForm, self).save(request)

        user.province_region = self.cleaned_data["province_region"]
        user.city = self.cleaned_data["city"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save()

        # You must return the original result.
        return user


class SocialSignupCompleteForm(PhoneSignupForm):
    wechat_openid = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )

    wechat_id = forms.CharField(
            required=False
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password1')

    def save(self, request, *args, **kwargs):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)

        user.gender = self.cleaned_data["gender"]
        user.wechat_openid = self.cleaned_data["wechat_openid"]

        user.save()
        # You must return the original result.
        return user


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("username", "country", "city")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class UserForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False
    )
    job_title = forms.CharField(
            required=False, label=("Occupation"))

    province_region = ProvinceChoiceField(
        required=False,
        widget = SelectWidget(attrs={
                    'id': 'province',
                    'class': 'custom-select',
                    'name': 'province_region',
                    'autocomplete': 'on'
            })
        )
    city = CityChoiceField(
        required=False,
        widget = SelectWidget(attrs={
                    'id': 'city',
                    'class': 'custom-select',
                    'name': 'city',
                    'autocomplete': 'on'
            })
        )

    english_address = forms.CharField(required=False, label=("Address (English)"))
    chinese_address = forms.CharField(required=False, label=("Full address (Chinese)"))

    class Meta:
        model = User
        fields = (
                    "name", "job_title","bio",
                    "province_region", "city", "chinese_address", "english_address"
                )
        help_texts = {
            "bio": "A short introduction about yourself",
            "english_address": "Don't include your City and Province",
            "chinese_address": "Full address to be used for delivery services",
        }


class VerifyAddressForm(forms.ModelForm):
    province_region = ProvinceChoiceField(
        widget = SelectWidget(attrs={
                    'id': 'province',
                    'class': 'custom-select',
                    'name': 'province_region',
                    'autocomplete': 'on'
            })
        )
    city = CityChoiceField(
        widget = SelectWidget(attrs={
                    'id': 'city',
                    'class': 'custom-select',
                    'name': 'city',
                    'autocomplete': 'on'
            })
        )

    chinese_address = forms.CharField(required=False, label=("Full address (In Chinese)"))
    phone_number = forms.CharField(required=False, label=("Full address (In Chinese)"))

    class Meta:
        model = User
        fields = (
                    "province_region", "city", "chinese_address", "phone_number"
                )
        help_texts = {
            "chinese_address": "Full address in Chinese to be delivery services",
        }


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

        if getattr(settings, "SIGNUP_PASSWORD_ENTER_TWICE", False):
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


class CusSocialSignupForm(forms.Form):
    phone_number = forms.IntegerField(
        label=_("Phone number"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "tel", "placeholder": _("Don't include country code"),}
        ),
    )

    verify_code = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )

    email = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False
    )

    def save(self):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save()

        # Add your own processing here.
        user.phone_number = '+86' + str(self.cleaned_data["phone_number"])
        print( self.cleaned_data["phone_number"] )
        # You must return the original result.
        return user



class AdminCreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ "username", "english_address", "chinese_address",
            "city", "province_region","phone_number"]


class CustomSocialSignupForm(SocialSignupForm):
    phone_number = forms.IntegerField(
        label=_("Phone number"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "tel", "placeholder": _("Don't include country code"),}
        ),
    )

    verify_code = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )

    email = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False
    )

    def save(self):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save()

        # Add your own processing here.
        if self.cleaned_data["phone_number"].startsWith('+86'):
            user.phone_number = self.cleaned_data["phone_number"]
        else:
            user.phone_number = '+86' + self.cleaned_data['phone_number']
        # You must return the original result.
        return user


class CustomLoginForm(LoginForm):
    password = PasswordField(label=(""))

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
            attrs={"placeholder": (""), "autofocus": "autofocus", }
        )

        login_field = forms.CharField(
            label=_("Phone or username or email"), widget=login_widget
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
            attrs={"type": "tel", "placeholder": _("Don't include country code"),}
        ),
    )


class PhoneResetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    could add pattern attribute but it doesn't work on Chrome
    "pattern": "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$",
    """

    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        required=True,
        label=("New password"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Atleast 8 letters & numbers "),
                "type": "password",
                "minlength": 8,
                "maxlength": 30
            }
        )
    )
    new_password2 = forms.CharField(
        required=True,
        label=("Confirm password"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Same as above"),
                "type": "password",
                "minlength": 8,
                "maxlength": 30
            }
        )
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
