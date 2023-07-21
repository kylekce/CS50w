from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="create_listing"),
    path("displayCategory", views.display_category, name="display_category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("removeWatchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("addWatchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
]
