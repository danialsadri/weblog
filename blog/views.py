from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return HttpResponse('<h1>hello world</h1>')


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
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
