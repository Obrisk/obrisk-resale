from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
#from django.forms import formset_factory
from django.forms import modelform_factory
from django.template import RequestContext

from obrisk.helpers import AuthorRequiredMixin
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.classifieds.forms import ClassifiedForm, ClassifiedImageForm


class ClassifiedsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published classifieds list."""
    model = Classified
    paginate_by = 15
    context_object_name = "classifieds"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['popular_tags'] = Classified.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Classified.objects.get_published()


class DraftsListView(ClassifiedsListView):
    """Overriding the original implementation to call the drafts classifieds
    list."""
    def get_queryset(self, **kwargs):
        return Classified.objects.get_drafts()


class CreateClassifiedView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new classifieds."""
    model = Classified
    message = _("Your classified has been created.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_create.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class EditClassifiedView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing classifieds."""
    model = Classified
    message = _("Your classified has been updated.")
    form_class = ClassifiedForm
    template_name = 'classifieds/classified_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('classifieds:list')


class DetailClassifiedView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual classified."""
    model = Classified

# Below handling multiple images see below for help
#https://docs.djangoproject.com/en/2.1/topics/forms/formsets/
#https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django

@login_required
def post(request):

        ImageFormSet = modelformset_factory(ClassifiedImages,
                                            form=ClassifiedImageForm, extra=5)

        if request.method == 'POST':

            classifiedForm = ClassifiedForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES,
                                queryset=ClassifiedImages.objects.none())


            if classifiedForm.is_valid() and formset.is_valid():
                classified_form = classifiedForm.save(commit=False)
                classified_form.user = request.user
                classified_form.save()

                for form in formset.cleaned_data:
                    image = form['image']
                    photo = ClassifiedImages(classified=classified_form, images=image)
                    photo.save()
                messages.success(request,
                                "You have successfully created your classified!")
                #Take back to the list.
                return reverse('classifieds:list')
            else:
                print classifiedForm.errors, formset.errors
        else:
            classifiedForm = ClassifiedForm()
            formset = ImageFormSet(queryset=ClassifiedImages.objects.none())
        return render(request, 'classified_list.html',
                    {'classifiedForm': classifiedForm, 'formset': formset},
                    context_instance=RequestContext(request))

   
