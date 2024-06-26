from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import *
from blog.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import *


def index(request):
    return render(request, 'blog/index.html')


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
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
        'category': category,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'], phone=cd['phone'],
                                  subject=cd['subject'])
            return redirect('blog:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'comment': comment, 'form': form}
    return render(request, 'forms/comment.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(post=post, image_file=form.cleaned_data['image1'])
            Image.objects.create(post=post, image_file=form.cleaned_data['image2'])
            return redirect('blog:profile')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'forms/post.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results1 = Post.published.filter(title__icontains=query)
#             results2 = Post.published.filter(description__icontains=query)
#             results = results1 | results2
#     context = {'query': query, 'results': results}
#     return render(request, 'blog/search.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.filter(Q(title__icontains=query) | Q(description__icontains=query))
#     context = {'query': query, 'results': results}
#     return render(request, 'blog/search.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.filter(Q(title__search=query) | Q(description__search=query))
#     context = {'query': query, 'results': results}
#     return render(request, 'blog/search.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.annotate(search=SearchVector('title', 'description','slug')).filter(search=query)
#     context = {'query': query, 'results': results}
#     return render(request, 'blog/search.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_query = SearchQuery(query)
#             search_vector = SearchVector('title', 'description', 'slug')
#             # search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('slug', 'C')
#             search_rank = SearchRank(search_vector, search_query)
#             results = Post.published.annotate(search=search_vector, rank=search_rank).filter(search=search_query).order_by('-rank')
#             # results = Post.published.annotate(search=search_vector, rank=search_rank).filter(rank__gte=0.3).order_by('-rank')
#     context = {'query': query, 'results': results}
#     return render(request, 'blog/search.html', context)

def post_search(request):
    query = None
    post_results = []
    image_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            trigram_similarity1 = TrigramSimilarity('title', query)
            trigram_similarity2 = TrigramSimilarity('description', query)
            trigram_similarity3 = TrigramSimilarity('title', query)
            trigram_similarity4 = TrigramSimilarity('description', query)
            post_results1 = Post.published.annotate(similarity=trigram_similarity1).filter(similarity__gt=0.1)
            post_results2 = Post.published.annotate(similarity=trigram_similarity2).filter(similarity__gt=0.1)
            image_results1 = Image.objects.annotate(similarity=trigram_similarity3).filter(similarity__gt=0.1)
            image_results2 = Image.objects.annotate(similarity=trigram_similarity4).filter(similarity__gt=0.1)
            post_results = list(post_results1) + list(post_results2)
            image_results = list(image_results1) + list(image_results2)
            post_results.sort(key=lambda x: x.similarity, reverse=True)
            image_results.sort(key=lambda x: x.similarity, reverse=True)

    context = {'query': query, 'post_results': post_results, 'image_results': image_results}
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    context = {'posts': posts, 'user': user}
    return render(request, 'blog/profile.html', context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    return render(request, 'forms/post_delete.html', {'post': post})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'forms/post.html', context)


@login_required
def image_delete(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('your account is disabled')
#             else:
#                 return HttpResponse('you are not logged in')
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect(request.META.get('HTTP_REFERER'))


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('blog:password_change_done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('blog:password_reset_done')
    email_template_name = 'registration/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('blog:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        account_form = AccountEditForm(data=request.POST, files=request.FILES, instance=request.user.account)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
            return redirect('blog:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {'user_form': user_form, 'account_form': account_form}
    return render(request, 'registration/edit_account.html', context)
