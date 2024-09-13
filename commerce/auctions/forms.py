from django import forms
from .models import *
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'item_description', 'item_image']
        labels = {
            'item_name': 'Name', 
            'item_description': 'Description', 
            'item_image' :'Image URL',
            # 'starting_bid': 'Starting Bid'
        }
        widgets = {
            'item_name': forms.TextInput(), 
            'item_description': forms.Textarea(), 
            'item_image': forms.URLInput(), 
            # 'item_category': forms.CheckboxSelectMultiple(),
            # 'starting_bid': forms.DecimalField(),
        }

class BidForm(forms.Form):
    title = forms.CharField(label="Title: ", max_length=200, required=True,
        widget = forms.Textarea(attrs={'style': 'width: 80%; height: 40px; display: block;'})
        )
    content = forms.CharField(
        label = "Content:",
        widget = forms.Textarea(attrs={'style': 'width: 80%; height: 50%;'}
    )
    )
class CommentForm(forms.Form):
    title = forms.CharField(label="Title: ", max_length=200, required=True,
        widget = forms.Textarea(attrs={'style': 'width: 80%; height: 40px; display: block;'})
        )
    content = forms.CharField(
        label = "Content:",
        widget = forms.Textarea(attrs={'style': 'width: 80%; height: 50%;'}
    )
    )