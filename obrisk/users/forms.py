from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from obrisk.users.models import User 
from obrisk.users import models

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
    province_region = forms.CharField (widget=forms.HiddenInput(), required=False)
    city = forms.CharField (widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = User
        fields = ('picture', 'name', 'job_title', 'province_region', 'city', 'bio', 'instagram_account',
               'linkedin_account','snapchat_account', 'facebook_account' )
        help_texts = {
            "instagram_account": "Please fill in your username as it appears on your profile page.\
                 Make sure it is spelled correctly",
            "linkedin_account": "Please fill in your username as it appears on your profile page.\
                 Make sure it is spelled correctly",
            "facebook_account": "Please fill in your username as it appears on your profile page.\
                 Make sure it is spelled correctly",
            "snapchat_account": "Please fill in your username as it appears on your profile page.\
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




