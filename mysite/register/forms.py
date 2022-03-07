from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GENRES_CHOICES = [
    ('Adventure','Adventure'),
    ('Comedy','Comedy'),
    ('Action','Action'),
    ('Drama','Drama'),
    ('Crime','Crime'),
    ('Children','Children'),
    ('Mystery','Mystery'),
    ('Documentary','Documentary'),
    ('Animation','Animation'),
    ('Thriller','Thriller'),
    ('Horror','Horror'),
    ('Fantasy','Fantasy'),
    ('Western','Western'),
    ('Film-Noir','Film-Noir'),
    ('Romance','Romance'),
    ('War','War'),
    ('Sci-Fi','Sci-Fi'),
    ('Musical','Musical'),
]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    genres = forms.CharField(label='What is your favorite genres?', 
            widget=forms.Select(choices=GENRES_CHOICES))
    cc_number = forms.CharField(label='Credit Card Number')
    cc_name = forms.CharField(label='Credit Card Name')
    cc_expirydate = forms.CharField(label='Credit Card Expiry Date(MM/YY)')
    cc_cvv = forms.CharField(label='Credit Card CVV')

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2","first_name","last_name","genres","cc_number","cc_name","cc_expirydate","cc_cvv"]

