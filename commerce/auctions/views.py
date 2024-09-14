from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from .models import *
from .forms import *




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





@login_required
def create_listing(request):
    
    if request.method == "POST": 
        listing_form = ListingForm(request.POST)
        if listing_form.is_valid(): 
            new_listing = listing_form.save(commit=False)
            new_listing.auctioneer = request.user
            new_listing.current_bid = new_listing.starting_bid
            new_listing.save()
            return redirect('view_listing', listing_id=new_listing.id)
    else:
        listing_form = ListingForm()
    
    return render(request, 'auctions/create_listing.html', {
        'listing_form': listing_form
    })
                   
            
def all_categories(request):
    return render(request, "auctions/view_categories.html")

@login_required
def view_watchlist(request):
    return HttpResponseRedirect(reverse("index"))

def filter(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        listings = Listing.objects.filter(item_category=category, is_available=True)
    except Category.DoesNotExist:
        listings = []

    return render(request, 'auctions/filter.html', {
        'category': category_name,
        'listings': listings
    })

def view_listing(request, listing_id):
    current = Listing.objects.get(pk=listing_id)
    count = current.watchers.count()
    # watchers = [i.username for i in current.watchers.all()]
    pending_bids = [bid for bid in Bid.objects.all()]
    
    # try:
    #     bids = Bid.objects.all()
    #     pending_bids = [bid for bid in bids]
    #     # pending_bids = Bid.objects.filter(current_item=current)
    #     # pending_bids = [bid for bid in bids]
    #     # listings = Listing.objects.filter(item_category=category, is_available=True)
    # except Category.DoesNotExist:
    #     pending_bids = []
    # if request.method == "POST":
    #     if 'watchlist' in request.POST:
    #         pass
    #     elif 'place_bid' in request.POST:
    #         return render(request, "auctions/view_listing.html")
    #         # return redirect('create_bid', listing_id=listing_id)

    return render(request, "auctions/view_listing.html",{
                'listing': current,
                'count': count ,
                'watchers':watchers,
                'bids': pending_bids
        })

@login_required
def create_bid(request, listing_id):
    
    target_listing = get_object_or_404(Listing, pk=listing_id)
    
    if target_listing.is_available == False:
        messages.error(request, "This auction has ended.")
        return redirect('view_listing', listing_id=listing_id)
    
    if request.method =="POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            # if bid_form.bid_offer > target_listing.current_bid:
                confirmed_bid = bid_form.save(commit=False)
                confirmed_bid.current_user = request.user
                confirmed_bid.current_item = target_listing
                confirmed_bid.bid_offer = request.POST['bid_offer']
                confirmed_bid.save()
                target_listing.current_bid = confirmed_bid.bid_offer
                target_listing.watchers.add(request.user)
                # target_listing.watchers.add(request.user)
                target_listing.save()
                messages.success(request, "Your bid was placed successfully!")
                return redirect('view_listing', listing_id=listing_id)
            # else:
            #     pass
    else:
        bid_form = BidForm()

    return render(request, "auctions/create_bid.html", {
        'bid_form': bid_form,
        'listing': target_listing
    })

