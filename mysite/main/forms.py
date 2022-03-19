from django import forms
from django.contrib.auth.models import User
from .models import RatingList, Reward_Point

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

RATE_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

ACTION_CHOICES = [
    ('Rate','Rate'),
    ('Share','Share'),
]

PRIZE_CHOICES = [
    (1,"Movie Ticket"),
    (2,"Cinema Food Voucher"),
    (3,"One Month Subscription"),
]

class RatingForm(forms.Form):
    rating_score = forms.IntegerField(label='Rating Score', 
                  widget=forms.Select(choices=RATE_CHOICES))
    movie_id = forms.IntegerField(label='Movie ID')
    action = forms.CharField(label='Rate or Share', 
            widget=forms.Select(choices=ACTION_CHOICES))

    class Meta:
        model = RatingList
        fields = ["rating_score", "movie_id", "action"]
  
class RedeemForm(forms.Form):
    redeem_item_id = forms.IntegerField(label='Prize ID', 
                  widget=forms.Select(choices=PRIZE_CHOICES))
    
    class Meta:
        model = Reward_Point
        fields = ["redeem_item_id"]
