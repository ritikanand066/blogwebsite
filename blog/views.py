from django.shortcuts import render,HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Home
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

# About 
def about(request):
    return render(request,'blog/about.html')

# Contact
def contact(request):
    return render(request,'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts, 'full_name':full_name, 'groups':groups})
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup
def user_signup(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, "Successfully Created")
            user=fm.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        fm=SignUpForm()
    return render(request,'blog/signup.html',{'form':fm})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'Logged In Successfully!!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm=LoginForm()
        return render(request,'blog/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm = PostForm(request.POST)
            if fm.is_valid():
                title=fm.cleaned_data['title']
                description = fm.cleaned_data['description']
                pst = Post(title=title,description=description)
                pst.save()
        else:
            fm = PostForm()
        return render(request,'blog/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

# Update Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi = Post.objects.get(pk=id)
            fm = PostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi=Post.objects.get(pk=id)
            fm = PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')