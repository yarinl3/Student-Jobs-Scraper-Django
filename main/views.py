import time

from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import ScrapForm, JobsListFrom
from bs4 import BeautifulSoup
from .Student_Jobs import jobs_scrap
from .models import JobsList, Job, ScrapedJobs
from threading import Thread


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
                threads = []

                def foo(checked, user):
                    if jobs_scrap(checked, user) is True:
                        errors.append(f'{checked} scraped successfully.')
                timeout = 5
                for i in checked_list:
                    t = Thread(target=foo, args=(i, username))
                    threads.append(t)
                    t.start()
                for t in threads:
                    start_time = time.time()
                    t.join(timeout)
                    timeout -= time.time() - start_time
                    if timeout < 0:
                        timeout = 0
                for site in checked_list:
                    site_in_errors = False
                    for error in errors:
                        if site in error:
                            site_in_errors = True
                    if site_in_errors is False:
                        errors.append(f'Failed to scrap {site} completely.\n'
                                      f'Some jobs may have been saved.')

        else:
            form = ScrapForm()
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()
