from django import forms
from django.forms import BaseModelFormSet
from django.forms.models import inlineformset_factory
from django.conf import settings

from cloudinary.forms import CloudinaryJsFileField
# Next two lines are only used for generating the upload preset sample name
from cloudinary.compat import to_bytes
import cloudinary, hashlib

from obrisk.classifieds.models import Classified, ClassifiedImages


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    images = forms.CharField(widget=forms.HiddenInput(), max_length=4000)
    imgSize = forms.IntegerField(widget=forms.HiddenInput(), max_value=6)

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "located_area", "city", "tags", "images", "imgSize"]
        widgets = {'user': forms.HiddenInput()}

            

class ClassifiedReportForm(forms.ModelForm):
    laws = 'lw'
    abusive = 'ab'
    Infringes = 'in'
    others = 'ot'

    reason_choices = (
        (laws, "Violating the laws and regulations"),
        (abusive, "Abusive content"),  
        (Infringes, "Infringes my rights"),  
        (others, "others"),  
    )

    reporter = forms.CharField(widget=forms.HiddenInput())
    user = forms.CharField(widget=forms.HiddenInput())
    slug = forms.SlugField(widget=forms.HiddenInput())
    reason = forms.ChoiceField(choices= reason_choices)
    details = forms.CharField (max_length=300, required=False, )

    class Meta:
        model = Classified
        fields = ["slug", "user"]