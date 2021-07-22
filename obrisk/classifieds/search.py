from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

from elasticsearch_dsl.query import Q
from obrisk.utils.helpers import ajax_required
from obrisk.classifieds.models import Classified
from obrisk.classifieds.documents import ClassifiedDocument


@ajax_required
@require_http_methods(["GET"])
def classifieds_search(request):
    """view to render the search results"""

    query_str = request.GET.get("query")
    if len(query_str) < 2:
        return JsonResponse({
                'code': 601
            })

    qs = ClassifiedDocument.search().query(
            Q('match_phrase', title=query_str) |
            Q('match_phrase', details=query_str) |
            Q('match_phrase', tags=query_str)
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
    # Add all the retrieved classifieds to data_retrieved
    # list.
    data_retrieved = classifieds
    results = []
    return JsonResponse(results, safe=False)
