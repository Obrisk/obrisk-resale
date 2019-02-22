from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from obrisk.helpers import AuthorRequiredMixin
from obrisk.posts.models import Post
from obrisk.posts.forms import PostForm


class PostsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published Posts list."""
    model = Post
    paginate_by = 15
    context_object_name = "posts"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['popular_tags'] = Post.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Post.objects.get_active()


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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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


class DetailPostView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual Post."""
    model = Post
