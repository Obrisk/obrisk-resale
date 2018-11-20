from django import forms

from markdownx.fields import MarkdownxFormField

from obrisk.qa.models import Answer, Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]
