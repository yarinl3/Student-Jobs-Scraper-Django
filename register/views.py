from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegisterForm


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(response, user)
                return redirect('/scraped_list')
    else:
        form = RegisterForm()
    return render(response, 'register/register.html', {"form": form})

