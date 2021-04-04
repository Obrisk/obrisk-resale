from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from obrisk.utils.helpers import ajax_required
from obrisk.classifieds.models import Classified
from obrisk.classifieds.documents import ClassifiedDocument


#client = Elasticsearch()
#my_search = Search(using=client)


@require_http_methods(["GET"])
def classifieds_search(request):
    """view to render the search results"""

    query_str = request.GET.get("query")
    if len(query_str) < 2:
        return JsonResponse({
                'code': 601
            })

    qs = ClassifiedDocument.search().query(
            'match_phrase',
            details=query_str
        ).to_queryset().values(
            'title','price','city','slug', 'thumbnail'
        ).order_by('-timestamp')

    if qs.count() < 1:
        return JsonResponse({
                'code': 602
            })

    return JsonResponse({
            'code': 201,
            'classifieds': list(qs),
        },safe=False)


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
