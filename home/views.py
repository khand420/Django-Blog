
from django.db.models.query_utils import Q
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages 
from django.contrib.auth.models import User 
from blog.models import Post
# from blog.views import blogHome



from django.contrib.auth  import authenticate,  login, logout

# Create your views here.
def home(request): 
    return render( request, 'home/home.html')
    # return HttpResponse('This is home')
    

def about(request): 
    return render( request, 'home/about.html')
    # return HttpResponse('This is about')


 
    
# Authentication API start

# ****contact****
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent. Thank you!")
    return render(request, "home/contact.html")



# ****Searching Result****

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none() #for empty list in the all post
    else:
        allPosts=Post.objects.filter(Q(title__icontains=query) | Q(publish__icontains=query) | Q(content__icontains=query))

        # allPostsTitle= Post.objects.filter(title__icontains=query)#icontains it helps to find the search result in django
        # allPostsAuthor= Post.objects.filter(slug__icontains=query)
        # allPostsContent =Post.objects.filter(content__icontains=query)
        # allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor) #Union use to merge query like title, content search in the post
    # if allPosts.count()==0:
    #     messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)  
 



# *******SIGN UP******

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        
        # user name must be alphabate and number
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        #  for password
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match!")
             return redirect('home')
        
        if len(pass1 or pass2) < 8:
            messages.error(request, "Make sure your password is at lest 8 letters")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Code2hell Account has been successfully created :)")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")



# ****LOGIN*****

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In :)")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please Login Again :(")
            return redirect("/")

    return HttpResponse("404- Not found")




# ****LOGOUT*****
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')


# Create your views here.
# def blogTitle(request): 
#     allPosts= Post.objects.all()
#     context={'allPosts': allPosts}
#     return render(request, "home.html", context)