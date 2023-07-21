from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing

def index(request):
    # Get all active listings
    listings = Listing.objects.filter(is_active=True)

    # Get all categories
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def display_category(request):
    if request.method == "POST":
        # Get all active listings and filter by category
        listings = Listing.objects.filter(is_active=True, category=Category.objects.get(name=request.POST["category"]))

        # Get all categories
        categories = Category.objects.all()

        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
        })


def listing(request, listing_id):
    # Check if listing is in user's watchlist
    if request.user.is_authenticated:
        watchlist = Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists()
    else:
        watchlist = False

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "watchlist": watchlist
    })


def create_listing(request):
    if request.method == "POST":
        # Get form information
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]

        owner = request.user

        # Create new listing
        new_listing = Listing(
            title=title,
            description=description,
            image=image,
            price=price,
            category=Category.objects.get(name=category),
            owner=owner
            )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        # Get all categories
        categories = Category.objects.all()

        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })


def remove_watchlist(request, listing_id):
    # Remove listing from user's watchlist
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def add_watchlist(request, listing_id):
    # Add listing to user's watchlist
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
