from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from obrisk.users.models import User 
from obrisk.users import models

from obrisk.users.models import PROVINCE_CHOICES, CITY_CHOICES
from allauth.account.forms import SignupForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'country', 'city')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields

class UserForm(forms.ModelForm):
    bio = forms.CharField (widget=forms.Textarea(attrs={'rows': 3}), required=False) 
    
    class Meta:
        model = User
        fields = ('picture', 'name', 'job_title', 'city', 'bio', 'instagram_account',
               'linkedin_account', 'facebook_account' )
        help_texts = {
            "instagram_account": "Please copy the link of your profile on the browser.\
            Don't fill in your username.",
            "linkedin_account": "Please copy the link of your profile on the browser.\
            Don't fill in your username.",
            "facebook_account": "Please copy the link of your profile on the browser.\
            Don't fill in your username.",

        }
        # widgets = {
        #     'picture': forms.ImageField(attrs={'class': 'btn, btn-dark'}),
        # }
    
class CustomSignupForm(SignupForm): 
    province_region = forms.ChoiceField (widget=forms.HiddenInput(), choices=PROVINCE_CHOICES)
    city = forms.ChoiceField (widget=forms.HiddenInput(), choices=CITY_CHOICES)

    class Meta:
        model = User

def signup(self, request, user): 
    user.province_region = self.cleaned_data['province_region']
    user.city = self.cleaned_data['city']
    user.save() 
    return user 




