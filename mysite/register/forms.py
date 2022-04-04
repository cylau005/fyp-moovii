from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    cc_name = forms.CharField(label='Credit Card Name', max_length=40, required=False)
    cc_number = CardNumberField(label='Card Number', required=False)
    cc_expirydate = CardExpiryField(label='Expiration Date', required=False)
    cc_cvv = SecurityCodeField(label='CVV/CVC', required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2","first_name","last_name","cc_number","cc_name","cc_expirydate","cc_cvv"]
  