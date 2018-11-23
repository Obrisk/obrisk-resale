from django import forms
from markdownx.fields import MarkdownxFormField
from obrisk.posts.models import Post


class PostForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    content = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", "tags", "status", "edited"]