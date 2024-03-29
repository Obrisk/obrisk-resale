import json
import uuid
import itertools
import logging
from slugify import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
        HttpResponse, JsonResponse,
        HttpResponseBadRequest)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DeleteView, DetailView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import (
        OuterRef, Subquery, Case,
        When, Value, IntegerField, Count)
from django.core.paginator import (
        Paginator, EmptyPage,
        PageNotAnInteger)

from dal import autocomplete
from obrisk.utils.images_upload import (
        multipleImagesPersist, videoPersist)
from obrisk.utils.helpers import ajax_required, AuthorRequiredMixin
from obrisk.stories.models import Stories, StoryImages, StoryTags


@ensure_csrf_cookie
@require_http_methods(["GET"])
def stories_list(request, slug=None):
    # Try to Get the popular tags from cache
    # This will be there when I've started to add tags on stories
    # popular_tags = cache.get('stories_popular_tags')
    popular_tags = None

    # if popular_tags == None:
    #    popular_tags = Stories.objects.get_counted_tags()

    # Get stories
    stories_list = Stories.objects.filter(reply=False).annotate(
            img1 = Subquery (
                    StoryImages.objects.filter(
                        story=OuterRef('pk'),
                ).values_list(
                       'image', flat=True
                    )[:1])
        ).prefetch_related(
            'liked', 'parent',
            'user__thumbnail__username').order_by(
                    '-priority', '-timestamp')

    # Deal with tags in the end to override other_stories.
    tag = None

    if str(request.META.get(
                'PATH_INFO')).startswith('/stories/i/'):
        stories_list = stories_list.annotate(
                order = Case (
                    When(slug=slug, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            ).order_by('order', '-priority', '-timestamp')

    elif slug:
        tag = get_object_or_404(StoryTags, slug=slug)

        stories_list = Stories.objects.get_stories().filter(
                tags__in=[tag]).annotate (
                    img1 = Subquery (
                            StoryImages.objects.filter(
                                story=OuterRef('pk'),
                        ).values_list(
                           'image', flat=True
                            )[:1])
                ).prefetch_related(
                        'liked', 'parent', 'user__thumbnail__username'
                    )

    paginator = Paginator(stories_list, 5)  #5 stories/page
    page = request.GET.get('page')

    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        stories = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        stories = paginator.page(paginator.num_pages)

    if request.is_ajax():
       return render(request,'stories/stories_list_ajax.html',
                    {'page': page, 'popular_tags': popular_tags,
                    'stories': stories, 'base_active': 'stories'})

    return render(request, 'stories/stories_list.html',
                {'page': page, 'popular_tags': popular_tags,
                'stories': stories, 'tag': tag, 'base_active': 'stories'})


class DetailStoryView(DetailView):
    """This view is never called it is here for reference"""
    model = Stories
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailStoryView, self).get_context_data(**kwargs)

        story_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_stories = Stories.objects.get_stories().filter(tags__in=story_tags_ids)\
            .exclude(uuid_id=self.object.uuid_id).annotate (
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
                    )[3:4])).prefetch_related(
                            'liked', 'parent',
                            'user__thumbnail__username')

        context['similar_stories'] = similar_stories.annotate(
                same_tags=Count('tags'))\
            .order_by('-same_tags', '-timestamp')[:10]

        if context['similar_stories'].count() < 6:
            latest_stories = Stories.objects.filter(reply=False).annotate(
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
                    ).prefetch_related('liked', 'parent',
                            'user__thumbnail__username').order_by(
                                '-priority', '-timestamp')[:6]

            context['similar_stories'].union(latest_stories)
        return context


def stories_create_slugs(request):
    for self in Stories.objects.all():
        if not self.slug:
            self.slug = first_slug = slugify(
                    f"{self.user.username}-{uuid.uuid4().hex[:6]}",
                    to_lower=True, max_length=300)

            for x in itertools.count(1):
                if not Stories.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)
            self.save()

    return redirect('stories:list')


@ajax_required
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

    stories_html = render_to_string(
            "stories/stories_single.html", {"stories": stories})
    thread_html = render_to_string(
        "stories/stories_thread.html", {"thread": stories.get_thread()})
    return JsonResponse({
        "uuid": stories_id,
        "stories": stories_html,
        "thread": thread_html,
    })


class StoriesDeleteView(LoginRequiredMixin,
        AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView overriding the
    delete method to allow a no-redirect response to
    use with AJAX call."""
    model = Stories
    success_url = reverse_lazy("stories:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_stories(request):
    """A function view to implement the post functionality
    with AJAX allowing to create Stories instances
    as parent ones."""
    user = request.user
    post = request.POST.get('post')
    post = post.strip()

    images = request.POST.get('images')
    video = request.POST.get('story_video')
    viewers = request.POST.get('viewers')
    img_errors = request.POST.get('img_error')

    if len(post) <= 400 or images or video:

        if img_errors:
            logging.error(f"Stories Images error: {img_errors}")
        # Before saving the user inputs to the database, clean everything.
        story = Stories.objects.create(
            user=user,
            content=post,
            viewers=viewers
        )

        # Adding stories tags by hash tags
        list_of_tags = [tgs for tgs in post.split() if tgs.lower().startswith('#')]
        for tag in list_of_tags:
            story.tags.add(str(tag.strip('#')))

        if images:
            # split one long string of images 
            #into a list of string each for one JSON img_obj
            images_list = images.split(",")

            display_img = multipleImagesPersist(request, images_list, 'stories', story)
            if display_img:
                story.img1 = display_img
            else:
                return HttpResponse(_(
                    'Sorry, the image(s) were not uploaded successfully!'
                    )
                )

        if video:
            vid_img = videoPersist(request, video, 'stories', story)
            if vid_img:
                story.video = video
                story.img1 = vid_img

            else:
                return HttpResponse(_(
                    'Sorry, the image(s) were not uploaded successfully!'
                    )
                )

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


class StoryTagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = StoryTags.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

            return qs


@login_required
@ajax_required
@require_http_methods(["GET"])
def like(request):
    """Function view to receive AJAX, returns the count of likes
    a given stories has recieved."""
    stories_id = request.GET.get('stories')
    try:
        stories = Stories.objects.get(pk=stories_id)
    except:
        return JsonResponse({"error":"The story post is invalid!"})
    user = request.user
    stories.switch_like(user)

     # Without this you will get error
     # Object of type 'CombinedExpression' is not JSON serializable
    stories.refresh_from_db()
    return JsonResponse({"likes": stories.likes_count})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality
    with AJAX, creating Stories instances who happens to be
    the children and commenters of the root post."""
    user = request.user
    post = request.POST['reply']
    par = request.POST['parent']
    parent = Stories.objects.get(pk=par)
    post = post.strip()
    if post:
        parent.reply_this(user, post)
        # Without this you will get error
        # Object of type 'CombinedExpression' is not JSON serializable
        parent.refresh_from_db()
        return JsonResponse({
            'comments': parent.thread_count,
            'likes': parent.likes_count
            })

    else:
        return HttpResponseBadRequest()


@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    story = Stories.objects.get(pk=data_point)
    data = {
            'likes': story.likes_count,
            'comments': story.thread_count
        }
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def update_reactions_count(request):
    """ This view is temporal used to update stories
    to new reaction counts model setup"""
    for story in Stories.objects.all():
        try:
            story.thread_count = story.count_thread()
            story.likes_count = story.count_likers()
            story.save()
        except:
            return HttpResponse(
                    f"can't update {story}, Check the admin for more info")


    return HttpResponse("Successfully updated likes")


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


def update_images_count(request):
    stories = Stories.objects.all()

    for st in stories:
        imgs = StoryImages.objects.filter(story=st)
        if st.video is None or st.video == "":
            st.images_count = len(imgs)
            st.save()

    return redirect('stories:list')
