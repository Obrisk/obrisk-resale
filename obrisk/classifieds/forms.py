from django import forms
from dal import autocomplete
from obrisk.classifieds.models import Classified, OfficialAd

class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    images = forms.CharField(widget=forms.HiddenInput(), max_length=1500, required=False) #100 for each image.
    img_error = forms.CharField(widget=forms.HiddenInput(), max_length=500, required=False) #Store images error for later debugging.


    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price" ]

        widgets = {
            'user': forms.HiddenInput(),
            #'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }

class ClassifiedEditForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    #images = forms.CharField(widget=forms.HiddenInput(), max_length=1500) #100 for each image.
    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price" ]

        widgets = {
            'user': forms.HiddenInput(),
            'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }


class OfficialAdForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)
    images = forms.CharField(max_length=6000, widget=forms.HiddenInput()) #This is not related with any model

    class Meta:
        model = OfficialAd
        fields = ["title", "details", "tags", "images"]
        widgets = {'user': forms.HiddenInput()}
           
# class ClassifiedReportForm(forms.ModelForm):
#     laws = 'lw'
#     abusive = 'ab'
#     Infringes = 'in'
#     others = 'ot'

#     reason_choices = (
#         (laws, "Violating the laws and regulations"),
#         (abusive, "Abusive content"),  
#         (Infringes, "Infringes my rights"),  
#         (others, "others"),  
#     )

#     reporter = forms.CharField(widget=forms.HiddenInput())
#     reason = forms.ChoiceField(choices= reason_choices)
#     details = forms.CharField (max_length=3000, required=False, )

#     class Meta:
#         model = Classified
#         fields = ["slug", "user"]