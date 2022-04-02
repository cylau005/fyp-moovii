from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, CreditCard, BankIn
from main.models import MovieList

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import login, authenticate  
from django.views.generic import View, UpdateView
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def register(request):
    # Get individual genres from MovieList
    movie = MovieList.objects.values_list("movie_genre", flat=True).distinct()
    total_movie = len(movie)
    genre_list = ''
    for i in movie:
        genre_list = genre_list + '|' + i
    split_genre = genre_list.split('|')
    split_genre = list(dict.fromkeys(split_genre))
    split_genre = list(filter(None, split_genre))
    msg = ''
    
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]            
            g = request.POST['genres_chosen']
            paymentRadio = request.POST['paymentRadio'] 
            
            print(paymentRadio)
            
            # Unique username check
            user_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)

        
            if not user_check and not email_check:
                if paymentRadio == 'cc':
                    ccnumber = form.cleaned_data["cc_number"] or None
                    ccname = form.cleaned_data["cc_name"] or None
                    ccexpirydate = form.cleaned_data["cc_expirydate"] or None
                    cccvv = form.cleaned_data["cc_cvv"] or None
                    msg = 'Account created'
                    user = form.save(commit=False)  
                    user.is_active = False  
                    user.save()
                    t = Account(user=user, genres=g)
                    t.save()
                    print('account save')   

                    print(ccnumber)

                    if ccnumber is not None and ccname is not None and ccexpirydate is not None and cccvv is not None:
                        c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
                        c.save()
                        print('cc save')

                        # To get the domain of the current site  
                        current_site = get_current_site(request)  
                        mail_subject = 'Activate Your Account'  
                        message = render_to_string('register/acc_active_email.html', {  
                            'user': user,  
                            'domain': current_site.domain,  
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                            'token':default_token_generator.make_token(user),  
                        })  

                        to_email = form.cleaned_data.get('email')  
                        email = EmailMessage(  
                                    mail_subject, message, to=[to_email]  
                        )  
                        email.send()  
                        msg = 'Account created successfully. Please check your mailbox and comfirm your email address'
                    
                    else:
                        msg = 'Please check the payment detail'
                        
                if paymentRadio == 'bi':
                    user = form.save(commit=False)  
                    user.is_active = False  
                    user.save()
                    t = Account(user=user, genres=g)
                    t.save()
                    print('account save')
                    d = BankIn(user=user)
                    d.save()
                    print('bi save')
                    mail_subject = 'We will activate your account as soon as possible'  
                     # To get the domain of the current site  
                    current_site = get_current_site(request)  
                    message = render_to_string('register/acc_active_email_bi.html', {  
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                        'token':default_token_generator.make_token(user),  
                    })  

                    to_email = form.cleaned_data.get('email')  
                    email = EmailMessage(  
                                mail_subject, message, to=[to_email]  
                    )  
                    email.send()  
                    msg = 'We will verify your payment and activate your account within 3 business days'
            else:
                msg = 'Username / Email address exists. Please try other'
        else:
            msg = 'Please check the payment detail'
            
        return render(request, "register/register.html", {"form":form, "split_genre":split_genre, "msg":msg})
    else:
        form = RegisterForm()
        account_form = Account()
        credit_form = CreditCard()
    
    return render(request, "register/register.html", {"form":form, "split_genre":split_genre, "msg":msg})

def activate(request, uidb64, token):
    print('activation link')
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
