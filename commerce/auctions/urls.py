from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("categories", views.all_categories, name="categories"),
    path("category/<str:category_name>", views.filter, name="filter"),
    
    path("create", views.create_listing, name="create_listing"),
    path("item/<int:listing_id>", views.view_listing, name="view_listing"),
    path("item/<int:listing_id>/bid", views.create_bid, name="create_bid"),
    path("auction/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path('wishlist/<int:listing_id>/add', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('wishlist/<int:listing_id>/remove', views.add_to_watchlist, name='add_to_watchlist'),
    
    path("user/watchlist", views.view_watchlist, name="watchlist"),
]
