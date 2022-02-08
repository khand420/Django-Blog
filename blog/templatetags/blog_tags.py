
# CUSTOM TEMPLATE TAGS
# 1. Simple_tag: Processes the data and return string
# 2. Inclusion_tag: Process the data and return a render template


from django import template
from ..models import Post, BlogComment
from django.db.models import Count
# for markdown
# from django.utils.safestring import mark_safe
# import markdown

register = template.Library()

# 1. Simple_tag:
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# 2. Inclusion_tag:
@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return{'latest_posts': latest_posts}


# for markdown the content side in db
# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))
