from django import forms
from django.forms import BaseModelFormSet
from django.forms.models import inlineformset_factory
from django.conf import settings

from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
# Next two lines are only used for generating the upload preset sample name
import cloudinary

from obrisk.classifieds.models import Classified, ClassifiedImages


class ClassifiedForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)

    class Meta:
        model = Classified
        fields = ["title", "details", "status", "edited", "price", "located_area", "city", "tags"]
        widgets = {'user': forms.HiddenInput()}

#Below code is to handle multiple images in a classified.
#https://stackoverflow.com/questions/51510373/how-to-carry-out-uploading-multiple-files-in-django-with-createview

# class ImagesForm(forms.ModelForm):
#     image = CloudinaryJsFileField(attrs={'multiple': 1})

#     class Meta:
#         model = ClassifiedImages
#         fields = ["image"]


# class ImageDirectForm(ImagesForm):
#     image = CloudinaryJsFileField()

# class ImageUnsignedDirectForm(ImagesForm):
#     upload_preset_name = 
#     image = CloudinaryUnsignedJsFileField(upload_preset_name)

# ImagesCreateFormSet = inlineformset_factory(Classified, ClassifiedImages, fields =["image"], extra=3)

#### Declare FORMSET !!! ###
# class BaseImagesFormSet(BaseModelFormSet):

#     """By default, when you create a formset from a model, the formset
#     will use a queryset that includes all objects in the model"""

#     def __init__(self, *args, **kwargs):
#         if 'user' in kwargs.keys():
#             user = kwargs.pop('user')
#         else:
#             user = None
#         super().__init__(*args, **kwargs)
#         if user and isinstance(settings.AUTH_USER_MODEL):
#             self.queryset = ClassifiedImages.objects.filter(user=user)
#         else:
#             self.queryset = ClassifiedImages.objects.none()

# """I usually declare formset for create operations and formset for update operations separately"""          
# ImagesCreateFormSet = forms.modelformset_factory(ClassifiedImages, ImageDirectForm,
#                                                     fields=ImagesForm.Meta.fields, extra=3,
#                                                     formset=BaseModelFormSet)


# ImagesUpdateFormSet = forms.modelformset_factory(ClassifiedImages, ImagesForm, can_delete=True,
#                                               fields=PropertyImageForm.Meta.fields, extra=3,
#                                               formset=BaseImagesFormSet)


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