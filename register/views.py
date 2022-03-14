from django.shortcuts import render, redirect
from .forms import RegisterForm
from main.models import JobsList, ScrapedJobs, WishlistJobs


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            JobsList(name=username).save()
            ScrapedJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
            WishlistJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
        return redirect('/')
    else:
        form = RegisterForm()
    return render(response, 'register/register.html', {"form": form})

