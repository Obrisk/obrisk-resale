from django import forms
from markdownx.fields import MarkdownxFormField
from obrisk.posts.models import Post, Comment, Jobs, Events


class PostForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image = forms.ImageField(required=False)
    content = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", "tags", "status", "edited"]
        help_texts = {
            "title": "Make it short but descriptive, the maximum is 80 characters.",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'cols': 'auto'}),
        }
        labels = {'body': '', }


class JobsForm(forms.ModelForm):
    user =  forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Jobs
        fields = ["title", "location", "details", "requirements", "deadline", "contacts"]
class EventsForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Events
        fields = ["title", "address", "starting_time", "description", "ending_time", "contacts"]

