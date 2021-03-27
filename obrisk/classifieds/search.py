from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from obrisk.utils.helpers import ajax_required
from obrisk.classifieds.models import Classified

class SearchListView(ListView):
    """CBV to contain all the search results"""
    model = Classified
    template_name = "classifieds/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = 'classified'
        context["classifieds_list"] = Classified.objects.all()
        return context


# For autocomplete suggestions
@ajax_required
def get_suggestions(request):
    # Convert classifieds objects into list to be
    # represented as a single list.
    query = request.GET.get('term', '')
    classifieds = list(Classified.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(
            tags__name__icontains=query) | Q(
                title__trigram_similar=query) | Q(
                details__trigram_similar=query) | Q(
                tags__trigram_similar=query)))

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


