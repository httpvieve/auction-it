from django import forms
from .models import *
from django.core.exceptions import ValidationError 

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ['item_name', 'item_description','item_image', 'item_category','starting_bid']
        labels = {
            'item_name': 'Product Name * ', 
            'item_description': 'Product Description ',
            'item_image':'Image URL ',
            'item_category':'Select Category *  ',
            'starting_bid': 'Initial Price * '
        }
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'auction-name'}), 
            'item_description': forms.Textarea(attrs={'class': 'auction-description'}), 
            'item_image': forms.URLInput(attrs={'class': 'auction-img'}), 
            # 'item_category': forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None),
            'starting_bid': forms.NumberInput(attrs={'class': 'initial-price'})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_offer']
        widgets = {
            'bid_offer': forms.NumberInput()
        }
    def __init__(self, *args, **kwargs):
            self.listing = kwargs.pop('listing', None)
            super(BidForm, self).__init__(*args, **kwargs)

    def clean_bid_offer(self):
        bid_offer = self.cleaned_data['bid_offer']
        if self.listing:
            current_bid = self.listing.current_bid or self.listing.starting_bid
            if bid_offer <= current_bid:
                raise ValidationError(f'Your bid must be higher than the current bid of {current_bid}.')
        return bid_offer

class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'comment'})
        }