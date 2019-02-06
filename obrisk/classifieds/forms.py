from django import forms

from obrisk.classifieds.models import Classified, ClassifiedImages


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    images = forms.CharField(max_length=6000, widget=forms.HiddenInput())

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "located_area", "city", "tags", "images"]
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