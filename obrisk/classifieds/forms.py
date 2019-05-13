from django import forms
from obrisk.classifieds.models import Classified, OfficialAd

class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    images = forms.CharField(widget=forms.HiddenInput(), max_length=1500) #100 for each image.
    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "located_area", "contact_info", "tags"]

        widgets = {'user': forms.HiddenInput()}
        help_texts = {
            "located_area": "It can be a street name, address or other description.\
            Please don't enter your city it will be added automatically based on your profile",
            "contact_info": "This field is optional. You can include your phone number, or wechat-ID or other contacts info."
        }

class OfficialAdForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea)
    images = forms.CharField(max_length=6000, widget=forms.HiddenInput()) #This is not related with any model

    class Meta:
        model = OfficialAd
        fields = ["title", "details", "located_area", "contact_info", "tags", "images"]
        widgets = {'user': forms.HiddenInput()}
        help_texts = {
            "located_area": "It can be a street name, address or other description.\
             Please don't enter your city, it will be added automatically based on your profile",
            "contact_info": "This field is optional. You can include your phone number, or wechat-ID or other contacts info."
        }
           
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