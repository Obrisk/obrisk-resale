from django import forms
from dal import autocomplete
from obrisk.classifieds.models import Classified, OfficialAd, ClassifiedOrder
from phonenumber_field.formfields import PhoneNumberField


class ClassifiedForm(forms.ModelForm):
    details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
        label=("details (Optional)")
    )
    price = forms.DecimalField(
            required=False
        )
    status = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )
    edited = forms.BooleanField(
            widget=forms.HiddenInput(),
            required=False, initial=False
        )
    #100 for each image.
    images = forms.CharField(
            widget=forms.HiddenInput(),
            max_length=1500, required=False
        )
    #Store images error for later debugging.
    img_error = forms.CharField(
            widget=forms.HiddenInput(),
            max_length=500, required=False
        )

    english_address = forms.CharField(
            required=False, label=("Address (English)")
        )

    phone_number = PhoneNumberField(required=False,
            label=("Phone number(optional)"),
            widget=forms.TextInput(
                attrs={
                    'placeholder': ('Don\'t enter country code')
                }
            )
        )

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited",
                 "price", "english_address", "phone_number"]


class AdminClassifiedForm(forms.ModelForm):
    details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
        label=("details (Optional)")
    )
    price = forms.DecimalField(
            required=False
        )
    status = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )
    edited = forms.BooleanField(
            widget=forms.HiddenInput(),
            required=False, initial=False
        )
    #100 for each image.
    images = forms.CharField(
            widget=forms.HiddenInput(),
            max_length=1500, required=False
        )
    #Store images error for later debugging.
    img_error = forms.CharField(
            widget=forms.HiddenInput(),
            max_length=500, required=False
        )

    english_address = forms.CharField(
            required=False, label=("Address (English)")
        )

    phone_number = PhoneNumberField(required=False,
            label=("Phone number(optional)"),
            widget=forms.TextInput(
                attrs={
                    'placeholder': ('Don\'t enter country code')
                }
            )
        )

    class Meta:
        model = Classified
        fields = ["user", "title", "details", "status", "edited","tags",
                 "price", "english_address", "phone_number"]



class ClassifiedOrderForm(forms.ModelForm):
    recipient_chinese_address = forms.CharField(
            required=False, label=("Address (in Chinese)")
        )
    recipient_phone_number = forms.CharField(
            required=False,
            label=("Phone number")
        )
    is_offline = forms.BooleanField(
            widget=forms.HiddenInput(),
            required=False, initial=False
        )

    class Meta:
        model = ClassifiedOrder
        fields = ["recipient_chinese_address", "recipient_phone_number", "is_offline"]


class ClassifiedEditForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
            widget=forms.HiddenInput(),
            required=False, initial=False
        )
    details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False
    )
    english_address = forms.CharField(
            required=False, label=("Address (English)")
        )

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price",
         "english_address"]

        widgets = {
            'user': forms.HiddenInput(),
            'tags': autocomplete.TaggitSelect2(
                'tags_autocomplete'
            )
        }

        help_texts = {
            "english_address": "Can be street name,district or other info.\
            Don't enter your city",
            "phone_number": "This field is optional.",
            "tags": "Category of your item, can be 1 or multiple separated by a comma.\
                        e.g electronics, ebike"
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
