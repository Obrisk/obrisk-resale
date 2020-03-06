from django import forms
from markdownx.fields import MarkdownxFormField
from obrisk.posts.models import Post, Comment


class PostForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image = forms.CharField(required=False, max_length=150, label=('Cover photo URL'))
    content = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", #"tags"
                "status", "edited", "category"]
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
