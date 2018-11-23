from django import forms

from markdownx.fields import MarkdownxFormField

from obrisk.classifieds.models import Classified, ClassifiedImages


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)

    class Meta:
        model = Classified
        fields = ["title", "content", "tags", "status", "edited", "price", "located_area"]


class ClassifiedImageForm(forms.ModelForm):
    images = forms.ImageField(label='Image')

    class Meta:
        model = ClassifiedImages
        fields = ["images"]