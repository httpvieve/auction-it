from django.contrib.auth.models import AbstractUser
from django.db import models

class User (AbstractUser):

    def __str__(self):
        return f"{self.username}"
     
class Category(models.Model):
    
    tag = models.CharField(max_length = 25)
    def __str__(self):
        return f"{self.tag}"
class Listing (models.Model):
    
    # categories = [
    #     ('Fashion/Clothes','Fashion/Clothes'),
    #     ('Gaming','Gaming'),
    #     ('Health & Beauty','Health & Beauty'),
    #     ('Collectibles','Collectible'),
    #     ('Books','Books'),
    #     ('Electronics','Electronics'),
    #     ('Sports & Outdoors','Sports & Outdoors'),
    #     ('Camera/Photo','Camera/Photo'),
    #     ('Home','Home'),
    #     ('Others','Others')
    # ]
    
    auctioneer =  models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listing")
    time_created = models.DateTimeField(auto_now = True)
    
    item_name = models.CharField(max_length = 64)
    item_image = models.URLField(max_length=256, blank=True)
    item_description = models.TextField()
    item_category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL, related_name = "categories")
    is_available = models.BooleanField(default = True)
    
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    starting_bid = models.DecimalField(max_digits = 9, decimal_places = 2)
    current_bid = models.DecimalField(max_digits = 9, decimal_places = 2, null = True, blank = True)
    auction_winner = models.CharField(max_length = 64, null = True, blank = True) 
    
        
    def __str__(self):
        return f'{self.auctioneer} have listed an item "{self.item_name}" for PHP {self.starting_bid}.'

class Bid (models.Model):
    
    current_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid")
    current_item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bid")
    # current_time = models.DateTimeField(auto_now = True)
    bid_offer = models.DecimalField(max_digits = 9, decimal_places = 2)
    
    def __str__(self):
        return f'{self.current_user} have placed a bid on "{self.current_item}" for PHP {self.bid_offer}.'

# class UserWatchlist (models.Model):
    
#     current_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "watch_list")
#     current_item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "watched_by")
    
#     def __str__(self):
#         return f'{self.current_user} have added item "{self.item_name}" to their watchlist.'

class UserComment (models.Model):
    
    current_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    current_item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
    comment = models.TextField()
    time_created = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.user} left a comment:"

