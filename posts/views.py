from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .models import BlogPostFrom


def get_posts(request):
    """
    Create a view that will retun a list of posts
    that were published prior to 'now' and render them to the
    'Blogposts.html' template
    """

    posts = Post.objects.filter(published_date__lte=timezone.now
                                ()).ordered_by('published_date')
    return render(request, "blogposts.html", {'posts': posts})


def post_detail(request, pk):
    """
    Create a view that returns a single Post Object
    based on the post ID (pk) and render it to the
    'postdetail.html' template. Or return a
    """
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post': post})


def create_or_edit_post(request, pk=None):
    """
    Create a view that allows us to create
    or edit a post depending if the Post Id
    is null or not
    """
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostFrom(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostFrom(instance=post)
    return render(request, 'blogpostform.html', {'form': form})
