from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.modelfields import PhoneNumberField

from obrisk.users.models import User 
from obrisk.users import models

from allauth.account.forms import SignupForm

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
        # widgets = {
        #     'picture': forms.ImageField(attrs={'class': 'btn, btn-dark'}),
        # }
    
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


class PhoneSignupForm(UserCreationForm): 

    class Meta:
        model = User
        widgets = {
            'province_region': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }
        help_texts = {
            'username': "At least 3 characters, no special characters",
        } 
        fields = ( 'username', 'city', 'province_region', 'phone_number', 'password1', 'password2')



    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = "At least 8 character, can't be too common or entirely numeric"



