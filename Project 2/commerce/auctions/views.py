from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def index(request):
    # Get all active listings
    listings = Listing.objects.filter(is_active=True)

    # Get all categories
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def display_watchlist(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "Please login to view your watchlist."
        })

    # Get user's watchlist
    user = request.user
    listings = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
        })


def create_listing(request):
    if request.method == "POST":
        # Get form information
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]

        # Create a new bid
        bid = Bid(
            bidder=request.user,
            bid=float(price),
            )
        bid.save()


        # Create new listing
        new_listing = Listing(
            title=title,
            description=description,
            image=image,
            price=bid,
            category=Category.objects.get(name=category),
            owner=request.user
            )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        # Get all categories
        categories = Category.objects.all()

        return render(request, "auctions/create_listing.html", {
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

    # Check if listing is active
    is_active = Listing.objects.get(pk=listing_id).is_active

    # Check if listing is closed and user is the winner
    if is_active == False and Listing.objects.get(pk=listing_id).price.bidder.username == request.user.username:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": watchlist,
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "You won the auction!",
            "update": True,
            "error": False,
            "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
            "is_active": is_active,
        })
    # Check if listing is closed and user is not the winner
    elif is_active == False:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": watchlist,
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "Listing closed.",
            "update": True,
            "error": False,
            "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
            "is_active": is_active,
        })
    # Display if listing is active
    else:
        return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "watchlist": watchlist,
        "comments": Comment.objects.filter(listing=listing_id),
        "error_message": "No error.",
        "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
        "is_active": is_active,
    })


def close_listing(request, listing_id):
    # Get listing
    listing = Listing.objects.get(pk=listing_id)

    # Close listing
    listing.is_active = False
    listing.save()

    return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists(),
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "Listing closed.",
            "update": True,
            "error": False,
            "is_active": False,
        })


def add_comment(request, listing_id):
    # Create new comment
    new_comment = Comment(
        author=request.user,
        listing=Listing.objects.get(pk=listing_id),
        comment=request.POST["comment"]
        )
    new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def add_bid(request, listing_id):
    # Get bid amount
    bid = float(request.POST["bid"])

    # Get current bid
    current_bid = Listing.objects.get(pk=listing_id).price.bid

    # Check if listing is active
    is_active = Listing.objects.get(pk=listing_id).is_active

    # Check if bid is higher than current bid
    if bid > current_bid:
        # Create new bid
        new_bid = Bid(
            bidder=request.user,
            bid=bid
            )
        new_bid.save()

        # Update listing with new bid
        listing = Listing.objects.get(pk=listing_id)
        listing.price = new_bid
        listing.save()

        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists(),
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "Bid success! You are now the highest bidder",
            "update": True,
            "error": False,
            "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
            "is_active": is_active,
        })
    else:
        # Display error message
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists(),
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "Bid must be higher than current bid.",
            "update": True,
            "error": True,
            "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
            "is_active": is_active,
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
