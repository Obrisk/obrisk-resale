from django import forms
from markdownx.fields import MarkdownxFormField
from obrisk.posts.models import Post, Comment, Jobs, Events



JOB_CHOICES =(
    ('FULLTIME', 'full time'),
    ('PARTTIME', 'part time'),
    ('INTERNSHIP', 'internship'),
    ('OTHERS', 'others'),
)

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
    jobs_type = forms.ChoiceField(choices=JOB_CHOICES)

    class Meta:
        model = Jobs
        fields = (
            'title',
            'jobs_type',
            'description',
            'requirements',
            'start_date',
            'deadline',

        )


class EventsForm(forms.ModelForm):

    class Meta:
        model = Events
        fields = (
            'title',
            'host',
            'venue',
            #'events_image',
            'details',
            'start_time',
            'end_time',
            'contacts',
            'sponsors',


        )
