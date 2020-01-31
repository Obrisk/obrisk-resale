from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from obrisk.posts.models import Post
from taggit.models import Tag


class SearchListView(LoginRequiredMixin, ListView):
    """CBV to contain all the search results"""
    model = Post 
    template_name = "posts/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = 'posts'
        context["tags_list"] = Tag.objects.filter(name=query).distinct()
        context["posts_list"] = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).distinct()
 
        context["posts_count"] = context["posts_list"].count()
        context["tags_count"] = context["tags_list"].count()
        context["total_results"] = context["posts_count"] + context["tags_count"]

        return context

