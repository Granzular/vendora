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
from .utils import send_confirmation_email, verify_secret_key
from datetime import timedelta
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required,name="dispatch")
class ProfileView(View):

    def get(self,request):
        return render(request,"customers/profile.html")

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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
            user.is_active = False
            user.save()
            Customer.objects.create(user=user)
            request.session["email"] = email
            request.session["username"] = username
            request.session.set_expiry(timedelta(minutes=10)) 
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
                    user = User.objects.get(username=username)
                    if not user.is_active:
                        request.session["email"] = user.email
                        request.session["username"] = username
                        request.session.set_expiry(timedelta(minutes=10))
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

@login_required
def logout_view(request):
    logout(request)

    return redirect(reverse("customers:login"))

    
def confirm_email_view(request):
    """ starts verification process"""
    email = request.session.get('email')
    username = request.session.get('username')
    if username is None:
        return redirect(reverse('customers:login'))
    request.session['username'] = username

    res = send_confirmation_email(email,username)
    msg ="A verification link has been emailed to you!"
    context = {
            "email":email,
            "msg": msg,
            }
    return render(request,"customers/confirm_email.html",context)


def confirm_email_verification_view(request,secret_key):
    """ confirm that the email has been clicked, """
    status, user = verify_secret_key(secret_key)
    if status:
        print("Email Verified!")
        user.is_active = True
        user.save()
        context = {
                "success" : "Email Verified Successfully"
                }
        return render(request,"customers/message.html",context)

    else:
        print("Verification failed")
        context = {
                "failed" : "Email Verification Failed"
                }
        return render(request,"customers/message.html",context)
        
