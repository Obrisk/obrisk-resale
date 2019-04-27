from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

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