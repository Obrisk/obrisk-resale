from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from obrisk.helpers import ajax_required, AuthorRequiredMixin
from obrisk.stories.models import Stories


class StoriesListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""
    model = Stories
    paginate_by = 15

    def get_queryset(self, **kwargs):
        return Stories.objects.filter(reply=False)


class StoriesDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""
    model = Stories
    success_url = reverse_lazy("stories:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_stories(request):
    """A function view to implement the post functionality with AJAX allowing
    to create Stories instances as parent ones."""
    user = request.user
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0 and len(post) <= 280:
        posted = Stories.objects.create(
            user=user,
            content=post,
        )
        html = render_to_string(
            'stories/stories_single.html',
            {
                'stories': posted,
                'request': request
            })
        return HttpResponse(html)

    else:
        lenght = len(post) - 280
        return HttpResponseBadRequest(
            content=_(f'Text is {lenght} characters longer than accepted.'))


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """Function view to receive AJAX, returns the count of likes a given stories
    has recieved."""
    stories_id = request.POST['stories']
    stories = Stories.objects.get(pk=stories_id)
    user = request.user
    stories.switch_like(user)
    return JsonResponse({"likes": stories.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of stories with the given stories as parent."""
    stories_id = request.GET['stories']
    stories = Stories.objects.get(pk=stories_id)
    stories_html = render_to_string("stories/stories_single.html", {"stories": stories})
    thread_html = render_to_string(
        "stories/stories_thread.html", {"thread": stories.get_thread()})
    return JsonResponse({
        "uuid": stories_id,
        "stories": stories_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    Stories instances who happens to be the children and commenters of the root
    post."""
    user = request.user
    post = request.POST['reply']
    par = request.POST['parent']
    parent = Stories.objects.get(pk=par)
    post = post.strip()
    if post:
        parent.reply_this(user, post)
        return JsonResponse({'comments': parent.count_thread(), 'likes': parent.count_likers()})

    else:
        return HttpResponseBadRequest()

@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    stories = Stories.objects.get(pk=data_point)
    data = {'likes': stories.count_likers(), 'comments': stories.count_thread()}
    return JsonResponse(data)
