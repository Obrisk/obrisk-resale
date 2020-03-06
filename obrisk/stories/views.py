from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import json

from obrisk.utils.images_upload import multipleImagesPersist, videoPersist
from obrisk.utils.helpers import ajax_required, AuthorRequiredMixin
from obrisk.stories.models import Stories, StoryImages
from django.db.models import OuterRef, Subquery, Case, When, Value, IntegerField


class StoriesListView(ListView):
    """A really simple ListView, with some JS magic on the UI."""
    model = Stories
    paginate_by = 50
    def get_context_data(self, *args, **kwargs):
        context = super(StoriesListView, self).get_context_data(**kwargs)
        context["base_active"] = "stories"
        return context

    def get_queryset(self, **kwargs):
        return Stories.objects.filter(reply=False).annotate (
            img1 = Subquery (
                    StoryImages.objects.filter(
                        story=OuterRef('pk'),
                ).values_list(
                   'image_thumb', flat=True
                    )[:1]),
            img2 = Subquery (
                StoryImages.objects.filter(
                    story=OuterRef('pk'),
                ).values_list(
                   'image_thumb', flat=True
                )[1:2]),
            img3 = Subquery (
                StoryImages.objects.filter(
                    story=OuterRef('pk'),
                ).values_list(
                   'image_thumb', flat=True
                )[2:3]),
            img4 =  Subquery (
                StoryImages.objects.filter(
                    story=OuterRef('pk'),
                ).values_list(
                   'image_thumb', flat=True
                )[3:4])

        ).prefetch_related('liked', 'parent', 'user__thumbnail__username').order_by('-priority', '-timestamp')
        

@require_http_methods(["GET"])
def get_story_images(request):
    """A function view return all images of a specific story"""
    story_id = request.GET['story_id']

    try:
        images = list(StoryImages.objects.filter(
                            story=story_id,
                        ).extra( 
                            select={ 'src': 'image'}).values('src')
                        )
    except:
        return HttpResponseBadRequest(
                content=_('The story post is invalid'))
    return HttpResponse(json.dumps(images), content_type='application/json')



@require_http_methods(["GET"])
def get_story_likers(request):
    """A function view that returns all people that liked the story"""
    story_id = request.GET['story_id']

    try:
        story = Stories.objects.get(uuid_id=story_id)
    except:
        return HttpResponseBadRequest(
                content=_('The story post is invalid'))
    users = list(story.liked.all().values_list('username', flat=True))

    return HttpResponse(json.dumps(users), content_type='application/json')



@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of stories with the given stories as parent."""
    stories_id = request.GET['stories']
    try:
        stories = Stories.objects.get(pk=stories_id)
    except:
        return JsonResponse({"error":"Story post is not valid"})
    stories_html = render_to_string("stories/stories_single.html", {"stories": stories})
    thread_html = render_to_string(
        "stories/stories_thread.html", {"thread": stories.get_thread()})
    return JsonResponse({
        "uuid": stories_id,
        "stories": stories_html,
        "thread": thread_html,
    })


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
    post = request.POST.get('post')
    post = post.strip()
    images = request.POST.get('images')
    video = request.POST.get('story_video')
    viewers = request.POST.get('viewers')
    img_errors = request.POST.get('img_error')

    if len(post) <= 400 or images or video:

        if img_errors:
            #In the near future, send a message like sentry to our mailbox to notify about the error!
            send_mail('JS ERRORS ON IMAGE UPLOADING', str(img_errors) , 'errors@obrisk.com', ['admin@obrisk.com',])
        
        #Before saving the user inputs to the database, clean everything.
        story = Stories.objects.create(
            user=user,
            content=post,
            viewers=viewers
        )
        
        if images:            
            # split one long string of images into a list of string each for one JSON img_obj
            images_list = images.split(",")

            imgs_objs = multipleImagesPersist(request, images_list, 'stories', story)
            if imgs_objs[0]:
                story.img1 = imgs_objs[0].image_thumb
                story.img2 = story.img3 = story.img4 = None 
                #Find a way to return a list in a subquery
                try:
                    if imgs_objs[1]:
                        story.img2 = imgs_objs[1].image_thumb
                        if imgs_objs[2]:
                            story.img3 = imgs_objs[2].image_thumb
                            if imgs_objs[3]:
                                story.img4 = imgs_objs[3].image_thumb
                except IndexError:
                    pass 
            else:
                return HttpResponseBadRequest(
                    content=_('Sorry, the image(s) were not uploaded successfully!'))
        
        if video:
            if videoPersist(request, video, 'stories', story):
                story.video = video

        html = render_to_string(
            'stories/stories_single.html',
            {
                'stories': story,
                'request': request
            })
        
        return HttpResponse(html)

    else:
        return HttpResponseBadRequest(
                content=_('Text length is longer than accepted characters.'))

@csrf_exempt
@login_required
@ajax_required
@require_http_methods(["GET"])
#The only reason this method is GET is because the server will return 403 on the live site,
#even when ignoring the csrf with exempt decorator. Need to fix this method to become post.
def like(request):
    """Function view to receive AJAX, returns the count of likes a given stories
    has recieved."""
    stories_id = request.GET.get('stories')
    try:
        stories = Stories.objects.get(pk=stories_id)
    except:
        return JsonResponse({"error":"The story post is invalid!"}) 
    user = request.user
    stories.switch_like(user)

    #Without this you will get error
    #Object of type 'CombinedExpression' is not JSON serializable
    stories.refresh_from_db()
    return JsonResponse({"likes": stories.likes_count})



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
        #Without this you will get error
        #Object of type 'CombinedExpression' is not JSON serializable
        parent.refresh_from_db()
        return JsonResponse({'comments': parent.thread_count, 'likes': parent.likes_count})

    else:
        return HttpResponseBadRequest()

@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    story = Stories.objects.get(pk=data_point)
    data = {'likes': story.likes_count, 'comments': story.thread_count}
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def update_reactions_count(request):
    """ This view is temporal used to update stories to new reaction counts model setup"""
    for story in Stories.objects.all():
        try:
            story.thread_count = story.count_thread()
            story.likes_count = story.count_likers()
            story.save()
        except:
            return HttpResponse(f"can't update the story object, {story}. Check the admin for more info")


    return HttpResponse("Successfully updated likes")
