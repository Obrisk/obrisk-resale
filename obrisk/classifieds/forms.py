from django import forms

from markdownx.fields import MarkdownxFormField

from obrisk.classifieds.models import Classified


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)

    class Meta:
        model = Classified
        fields = ["title", "content", "image", "tags", "status", "edited", "price", "street_area", "district", "city"]

