import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect
from obrisk.utils.helpers import AuthorRequiredMixin
from obrisk.posts.models import Post
from obrisk.posts.forms import PostForm, CommentForm
#For comments
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from obrisk.utils.images_upload import bucket, bucket_name
from slugify import slugify
import base64
import datetime

import oss2
from aliyunsdkcore import client

class PostsListView(ListView):
    """Basic ListView implementation to call the published Posts list."""
    model = Post
    paginate_by = 30
    context_object_name = "posts"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #This query could be slowing the posts
        #context['popular_tags'] = Post.objects.get_counted_tags()
        context['base_active'] = 'posts'

        return context

    def get_queryset(self, **kwargs):
        return Post.objects.get_active().select_related('user')


class DraftsListView(PostsListView):
    """Overriding the original implementation to call the drafts Posts
    list."""
    template_name = 'posts/draft_list.html'

    def get_queryset(self, **kwargs):
        return Post.objects.get_draft().filter(user=self.request.user)


class CreatePostView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new Posts."""
    model = Post
    message = _("Your Post has been created.")
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def form_valid(self, form):
        print(form.cleaned_data['status'])
        if self.request.user.is_official is False and form.cleaned_data['status'] is 'P':
            print ('mafan')

        image = form.cleaned_data['image']

        if (image is None or (image.startswith(
            f'media/images/posts/{self.request.user.username}') is False)):
            messages.error(self.request, "Sorry, the image was not uploaded. \
                Please add the image and submit the form!")
            return self.form_invalid(form)

        else:
            form.instance.user = self.request.user
            post = form.save(commit=False)
            post.user = self.request.user
            post.image = image

            d = str(datetime.datetime.now())
            thumb_name = "media/images/posts/" + str(post.user) + "/" + \
            slugify(str(post.title), to_lower=True) + "/thumbnails/" + d
            style = 'image/resize,m_fill,h_300,w_430'

            try:
                process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                        oss2.compat.to_string(base64.urlsafe_b64encode(
                            oss2.compat.to_bytes(thumb_name))),
                        oss2.compat.to_string(
                            base64.urlsafe_b64encode(
                                oss2.compat.to_bytes(bucket_name)
                            )
                        )
                    )
                bucket.process_object(post.image, process)

            except oss2.exceptions.ServerError as e:
                post.save()
                messages.error(self.request, _("Sorry, \
                    Your image was not uploaded. Please verify that, \
                    your internet is stable and edit the post to add images.")
                )
                logging.error(e)
                # return self.form_invalid(form)
                #Dont return form because this is likely our problem
                return redirect ('posts:list')

            else:
                post.img_small = thumb_name
                post.save()

            return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        if self.request.user.is_official:
            return reverse('posts:list')
        else:
            return self.object.get_absolute_url()


class EditPostView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing Posts."""
    model = Post
    message = _("Your Post has been updated.")
    form_class = PostForm
    template_name = 'posts/post_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('posts:list')



@method_decorator(login_required, name='post')
@method_decorator(ensure_csrf_cookie, name='get')
class DetailPostView(DetailView):
    """Basic DetailView implementation to call an individual Post."""
    model = Post

    def render_to_response(self, context, **response_kwargs):
        """ Allow AJAX requests to be handled more gracefully """
        if self.request.is_ajax():
            return JsonResponse(
                _('Your comment has been uploaded!'),
                safe=False,
                **response_kwargs
            )
        else:
            return super(DetailView,self).render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """

        comment_form = CommentForm(self.request.POST)
        self.object = self.get_object()

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = self.object
            new_comment.user = self.request.user
            # Save the comment to the database
            new_comment.save()

            context = context = super(DetailPostView, self).get_context_data(**kwargs)
            context['comment_form'] = CommentForm()
            context['comments'] = self.object.comments.all()
            context['new_comment'] = None
            return self.render_to_response(context=context)

        else:
            context = super(DetailPostView, self).get_context_data(**kwargs)
            #Return the form with errors.
            context['comment_form'] = comment_form
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailPostView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['new_comment'] = None
        return context
