from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from blog.models import Post, Comment
from markdown import markdown

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=5):
    l_posts = Post.published.order_by('-publish')[:count]
    return {'l_posts': l_posts}


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
