from django.shortcuts import render
from .models import Customer
from django.contrib.auth.models import User
from django.views import View
from .forms import LoginForm, SignUpForm
from django.shortcuts import reverse, redirect
from django.urls import resolve
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse
from django.contrib.auth import login, logout, authenticate
from .utils import send_confirmation_email
from datetime import timedelta
from django.http import Http404

class SignUpView(View):

    def get(self,request):
        form = SignUpForm()
        context = {
                "signupform":form
                }
        return render(request,"customers/signup.html",context)

    def post(self,request):
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,password=password)
            user.is_active = False
            user.save()
            Customer.objects.create(user=user)
            # Send verification email
            send_confirmation_email(email)

            return redirect(reverse("customers:confirm_email"))
        else:
            context = {
                    "signupform":form,
                    "error":"invalid form data"
                    }
            return render(request,"customers/signup.html",context)

class LoginView(View):

    def get(self,request):
        form = LoginForm()
        context = {
                "loginform":form
                }
        return render(request,"customers/login.html",context)

    def post(self,request):
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user:

                login(request,user)
                next_url = request.GET.get("next")
                if next_url:
                    try:
                        resolve(urlparse(next_url).path)
                        return redirect(next_url)
                    except Resolver404:
                        return redirect(reverse("store:index"))
                else:
                    return redirect(reverse("store:index"))

            else:
                try:
                    user = User.objects.get(username=username,password=password)
                    if not user.is_active:
                        request.session["email"] = "ayenimichael92@gmail.com" 
                        request.session.set_expiry(timedelta(minutes=1)) # change to 10 minute
                        return redirect(reverse("customers:confirm_email"))
                except User.DoesNotExist:
                    context = {
                            "loginform":form,
                            "error":"invalid credentials"
                            }
                    return render(request,"customers/login.html",context)

        else:
            context= {
                    "loginform":form,
                    "error":"invalid form data"
                    }
            return render(request,"customers/login.html",context)

def logout_view(request):
    logout(request)

    return redirect(reverse("customers:login"))

    
def confirm_email_view(request):
    """ starts verification process"""
    email = request.session.get("email")
    secret_key = send_confirmation_email(email)
    request.session["secret_key"] = secret_key
    request.set_expiry(timedelta(minutes=1)) # change to 10 minutes
    context = {
            "email":email,
            }
    return render(request,"customers/confirm_email.html")

def confirm_email_verification_view(request,secret_key):
    """ confirm that the email has been clicked, """

    if secret_key == request.session.get("secret_key"):
        print("Email Verified!")
        return redirect(reverse("customers:login"))

    else:
        print("Verification failed")
        raise Http404
        
