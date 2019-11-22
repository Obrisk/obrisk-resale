from django import forms
from dal import autocomplete
from obrisk.classifieds.models import Classified, OfficialAd
from phonenumber_field.formfields import PhoneNumberField

class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput(), required=False)
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    show_phone = forms.BooleanField( widget=forms.HiddenInput(), initial=True)
    #100 for each image.
    images = forms.CharField(widget=forms.HiddenInput(), max_length=1500, required=False)
    #Store images error for later debugging.
    img_error = forms.CharField(widget=forms.HiddenInput(), max_length=500, required=False) 
    address = forms.CharField (
        required=False, 
        label=("Your address"), help_text='English address is preferred. You can permanently save it in your profile settings'
    )
    phone_number = PhoneNumberField(required=False, label=("Phone number(optional)"),
                                    widget=forms.TextInput(
                                        attrs={'placeholder': ('Don\'t enter country code')}
                                    )
                                )


    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "address", "phone_number", "show_phone"]

        widgets = {
            'user': forms.HiddenInput(),
            'details': forms.Textarea(attrs={'rows': 3})
            #'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }

        help_texts = {
            "title": "Short description of your product",
            "price": "Leave 0 if you're giving away for free. Input numbers only",
            "details": "Please provide detailed information, it easily convinces someone to buy.",
        }

class ClassifiedEditForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField( widget=forms.HiddenInput(), required=False, initial=False)
    details = forms.CharField(widget=forms.Textarea)
    wechat_id = forms.CharField(required=False, label=('WechatID'))
    phone_number = forms.CharField(required=False)
    #images = forms.CharField(widget=forms.HiddenInput(), max_length=1500) #100 for each image.
    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "tags",
         "address", "wechat_id", "phone_number" ]

        widgets = {
            'user': forms.HiddenInput(),
            'tags': autocomplete.TagSelect2(url='classifieds:tags_autocomplete')
        }

        help_texts = {
            "address": "It can be a street name, address or other description.\
            Please don't enter your city it will be added automatically based on your profile",
            "phone_number": "This field is optional.", 
            "wechat_id": "This field is optional.", 
            "tags": "Write the categories of your item, can be one or multiple separated by a comma.\
            e.g phone,electronics. Some categories will appear as you start to type."
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