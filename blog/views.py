from django.db.models.aggregates import Count
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404
from taggit.models import Tag

# Create your views here.
# def blogHome(request): 
#     allPosts= Post.objects.all().order_by('pk')#[:20]
#     context={'allPosts': allPosts}
#     return render(request, "home/home.html", context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 9
    template_name = 'blog/blogHome.html'



# For tags 
def blogHome(request, tag_slug = None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = Post.published.all(tags__in = [tag])
    paginator = Paginator(object_list,9)# 9 posts at single page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/blogHome.html',{'page':page,'posts':posts, 'tag': tag})



def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    # for show views in post
    post.views= post.views +1
    post.save()
    # for shows comment in blog
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)


#To display a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
                             
# FOR COMMENTS
    # for show views in post
    post.views= post.views +1
    post.save()

    
    # for shows comment in blog
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
        # for simillar tags 
    post_tags_ids = post.tags.values_list('id', flat = True) 
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(slug=post.slug)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]  

    return render(request,'blog/blogPost.html',{'post':post,'comments': comments, 'user': request.user, 'replyDict': replyDict,'similar_posts':similar_posts})


# FOR SHARE THE THROUGH EMAIL 
# def post_share(request,post_id):
#     post = get_object_or_404(Post,id=post_id,status='published')
#     sent = False
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             #.....send email
#             post_url= request.build_absolute_url(post.get_absolute_url())
#             subject = f"{cd['name']} recommends you read" f"{post.title}"
#             message = f"Read {post.tile} at {post_url}\n\n" f"{cd['name']}\s comments: {cd['comments']}"
#             send_mail(subject,message,'khand7661@gmail.com', [cd['to']])
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(request,'blog/post/share.html',{'post':post, 'form':form, 'sent':sent})







def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
            # return redirect("blog/blogPost")
    return redirect(f"/blog/{post.slug}")

