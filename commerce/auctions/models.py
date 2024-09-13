from django.contrib.auth.models import AbstractUser
from django.db import models

class User (AbstractUser):

    def __str__(self):
        return f"{self.username}"
     
class Category(models.Model):
    tag = models.CharField(max_length = 32, unique = True)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.tag}"
class Listing (models.Model):
    
    auctioneer =  models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listing")
    time_created = models.DateTimeField(auto_now = True)
    
    item_name = models.CharField(max_length = 64)
    item_image = models.URLField(blank = True)
    item_description = models.TextField()
    item_category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL, related_name = "categories")
    is_available = models.BooleanField(default = True)
    
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    starting_bid = models.DecimalField(max_digits = 9, decimal_places = 2)
    current_bid = models.DecimalField(max_digits = 9, decimal_places = 2, null = True, blank = True)
    auction_winner = models.CharField(max_length = 64, null = True, blank = True) 
    
        
    def __str__(self):
        return f' "{self.item_name} ({self.current_bid})"'

class Bid (models.Model):
    
    current_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid")
    current_item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bid")
    # current_time = models.DateTimeField(auto_now = True)
    bid_offer = models.DecimalField(max_digits = 9, decimal_places = 2)
    
    def __str__(self):
        return f'{self.current_user} bids {self.current_item} for PHP {self.bid_offer}.'

class UserComment (models.Model):
    
    current_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    current_item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    comment = models.TextField()
    time_created = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.user} left a comment:"

