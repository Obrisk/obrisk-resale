from django import forms
from django.contrib.postgres.forms import JSONField
from obrisk.posts.models import Post, Comment
from obrisk.utils.fields import RichTextFormField
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete

class PostForm(forms.ModelForm):
    status = forms.CharField(
            widget=forms.HiddenInput(), required=False
    )
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    image = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.HiddenInput(),
    )
    content_html = RichTextFormField(
        widget=forms.HiddenInput(), required=False
    )
    content_json = JSONField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            "title",
            "content_html",
            "content_json",
            "image",
            "tags",
            "status",
            "edited",
            "category",
        ]
        widgets = {
            'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }

        help_texts = {
            "title": _("Make it short but descriptive, maximum 80 characters."),
        }


class PostEditForm(forms.ModelForm):
    status = forms.CharField(
            widget=forms.HiddenInput(), required=False
    )
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    image = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.HiddenInput(),
    )
    content_html = RichTextFormField(
        widget=forms.HiddenInput(), required=False
    )
    content_json = JSONField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = [
            "title",
            "content_html",
            "content_json",
            "image",
            "tags",
            "status",
            "edited",
            "category",
        ]
        widgets = {
            'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }

        help_texts = {
            "title": _("Make it short but descriptive, maximum 80 characters."),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "cols": "auto"}),
        }
        labels = {
            "body": "",
        }
