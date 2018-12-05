from django import forms

from markdownx.fields import MarkdownxFormField

from obrisk.classifieds.models import Classified


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)

    class Meta:
        model = Classified
        fields = ["title", "details", "image", "tags", "status", "edited", "price", "street_area", "district", "city"]

class ClassifiedReportForm(forms.Form):
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
    classified_ad = forms.URLField(widget=forms.HiddenInput())
    reason = forms.ChoiceField(choices= reason_choices)
    details = forms.CharField (max_length=300, required=False, )
    