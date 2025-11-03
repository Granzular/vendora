from django.shortcuts import render
from .models import Customer,Notification, CustomUser
from django.views import View
from .forms import LoginForm, SignUpForm, ProfileForm
from django.shortcuts import reverse, redirect, get_object_or_404
from django.urls import resolve
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse
from django.contrib.auth import login, logout, authenticate
from .utils import send_confirmation_email, verify_secret_key,send_notification
from datetime import timedelta
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required,name="dispatch")
class ProfileView(View):

    def get(self,request):
        
        fname = request.user.first_name
        lname = request.user.last_name
        username = request.user.username
        email = request.user.email
        cust = request.user.customer_set.all()[0]
        addr = cust.address
        phone = cust.phone

        profile_form = ProfileForm(initial={"first_name":fname,"last_name":lname,"username":username,"email":email,"delivery_address":addr,"phone":phone})
        context = {
                "profile_form":profile_form
                }
        return render(request,"customers/profile.html",context)

    def post(self,request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get("first_name")
            lname = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            addr  = form.cleaned_data.get("delivery_address")
            phone = form.cleaned_data.get("phone")
            # save changes
            user = request.user
            cust = user.customer_set.all()[0]
            user.first_name = fname
            user.last_name = lname
            user.username = username
            user.email = email
            cust.address = addr
            cust.phone = phone
            user.save()
            cust.save()
            context = {
                    "success" : "profile updated",
                    "profile_form" : form
                    }
            return render(request,"customers/profile.html",context)
        else:
            # if form is not valid
            context = {
                    "failure": "profile not updated",
                    "profile_form" : form,
                    }
            return render(request,"customers/profile.html",context)

@login_required
def notification_list(request):
    """ The notification instance would be automatically added by the context processor  customers.context_processor.notification.
    """
    return render(request,"customers/notification_list.html")

@login_required
def notification_detail(request,pk):
    """ This view is not a typical detail view, as it does not really renders a detail view of a notification instance, but confirms it was clicked or interacted with, therefore marking it as viewed. it redirects to the instance.url """
    instance = get_object_or_404(Notification,pk=pk,user=request.user)
    if not instance.viewed:
        instance.mark_as_viewed()
        instance.save()
    return redirect(instance.url)

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
            user = CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
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
                    user = CustomUser.objects.get(username=username)
                    if not user.is_active:
                        request.session["email"] = user.email
                        request.session["username"] = username
                        request.session.set_expiry(timedelta(minutes=10))
                        return redirect(reverse("customers:confirm_email"))
                except CustomUser.DoesNotExist:
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
        
