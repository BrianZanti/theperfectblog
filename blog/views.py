from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from forms import UserForm, BlogForm, CommentForm
from django.contrib.auth.models import User
from models import Blogpost, Comment
import datetime

def home(request):
    blogposts = Blogpost.objects.order_by('date_created')[0:10]
    return render(request, "home.html", {'title':'The Perfect Blog', 'blogposts':blogposts})

@login_required
def viewpost(request, id):
    post = Blogpost.objects.filter(pk=id)
    if post.__len__() == 0:
        return render(request, "viewpost.html", {"errors": ["Sorry, there doesn't seem to be a post with that ID"], "title":"An Error Occurred"})
    comments = Comment.objects.filter(blogpost=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(body=form.cleaned_data['body'],
                                             user=request.user,
                                             date_created=datetime.datetime.now(),
                                             blogpost = post)
            comment.save()
            return render(request, "viewpost.html", {'comments':comments, "post": post, 'form':CommentForm, "title":post.title, 'messages':["Your comment was posted successfully"]})
        else:
            return render(request, "viewpost.html", {'comments':comments, "errors":["The information you submitted was invalid"], "title":post.title, 'form':CommentForm, 'post':post})

    return render(request, "viewpost.html", {'comments':comments, "post": post, 'form':CommentForm, "title":post.title})

@login_required()
def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            blogpost = Blogpost.objects.create(title=data['title'], body = data['body'], user = request.user, date_created=datetime.datetime.now())
            blogpost.save()
            comments = Comment.objects.filter(blogpost=blogpost.pk)
            return render(request, "viewpost.html", {"messages":["Your Post was created successfully"], "post":blogpost, "title":blogpost.title, 'form':CommentForm, 'comments':comments})
        else:
            return render(request, "new.html", {"errors":["The information you submitted was invalid"], "title":"New Blogpost"})
    else:
        return render(request, "new.html", {'form':BlogForm, "title":"New Blogpost"})

def createuser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['retypepassword']:
                return render(request, "create.html", {'form':UserForm, 'errors':["Your passwords do not match"]})
            if User.objects.filter(username = form.cleaned_data['username']).__len__() != 0:
                return render(request, "create.html", {'form':UserForm, 'errors':["That Username is already taken"]})
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.save()
            thanks_string = "Thanks for signing up %s!"%(form.cleaned_data['username'])
            context = {"messages":[thanks_string]}
            return render(request, "home.html", context)
        else:
            return render(request, "create.html", {'form':UserForm, 'errors':["Your input was not valid"]})
    else:
        return render(request,"create.html", {'form':UserForm})

@login_required
def account(request):
    posts = Blogpost.objects.filter(user = request.user).order_by("date_created")
    comments = Comment.objects.filter(user = request.user).order_by("date_created")
    return render(request, "account.html", {'user':request.user, 'comments':comments, 'posts':posts})

@login_required
def delete(request):
    posts = Blogpost.objects.filter(user = request.user)
    comments = Comment.objects.filter(user = request.user)
    posts.delete()
    comments.delete()
    request.user.delete()
    return HttpResponseRedirect("/")