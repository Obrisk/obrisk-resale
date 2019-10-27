from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from taggit.models import Tag
from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.utils.helpers import ajax_required


class SearchListView(LoginRequiredMixin, ListView):
    """CBV to contain all the search results"""
    model = Classified
    template_name = "classifieds/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = 'classified'
        context["tags_list"] = Tag.objects.filter(name=query).distinct()
        context["classifieds_list"] = Classified.objects.filter(Q(
            title__icontains=query) | Q(details__icontains=query) | Q(
                tags__name__icontains=query)).distinct()
        context["images"]  = ClassifiedImages.objects.all()
        context["classifieds_count"] = context["classifieds_list"].count()
        context["tags_count"] = context["tags_list"].count()

        return context




# For autocomplete suggestions
@login_required
@ajax_required
def get_suggestions(request):
    # Convert classifieds objects into list to be
    # represented as a single list.
    query = request.GET.get('term', '')
    classifieds = list(Classified.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(
            tags__name__icontains=query)))
    # Add all the retrieved classifieds to data_retrieved
    # list.
    data_retrieved = classifieds
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, Classified):
            data_json['id'] = data.id
            data_json['label'] = data.title
            data_json['value'] = data.title
        results.append(data_json)
    return JsonResponse(results, safe=False)


