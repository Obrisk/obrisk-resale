from django import forms
from django.contrib.postgres.forms import JSONField
from markdownx.fields import MarkdownxFormField
from obrisk.posts.models import Post, Comment
from obrisk.utils.fields import RichTextFormField


class PostForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image = forms.CharField(
            required=False, max_length=150,
            label=('Cover photo URL'))
    content = MarkdownxFormField()
    content_html = RichTextFormField(
            widget=forms.HiddenInput(), required=False)
    content_json = JSONField(
            widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "content_html",
                "content_json", "image", "tags",
                "status", "edited", "category"]
        help_texts = {
            "title": "Make it short but descriptive, maximum 80 characters.",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'cols': 'auto'}),
        }
        labels = {'body': '', }
