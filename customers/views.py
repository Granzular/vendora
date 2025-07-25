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
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,password=password)
            Customer.objects.create(user=user)

            return redirect(reverse("customers:login"))
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
                        resolve(urlparse(next_url.path))
                        return redirect(next_url)
                    except Resolver404:
                        return redirect(reverse("store:index"))
                else:
                    return redirect(reverse("store:index"))

            else:
                context = {
                        "loginform":form,
                        "error":"user does not exist"
                        }
                return render(request,"customers/login.html",context)
        else:
            context= {
                    "loginform":form,
                    "error":"invalid form data"
                    }
            return render(request,"customers/login.html",context)

def logoutView(request):
    logout(request)

    return redirect(reverse("customers:login"))
