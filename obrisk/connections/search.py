   
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from taggit.models import Tag
from obrisk.users.models import User
from obrisk.utils.helpers import ajax_required


class SearchListView(LoginRequiredMixin, ListView):
    """CBV to contain all the search results"""
    model = User
    template_name = "connections/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context['query'] = query
        context["users_list"] = User.objects.filter(username__icontains=query).distinct()
        context["users_count"] = context["users_list"].count()
        return context



# For autocomplete suggestions
@login_required
@ajax_required
def get_suggestions(request):
    # Convert classifieds objects into list to be
    # represented as a single list.
    query = request.GET.get('term', '')
    users = list(User.objects.filter(title__icontains=query))


    # Add all the retrieved classifieds to data_retrieved
    # list.
    data_retrieved = users
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, User):
            data_json['id'] = data.id
            data_json['label'] = data.username
            data_json['value'] = data.city
        results.append(data_json)
    return JsonResponse(results, safe=False)


