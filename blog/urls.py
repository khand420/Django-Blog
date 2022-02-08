from django.contrib import admin
from django.urls import path, include
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'


urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name="bloghome"),
    #  path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<str:slug>', views.blogPost, name="blogPost"),
    path('feed/', LatestPostFeed(), name='post_feed'),
]
