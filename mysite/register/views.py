from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Account, CreditCard
from main.models import MovieList
from django.contrib.auth.models import User

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
            ccnumber = form.cleaned_data["cc_number"]
            ccname = form.cleaned_data["cc_name"]
            ccexpirydate = form.cleaned_data["cc_expirydate"]
            cccvv = form.cleaned_data["cc_cvv"]
            
            
            # Unique username check
            user_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)
            ccnum_check = CreditCard.objects.filter(cc_number=ccnumber)
            
            if not user_check and not email_check and not ccnum_check:
                msg = 'Account created'
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()
                t = Account(user=user, genres=g)
                t.save()
                c = CreditCard(user=user, cc_number=ccnumber, cc_name=ccname, cc_expirydate=ccexpirydate, cc_cvv=cccvv)
                c.save()

                # # to get the domain of the current site  
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
                if not user_check and email_check:
                    msg = 'Username/Email Address exist. Please try with others'
                if user_check and not email_check:
                    msg = 'Username/Email Address exist. Please try with others'
                if ccnum_check:
                    msg = 'Credit Card used in other account. Please try with other credit card'
        
        else:
            msg = 'Username/Email Address exist. Please try with others'
            
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
        print(uid)
        #user = UserModel._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
        print(user)
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
