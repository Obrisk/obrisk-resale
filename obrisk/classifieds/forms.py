from django import forms
from obrisk.classifieds.models import Classified, ClassifiedImages
from .fields import MultiFileField

class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    images = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5) #This is not related with any model
    

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "located_area", "contact_info", "tags", "images"]
        widgets = {'user': forms.HiddenInput()}
        help_texts = {
            "located_area": "It can be a street name, address or other description.\
            Your city is added by default based on your location.",
            "contact_info": "Phone number, or wechat-ID or any other contacts info, if necessary."
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