from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    # cc_number = forms.CharField(label='Credit Card Number', max_length=16)
    # cc_name = forms.CharField(label='Credit Card Name', max_length=40)
    # cc_expirydate = forms.CharField(label='Credit Card Expiry Date(MMYY)', max_length=4)
    # cc_cvv = forms.CharField(label='Credit Card CVV', max_length=3)
    # cc_number = forms.CharField(label='Credit Card Number', max_length=16)
    cc_name = forms.CharField(label='Credit Card Name', max_length=40)
    # cc_expirydate = forms.CharField(label='Credit Card Expiry Date(MMYY)', max_length=4)
    # cc_cvv = forms.CharField(label='Credit Card CVV', max_length=3)

    cc_number = CardNumberField(label='Card Number')
    cc_expirydate = CardExpiryField(label='Expiration Date')
    cc_cvv = SecurityCodeField(label='CVV/CVC')

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2","first_name","last_name","cc_number","cc_name","cc_expirydate","cc_cvv"]
  