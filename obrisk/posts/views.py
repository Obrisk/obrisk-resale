from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect
from obrisk.utils.helpers import AuthorRequiredMixin
from obrisk.posts.models import Post, Comment
from obrisk.posts.forms import PostForm, CommentForm
#For comments
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from obrisk.utils.images_upload import bucket, bucket_name
from slugify import slugify

import os
import base64
import datetime


import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

class PostsListView(ListView):
    """Basic ListView implementation to call the published Posts list."""
    model = Post
    paginate_by = 10
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
    def get_queryset(self, **kwargs):
        return Post.objects.get_draft()

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
        image = form.cleaned_data['image']

        if (image == None):
            messages.error(self.request, "Sorry, the image were not uploaded successfully. \
                Please add the image again and submit the form!")
            return self.form_invalid(form)
        
        else:
            form.instance.user = self.request.user
            post = form.save(commit=False)
            post.user = self.request.user
            post.image = post.image.replace('https://obrisk.oss-cn-hangzhou.aliyuncs.com/', '')

            d = str(datetime.datetime.now())
            thumb_name = "posts/" + str(post.user) + "/" + \
            slugify(str(post.title), allow_unicode=True, to_lower=True) + "/thumbnails/" + d 
            style = 'image/resize,m_fill,h_300,w_430'
            
            try:
                process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(
                                                                oss2.compat.to_bytes(thumb_name))),
                                                            oss2.compat.to_string(base64.urlsafe_b64encode(oss2.compat.to_bytes(bucket_name))))
                bucket.process_object(post.image, process)

            except oss2.exceptions.ServerError as e:
                post.save()
                messages.error(self.request, "Oops we are very sorry. \
                Your image was not uploaded successfully. Please ensure that, \
                your internet connection is stable and edit your item to add images. "
                            + 'status={0}, request_id={1}'.format(e.status, e.request_id))
                # return self.form_invalid(form)
                #I am not returning form errors because this is our problem and not user's
                return redirect ('posts:list')
            
            except:
                post.save()
                messages.error(self.request, "Oops we are sorry! Your image \
                    was not uploaded successfully. Please select your item, then edit, \
                    and try again to upload the images.")
                #return self.form_invalid(form)
                #I am not returning form errors because this is our problem and not user's
                return redirect ('posts:list')
        
            else:
                post.img_small = thumb_name
                post.save()

            #When the for-loop has ended return the results.        
            return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('posts:list')


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
class DetailPostView(DetailView):
    """Basic DetailView implementation to call an individual Post."""
    model = Post

    def render_to_response(self, context, **response_kwargs):
        """ Allow AJAX requests to be handled more gracefully """
        if self.request.is_ajax():
            return JsonResponse('Your comment has been uploaded!',safe=False, **response_kwargs)
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
    

