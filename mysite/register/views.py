from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import login, authenticate  
from django.contrib.auth.tokens import default_token_generator

from .tokens import account_activation_token  
from .forms import RegisterForm
from .models import Account, CreditCard, BankIn
from main.models import MovieList


# Function for registration
def register(request):
    
    # Populate all distinct movie genre into Registration page's favourite genre drop down list
    # Get individual genres from MovieList
    movie = MovieList.objects.values_list("movie_genre", flat=True).distinct()
    
    genre_list = ''
    for i in movie:
        genre_list = genre_list + '|' + i
    split_genre = genre_list.split('|')
    split_genre = list(dict.fromkeys(split_genre))
    split_genre = list(filter(None, split_genre))
    msg = ''

    gender_list = ['Male','Female']

    # Form for registration
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            dob = form.cleaned_data["dob"]      
            gender = request.POST['gender_chosen']
            g = request.POST['genres_chosen']
            paymentRadio = request.POST['paymentRadio'] 
            
            # Unique username and email address check
            user_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)

            # If no user found in database, add user
            if not user_check and not email_check:

                # If is credit card payment method, add user and credit card
                if paymentRadio == 'cc':
                    ccnumber = form.cleaned_data["cc_number"] or None
                    ccname = form.cleaned_data["cc_name"] or None
                    ccexpirydate = form.cleaned_data["cc_expirydate"] or None
                    cccvv = form.cleaned_data["cc_cvv"] or None
                    msg = 'Account created'
                    user = form.save(commit=False)  
                    user.is_active = False  
                    user.save()
                    t = Account(user=user, genres=g, gender=gender, dob=dob)
                    t.save()
                    print('account save')   

                    # Ensure credit card info is not empty, then add record

                    if ccnumber is not None and ccname is not None and ccexpirydate is not None and cccvv is not None:
                        c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
                        c.save()
                        
                        # Trigger account activation email to registered user
                        # To get the domain of the current site  
                        
                        #current_site = get_current_site(request)  
                        domain = 'fyp-moovii.herokuapp.com'
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = default_token_generator.make_token(user)

                        print(domain)
                        print(uid)
                        print(token)

                        mail_subject = 'Activate Your Account'  
                        message = render_to_string('register/acc_active_email.html', {  
                            'user': user,  
                            'domain': domain,  
                            'uid':uid,  
                            'token':token,  
                        })  

                        print('Sending email...')

                        to_email = email
                        emailSend = EmailMessage(  
                                    mail_subject, message, to=[to_email]  
                        )  
                        emailSend.send()  
                        msg = 'Account created successfully. Please check your mailbox and comfirm your email address'
                    
                    else:
                        msg = 'Please check the payment detail'

                # If payment method is bank transfer/paynow
                #  Add record to User model and BankIn model
                if paymentRadio == 'bi':
                    user = form.save(commit=False)  
                    user.is_active = False  
                    user.save()
                    t = Account(user=user, genres=g, gender=gender, dob=dob)
                    t.save()
                    print('account save')
                    d = BankIn(user=user)
                    d.save()
                    print('bi save')

                    # Email customer and say we will activate your account after confirming your payment
                    # Admin to check if receive money in bank account, if yes, activate account manually
                    mail_subject = 'We will activate your account as soon as possible'  
                     # To get the domain of the current site  
                    current_site = get_current_site(request)  
                    message = render_to_string('register/acc_active_email_bi.html', {  
                        'user': user,  
                    })  

                    to_email = email
                    emailSend = EmailMessage(  
                                mail_subject, message, to=[to_email]  
                    )  
                    emailSend.send()  
                    msg = 'We will verify your payment and activate your account within 3 business days'
            else:
                msg = 'Username / Email address exists. Please try other'
        else:
            msg = 'Please check the payment detail'
        
    else:
        form = RegisterForm()
        account_form = Account()
        credit_form = CreditCard()
    
    context = {"form":form, 
                "split_genre":split_genre, 
                "gender_list":gender_list,
                "msg":msg
    }

    return render(request, "register/register.html", context)


# Function for account activation from email
def activate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        msg = 'Account activated'
        return render(request, "register/register-activated.html", {"msg":msg})
    else:
        msg = 'Activation link expired. Please contact our customer service'
        return render(request, "register/register-activated.html", {"msg":msg})
