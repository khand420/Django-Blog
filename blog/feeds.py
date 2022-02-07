

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy #for generate url for the link attributes
# from django.urls.base import reverse
from .models import Post

class LatestPostFeed(Feed):
    title = "Code2hell"
    link = reverse_lazy('blog:blogHome')
    description = 'new Post of my Blog'

    def item(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title 

    def item_description(self, item):
        return truncatewords(item.content,30)
