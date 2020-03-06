from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

from taggit.models import Tag

from obrisk.classifieds.models import Classified, ClassifiedImages
from obrisk.stories.models import Stories
from obrisk.utils.helpers import ajax_required
from obrisk.qa.models import Question


class SearchListView(LoginRequiredMixin, ListView):
    """CBV to contain all the search results"""
    model = Stories
    template_name = "search/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = 'stories'
        context["hide_search"] = True
        context["tags_list"] = Tag.objects.filter(name=query).distinct()
        context["stories_list"] = Stories.objects.filter(
            content__icontains=query).distinct()
        context["classifieds_list"] = Classified.objects.filter(Q(
            title__icontains=query) | Q(details__icontains=query) | Q(
                tags__name__icontains=query)).distinct()
        context["questions_list"] = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(
                tags__name__icontains=query)).distinct()
        # context["users_list"] = get_user_model().objects.filter(
        #     Q(username__icontains=query) | Q(
        #         name__icontains=query)).distinct()
            
        context["images"]  = ClassifiedImages.objects.all()

        context["stories_count"] = context["stories_list"].count()
        context["classifieds_count"] = context["classifieds_list"].count()
        context["questions_count"] = context["questions_list"].count()
        # context["users_count"] = context["users_list"].count()
        context["tags_count"] = context["tags_list"].count()
        context["total_results"] = context["stories_count"] + \
        context["classifieds_count"] + context["questions_count"] + \
        context["tags_count"]

        return context


# For autocomplete suggestions
@login_required
@ajax_required
def get_suggestions(request):
    # Convert users, classifieds, questions objects into list to be
    # represented as a single list.
    query = request.GET.get('term', '')
    users = list(get_user_model().objects.filter(
        Q(username__icontains=query) | Q(name__icontains=query)))
    classifieds = list(Classified.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(
            tags__name__icontains=query)))
    questions = list(Question.objects.filter(Q(title__icontains=query) | Q(
        content__icontains=query) | Q(tags__name__icontains=query)))
    # Add all the retrieved users, classifieds, questions to data_retrieved
    # list.
    data_retrieved = users
    data_retrieved.extend(classifieds)
    data_retrieved.extend(questions)
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, get_user_model()):
            data_json['id'] = data.id
            data_json['label'] = data.username
            data_json['value'] = data.username

        if isinstance(data, Classified):
            data_json['id'] = data.id
            data_json['label'] = data.title
            data_json['value'] = data.title

        if isinstance(data, Question):
            data_json['id'] = data.id
            data_json['label'] = data.title
            data_json['value'] = data.title

        results.append(data_json)

    return JsonResponse(results, safe=False)



@require_http_methods(["GET"])
def all_search(request, **kwargs):
    ''' 
    s means (search in) stories
    p means (search in) posts
    q means (search in) qa
    u means (search in) users
    c means (search in) classifieds
    '''
    
    connections.create_connection()
    query = request.GET.get('query')
    stories_results = StoriesDocument.search().filter("term", content=query)

    if request.GET.get('c') is 1:
        classifieds_results = ClassifiedDocument.search().filter("term",
                                                                title=query,
                                                                details=query)
                                                               
        return render(request, 'classifieds/search_results.html', 
                {'classifieds_results': classifieds_results,
                 'stories_results': stories_results})

    elif request.GET.get('u') is 1:
        users_results = UsersDocument.search().filter("term", username = query)
        return render(request, 'connections/search_results.html', 
                {'users_results': users_results,
                 'stories_results': stories_results})

    elif request.GET.get('q') is 1:
        qa_results = QaDocument.search().filter("term",
                                                title=query,
                                                details=query)

        return render(request, 'qa/search_results.html', 
                {'qa_results': qa_results,
                 'stories_results': stories_results})
                
    elif request.GET.get('p') is 1:
        posts_results = PostDocument.search().filter("term",
                                                     title=query,
                                                     content=query
                                                    )
        return render(request, 'posts/search_results.html', 
                {'posts_results': posts_results,
                 'stories_results': stories_results})

    else:
        return render(request, 'search/search_results.html', 
                {'stories_results': stories_results })

    return render(request, 'search/search_results.html', 
                {'stories_results': stories_results })


