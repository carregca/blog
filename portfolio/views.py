from django.shortcuts import render

from blog.models import Post


def home(request):
    """Portfolio principal + las últimas entradas del blog."""
    latest_posts = Post.objects.published()[:3]
    return render(request, "portfolio/index.html", {"latest_posts": latest_posts})
