from django import forms
from .models import *


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ['item_name', 'item_description','item_image', 'item_category','starting_bid']
        labels = {
            'item_name': 'Name', 
            'item_description': 'Description',
            'item_image':'Image URL',
            'item_category':'Select category',
            'starting_bid': 'Starting Bid'
        }
        widgets = {
            'item_name': forms.TextInput(), 
            'item_description': forms.Textarea(), 
            'item_image': forms.URLInput(), 
            # 'item_category': forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None),
            'starting_bid': forms.NumberInput()
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_offer']
        widgets = {
            'bid_offer': forms.NumberInput()
        }
        # def __init__(self, *args, listing=None, **kwargs):
        #     self.listing = listing
        #     super().__init__(*args, **kwargs)

        # def clean_bid_offer(self):
        #     bid_offer = self.cleaned_data['bid_offer']
        #     if self.listing:
        #         if bid_offer <= self.listing.current_bid:
        #             raise forms.ValidationError("Your bid must be higher than the current bid.")
        #     return bid_offer
class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea()
        }