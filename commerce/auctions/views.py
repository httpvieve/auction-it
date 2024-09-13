from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import Category, Listing, Bid, User, UserComment
from .forms import ListingForm, BidForm, CommentForm
LISTING_CATEGORIES = [
    "Art",
    "Books",
    "Collectibles & Toys",
    "Electronics",
    "Fashion/Clothes",
    "Gaming",
    "Health & Beauty",
    "Home",
    "Music",
    "Office Supplies",
    "Sports & Outdoors",
    "Others"
]

def create_listing(request):

    listing_form = ListingForm(request.POST)
    if listing_form.is_valid(): 
            new_listing = listing_form.save()
            new_listing.auctioneer = request.user
            Listing.objects.create(new_listing) 
            # return redirect('view_listing', pk=new_listing.pk)
            # return redirect('index', pk=new_listing.pk)
            return render(request, 'auctions/view_listing.html', {
                'form': ListingForm()
                })
    categories = Category.objects.all()
    return render(request, 'auctions/create_listing.html', {
        'categories':categories
    })
                   
            
def all_categories(request):
    return render(request, "auctions/view_categories.html")


def view_watchlist(request):
    pass


def view_category(request):
    return HttpResponseRedirect(reverse("index"))


def view_listing(request, listing_id):
    current = Listing.objects.get(pk=listing_id)
    count = current.watchers.count()
    return render(request, "auctions/view_listing.html",{
                'listing': current,
                'count': count  
        })


def create_bid(request):
    pass




#############################

def index(request):
    return render(request, "auctions/index.html",{
                "auctions":Listing.objects.all()
        })

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
        
        for i in LISTING_CATEGORIES:
            Category.objects.create(tag=i)

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


