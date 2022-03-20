import time
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import ScrapForm, JobsListFrom, AddKeywordForm, DeleteKeywordForm
from .Student_Jobs import jobs_scrap
from .models import JobsList, Job, ScrapedJobs, WishlistJobs, JobsFilters
from threading import Thread
CHECKBOXLIST = ['alljobs', 'drushim', 'jobmaster', 'sqlink', 'telegram_jobs']


# Create your views here.
def home(response):
    return render(response, 'main/home.html', {'username': response.user})


def job_list(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        keywords_list = JobsFilters.objects.get(name=username).keyword_set.all()
        jobs = ScrapedJobs.objects.get(name=username).job_set.all()
        for job in jobs:
            for keyword in keywords_list:
                if keyword.keyword in job.title.lower():
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=job.link).delete()
        jobs = ScrapedJobs.objects.get(name=username).job_set.all()
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=link).delete()
                if val == 'Add to Wishlist':
                    job = ScrapedJobs.objects.get(name=username).job_set.filter(link=link)
                    if len(job) > 0:
                        job = job[0]
                        WishlistJobs.objects.get(name=username).job_set.create(title=job.title, link=job.link, sent=job.sent)
                        ScrapedJobs.objects.get(name=username).job_set.filter(link=link).delete()
                if val == 'Add to Sent':
                    ScrapedJobs.objects.get(name=username).job_set.filter(link=link).update(sent=True)
        else:
            form = JobsListFrom()
        new_jobs = []
        for job in jobs:
            if job.sent is False:
                new_jobs.append(job)
        return render(response, 'main/job_list.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def wishlist(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        jobs = WishlistJobs.objects.get(name=username).job_set.all()
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    WishlistJobs.objects.get(name=username).job_set.filter(link=link).delete()
                if val == 'Add to Sent':
                    WishlistJobs.objects.get(name=username).job_set.filter(link=link).update(sent=True)
        else:
            form = JobsListFrom()
        new_jobs = []
        for job in jobs:
            if job.sent is False:
                new_jobs.append(job)
        return render(response, 'main/wishlist.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
    else:
        raise PermissionDenied()


def sent(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        new_jobs = []
        for job in WishlistJobs.objects.get(name=username).job_set.all():
            if job.sent is True:
                new_jobs.append(job)
        for job in ScrapedJobs.objects.get(name=username).job_set.all():
            if job.sent is True:
                new_jobs.append(job)
        if response.method == "POST":
            form = JobsListFrom(response.POST)
            if form.is_valid():
                link = form.cleaned_data.get("link")
                val = form.cleaned_data.get("btn")
                if val == 'Delete':
                    wishlist_filter = WishlistJobs.objects.get(name=username).job_set.filter(link=link)
                    scraped_jobs_filter = ScrapedJobs.objects.get(name=username).job_set.filter(link=link)
                    if len(wishlist_filter) > 0:
                        new_jobs.remove((wishlist_filter[0]))
                    elif len(scraped_jobs_filter) > 0:
                        new_jobs.remove((scraped_jobs_filter[0]))
                    wishlist_filter.delete()
                    scraped_jobs_filter.delete()
        else:
            form = JobsListFrom()
        return render(response, 'main/sent.html', {'form': form, 'jobs': new_jobs, 'username': response.user})
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
                wishlist_jobs = WishlistJobs.objects.get(name=username).job_set.all()
                scraped_jobs = ScrapedJobs.objects.get(name=username).job_set.all()
                for scraped_job in scraped_jobs:
                    for wishlist_job in wishlist_jobs:
                        if scraped_job.link == wishlist_job.link:
                            ScrapedJobs.objects.get(name=username).job_set.filter(link=scraped_job.link).delete()
        else:
            form = ScrapForm()
        return render(response, 'main/scrap.html', {'form': form, 'errors': errors, 'username': response.user})
    else:
        raise PermissionDenied()


def keywords(response):
    if response.user.is_anonymous is False:
        username = str(response.user)
        add_form = AddKeywordForm(response.POST)
        del_form = DeleteKeywordForm(response.POST)
        if response.method == "POST":
            if add_form.is_valid():
                keyword = add_form.cleaned_data.get('keyword')
                if keyword != '' and \
                        len(JobsFilters.objects.get(name=username).keyword_set.filter(keyword=keyword.lower())) == 0:
                    JobsFilters.objects.get(name=username).keyword_set.create(keyword=keyword.lower())
            elif del_form.is_valid():
                keyword = del_form.cleaned_data.get('delete')
                JobsFilters.objects.get(name=username).keyword_set.filter(keyword=keyword.lower()).delete()

        keywords_list = JobsFilters.objects.get(name=username).keyword_set.all()
        return render(response, 'main/keywords.html', {'form': add_form, 'keywords': keywords_list, 'username': response.user})
    else:
        raise PermissionDenied()
