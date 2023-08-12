from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post


def home(request):
    return HttpResponse('<h1>hello world</h1>')


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
