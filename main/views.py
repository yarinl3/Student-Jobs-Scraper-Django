import time
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import ScrapForm, JobsListFrom
from .Student_Jobs import jobs_scrap
from .models import JobsList, Job, ScrapedJobs
from threading import Thread
CHECKBOXLIST = ['alljobs', 'drushim', 'jobmaster', 'sqlink', 'telegram_jobs']


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
    scrap_start_time = time.time()
    if response.user.is_anonymous is False:
        errors = []
        username = str(response.user)
        if response.method == "POST":
            form = ScrapForm(response.POST)
            if form.is_valid():
                checked_list = []
                threads = []
                t = ScrapedJobs.objects
                timeout = 25

                if len(t.filter(name=username)) == 0:
                    raise Exception(fr"Error: error in main\views.py, there is no list for {username}")
                elif len(t.filter(name=username)) > 1:
                    raise Exception(fr"Error: error in main\views.py, there is more than one list for {username}")
                ScrapedJobs.objects.get(name=username).delete()
                ScrapedJobs(jobs_list=JobsList.objects.get(name=username), name=username).save()
                res = response.POST
                for key in res:
                    if key in CHECKBOXLIST and res.get(key) == 'on':
                        checked_list.append(key)

                def foo(checked, user):
                    if checked == 'telegram_jobs' and 'upload' in response.FILES:
                        error_flag, error_value = jobs_scrap(checked, user, response.FILES['upload'])
                    else:
                        error_flag, error_value = jobs_scrap(checked, user)

                    if error_flag is True:
                        errors.append(f'{checked} scraped successfully.')
                    else:
                        errors.append(error_value)

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
                        if site in str(error):
                            site_in_errors = True
                    if site_in_errors is False and time.time() - scrap_start_time >= 25:
                        errors.append(f'Timeout: 25 seconds passed and the scraping did not end.\n'
                                      f'If the connection to {site} is correct it will continue the scraping'
                                      f' in the background. ')

        else:
            form = ScrapForm()
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()
