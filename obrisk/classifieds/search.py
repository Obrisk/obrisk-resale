from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

# Create a connection to ElasticSearch
connections.create_connection()

# ElasticSearch "model" mapping out what fields to index
class ClassifiedPostIndex(Document):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'blogpost-index'

# Bulk indexing function, run in shell
def bulk_indexing():
    ClassifiedPostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.ClassifiedPost.objects.all().iterator()))

# Simple search function
def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response



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
        context["classifieds_list"] = Classified.objects.none()
        #This query is very expensive it does 200 queries.
            #title__icontains=query) | Q(details__icontains=query) | Q(
                #tags__name__icontains=query) | Q(
                #title__trigram_similar=query) | Q(
                #details__trigram_similar=query)
                #).distinct()
       
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


