from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by("id").reverse()

    # Paginate posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/index.html", {
        "posts": page_obj
    })

def profile(request, user_id):
    # Get user info and posts
    user = User.objects.get(pk=user_id)
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    posts = Post.objects.filter(user=user).order_by("id").reverse()
    
    # Check if user is following profile
    try:
        Follow.objects.get(follower=request.user, following=user)
        is_following = True
    except Follow.DoesNotExist:
        is_following = False

    # Paginate posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/profile.html", {
        "posts": page_obj,
        "username": user.username,
        "user_profile": user,
        "followers": followers,
        "following": following,
        "is_following": is_following
    })

def follow(request):
    # Follow a user
    requested_user = request.POST["user_follow"]
    follow_request = User.objects.get(username=requested_user)
    user = User.objects.get(pk=request.user.id)
    follow = Follow(follower=user, following=follow_request)
    follow.save()

    return HttpResponseRedirect(reverse("profile", args=(follow_request.id,)))

def unfollow(request):
    # Unfollow a user
    requested_user = request.POST["user_unfollow"]
    follow_request = User.objects.get(username=requested_user)
    user = User.objects.get(pk=request.user.id)
    follow = Follow.objects.get(follower=user, following=follow_request)
    follow.delete()

    return HttpResponseRedirect(reverse("profile", args=(follow_request.id,)))

def new_post(request):
    if request.method == "POST":

        # Make a new post
        content = request.POST["content"]
        user = request.user
        post = Post(content=content, user=user)
        post.save()

        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
