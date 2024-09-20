from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse


from .models import *
from .forms import *

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
    watched_listings = Listing.objects.filter(watchers=request.user)
    return render(request, "auctions/view_watchlist.html", {
        "auctions": watched_listings
    })

@login_required
def user_listing(request):
    user_listings = Listing.objects.filter(auctioneer=request.user)
    return render(request, "auctions/user_listing.html", {
        "auctions": user_listings
    })
    
    
def filter(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        listings = Listing.objects.filter(item_category=category, is_available=True)
    except Category.DoesNotExist:
        listings = []

    return render(request, 'auctions/filter.html', {
        'category': category_name.lower(),
        'auctions': listings
    })

@login_required
def view_listing(request, listing_id):
    
    current = Listing.objects.get(pk=listing_id)
    count = Bid.objects.filter(current_item=current.id).count()
    pending_bids = [bid for bid in Bid.objects.all()]
    comments = UserComment.objects.filter(current_item=current)
    
    if request.method == 'POST':
        if "add_to_watchlist" in request.POST:
            current.watchers.add(request.user)
        elif "remove_from_watchlist" in request.POST:
            current.watchers.remove(request.user)
        elif "close_auction" in request.POST:
            current.is_available = False
            if current.current_bid != current.starting_bid:
                highest_bid = Bid.objects.get(bid_offer = current.current_bid) 
                current.auction_winner = highest_bid.current_user.username
            # current.watchers.clear()
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit = False)
                new_comment.current_user = request.user
                new_comment.current_item = current
                new_comment.comment = request.POST['comment']
                new_comment.save()
        current.save()

    comment_form = CommentForm()
    
    return render(request, "auctions/view_listing.html",{
                'listing': current,
                'count': count ,
                'bids': pending_bids,
                'comments': comments,
                'comment_form': comment_form    
        })
 
@login_required
def create_bid(request, listing_id):
    
    target_listing = get_object_or_404(Listing, pk=listing_id)

    if request.method =="POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            offer = bid_form.cleaned_data['bid_offer']
            current_price = target_listing.current_bid or target_listing.starting_bid
            if offer > current_price:
                confirmed_bid = bid_form.save(commit=False)
                confirmed_bid.current_user = request.user
                confirmed_bid.current_item = target_listing
                confirmed_bid.bid_offer = offer
                confirmed_bid.save()
                
                target_listing.current_bid = offer
                target_listing.watchers.add(request.user)
                target_listing.save()   
                
                if len(request.POST['comment']) > 0 :
                    comment_form = CommentForm()
                    new_comment = comment_form.save(commit = False)
                    new_comment.current_user = request.user
                    new_comment.current_item = target_listing
                    new_comment.comment = request.POST['comment']
                    new_comment.save()
                
                messages.success(request, "Your bid was placed successfully!")
                return redirect('view_listing', listing_id=listing_id)
            else:
                messages.error(request, f'Your bid must be higher than the current bid of {target_listing.current_bid}.')
    else:
        bid_form = BidForm()

    return render(request, "auctions/create_bid.html", {
        'bid_form': bid_form,
        'listing': target_listing
    })

