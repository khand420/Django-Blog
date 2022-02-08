

from django.contrib import admin
from django.urls import path, include
from home import views
# from blog.views import blogHome

urlpatterns = [
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),

    # path for searching the query of code2hell blog
    path('search', views.search, name="search"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),

    # path('', views.blogTitle, name="bloghome"),

    
]