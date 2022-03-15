from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import ScrapForm, JobsListFrom
from bs4 import BeautifulSoup
from .Student_Jobs import jobs_scrap
from .models import JobsList, Job, ScrapedJobs


# Create your views here.
def home(response):
    return render(response, 'main/home.html', {'username': response.user})


def job_list(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        jobs = ScrapedJobs.objects.get(name=username).job_set.all()
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=link).delete()

        else:
            form = JobsListFrom()
        return render(response, 'main/job_list.html', {'form': form, 'jobs': jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def scrap(response):
    if response.user.is_anonymous is False:
        errors = []
        username = str(response.user)
        if response.method == "POST":
            form = ScrapForm(response.POST)
            if form.is_valid():
                t = ScrapedJobs.objects
                if len(t.filter(name=username)) == 0:
                    raise Exception(fr"Error: error in main\views.py, there is no list for {username}")
                elif len(t.filter(name=username)) > 1:
                    raise Exception(fr"Error: error in main\views.py, there is more than one list for {username}")
                ScrapedJobs.objects.get(name=username).delete()
                ScrapedJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
                soup = BeautifulSoup(str(form), 'html.parser')
                checked_list = []
                for i in soup.find_all('input'):
                    try:
                        i["checked"]  # noqa
                        if i['name'] != 'all':
                            checked_list.append(i['name'])
                    except Exception:
                        pass
                for i in checked_list:
                    if jobs_scrap(i, username) is True:
                        errors.append(f'{i} scraped successfully.')
                    else:
                        errors.append(f'Failed to scrap {i}.')
        else:
            form = ScrapForm()
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()