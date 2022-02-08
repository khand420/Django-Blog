
# SITEMAP
# 1.A sitemap is an XML file that tells search engines the pages of our website, their relevance, and how frequently they are updated.
# 2. Using this we can make our website more visible on in search egines ranking.
# 3. it help crawler to index our website's content
# 4. Django Sitemap framework depends on django.contrib.sites

from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9  #max -> 1

    def items(self):
        return Post.published.all()

    def lastmod(self,obj):
        return obj.updated    