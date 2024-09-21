from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import models
from django.apps import apps
from .models import *

LISTING_CATEGORIES = [
    "Art",
    "Books",
    "Collectibles and Toys",
    "Electronics",
    "Fashion and Clothes",
    "Gaming",
    "Health and Beauty",
    "Home",
    "Music",
    "Office Supplies",
    "Sports and Outdoors",
    "Others"
]
class User (AbstractUser):

    def __str__(self):
        return f"{self.username}"
     
class Category(models.Model):
    name = models.CharField(max_length = 32, unique = True)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"
    
class Listing (models.Model):
    
    auctioneer =  models.ForeignKey(User,null = True, blank = True, on_delete = models.CASCADE, related_name = "listing")
    time_created = models.DateTimeField(auto_now = True)
    
    item_name = models.CharField(max_length = 128)
    item_image = models.URLField(blank = True)
    item_description = models.TextField(null = True, blank = True)
    item_category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL, related_name = "categories")
    is_available = models.BooleanField(default = True)
    
    watchers = models.ManyToManyField(User, blank = True, related_name="watchlist")
    
    starting_bid = models.DecimalField(max_digits = 9, decimal_places = 2)
    current_bid = models.DecimalField(max_digits = 9, decimal_places = 2, null = True, blank = True)
    auction_winner = models.CharField(max_length=128, null = True, blank = True) 
        
    def __str__(self):
        return f'{self.auctioneer} listed {self.item_name} for {self.current_bid}.'
class UserComment (models.Model):
    
    current_user = models.ForeignKey(User,null = True, blank = True, on_delete = models.CASCADE, related_name = "comments")
    current_item = models.ForeignKey(Listing, null = True, blank = True, on_delete = models.CASCADE, related_name = "comments")
    comment = models.TextField(null = True)
    
    time_created = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.time_created} :{self.current_user} left a comment on auction {self.current_item.item_name}"

class Bid (models.Model):
    
    current_user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE, related_name = "bid")
    current_item = models.ForeignKey(Listing, null = True, blank = True, on_delete = models.CASCADE, related_name = "bid")
    # current_time = models.DateTimeField(auto_now = True)
    bid_offer = models.DecimalField(max_digits = 9, decimal_places = 2, name="bid_offer")
    
    def __str__(self):
        return f'{self.current_user} bids {self.current_item.item_name} for ${self.bid_offer}.'

@receiver(post_migrate)
def create_categories(sender, **kwargs):
    if sender.name == 'auctions': 
        for tag in LISTING_CATEGORIES:
            Category.objects.get_or_create(name=tag)

post_migrate.connect(create_categories, sender=apps.get_app_config('auctions'))



